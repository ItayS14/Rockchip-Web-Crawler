from GeneralCrawler import GeneralCrawler, Firmware
import os

class RockchipCrawler(GeneralCrawler):
    def __init__(self):
        super().__init__('https://www.rockchipfirmware.com/')

    def get_firms(self, exists):
        """
        The funcion will get all the new firmwares in Rockchip website
        :param exists: pointer to function that checks if a firmware exists in memory by it's name (fnc that gets name as arg)
        :return: Generator that yield RockchipFirmware for every firmware in the website
        """
        for page in self.get_pages():
            soup = GeneralCrawler.get_soup(page)
            # Finding all table rows that contain the link for the firmware webpage
            for link_td in soup.find_all('td', {'class': 'views-field-title'}):
                link = link_td.find('a')
                if not exists(link.text):
                    # Link is relative and in the following format node\{num}, changing it to absolute link 
                    abs_link = self._server_url + link['href'].replace('\\', '/')
                    yield RockchipFirmware.from_web_link(abs_link)
                
    def get_pages(self):
        """
        The function will yield all the pages that has firmware from the Rockchip website
        :return: Generator that yields links to pages
        """
        full_link = self._server_url + 'firmware-downloads' # Link to the first page
        while True:
            yield full_link
            page = GeneralCrawler.get_soup(full_link)
            next_page_link = page.find('a', {'title': 'Go to next page'})
            if next_page_link is None: # Last page
                break
            full_link = self._server_url + next_page_link['href']


class RockchipFirmware(Firmware):
    def __init__(self, device_name, model,version, build_date, brand, is_rooted, links_for_files):
        super().__init__(device_name, model, version, build_date, brand, is_rooted, links_for_files)

    @classmethod
    def from_web_link(cls, url):
        """
        Constructor for RockchipFirmware class from web page link
        :param url: link for the webpage (str)
        """
        soup = GeneralCrawler.get_soup(url)

        return cls(
            RockchipFirmware.get_info(soup, 'title'),
            RockchipFirmware.get_info(soup, 'field-model'),
            RockchipFirmware.get_info(soup, 'field-android-version2'),
            RockchipFirmware.get_info(soup, 'changed-date'),
            RockchipFirmware.get_info(soup, 'field-brand'),
            RockchipFirmware.get_info(soup, 'field-rooted') == 'Rooted',
            RockchipFirmware.get_files(soup)
        )

    def download_files(self, directory=""):
        """
        Function that inherit the Firmware.download_files, it makes sure that a directory Rockchip is created
        :param directory: base directory to save the files to, by default into {current_dir}/Rockchip - (str)
        """
        new_dir = os.path.join(directory, 'Rockchip')
        super().download_files(new_dir)

    @staticmethod 
    def get_info(soup, name):
        """
        The function will get inforamtion about spesific name, i.e changed-date
        :param soup: the html of the website (BeautifulSoup)
        :param name: the name of the field to get the info 
        :return: the information of the name (str, or None if doesn't exist)
        """
        div = soup.find('div', {'class': 'field-name-' + name})
        if div:
            return div.find('div', {'class': 'field-item'}).text
        return None

    @staticmethod
    def get_files(soup):
        """
        The function will get list of files relevant to the firmware
        :param soup: the html of the website (BeautifulSoup)
        :return: the files relevant to the firmware (list)
        """
        # Case that the files are organized in a table in the website
        files = [file.find('a')['href'] for file in soup.find_all('span', {'class': 'file'})]
        if files:
             return files
            
        # Case that files are organized like the other data
        div = soup.find('div', {'class': 'field-name-field-firmware-image-download'})
        if div:
            return [a['href'] for a in div.find_all('a')]
            
        return []
