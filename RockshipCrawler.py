from GeneralCrawler import GeneralCrawler, Firmware

class RockshipCrawler(GeneralCrawler):
    def __init__(self, server_url):
        super().__init__(server_url)

    def get_firms(self):
        """
        The funcion will get all the firms in Rockship website
        :return: Generator that yield RockshipFirmware for every firmware in the website
        """
        for page in self.get_pages():
            soup = GeneralCrawler.get_soup(page)
            # Finding all table rows that contain the link for the firmware webpage
            for link_td in soup.find_all('td', {'class': 'views-field-title'}):
                link = link_td.find('a')
                # Link is relative and in the following format node\{num}, changing it to absolute link 
                abs_link = self._server_url + link['href'].replace('\\', '/')
                yield RockshipFirmware.fromWebLink(abs_link)

    def get_pages(self):
        """
        The function will yield all the pages that has firmware from the Rockship website
        :return: Generator that yields links to pages
        """
        full_link = self._server_url + 'firmware-downloads'
        while True:
            yield full_link
            page = GeneralCrawler.get_soup(full_link)
            next_page_link = page.find('a', {'title': 'Go to next page'})
            if next_page_link is None: # Last page
                break
            full_link = self._server_url + next_page_link['href']


class RockshipFirmware(Firmware):
    def __init__(self, device_name, version, build_date, brand, is_rooted):
        super().__init__(device_name, version, build_date, brand, is_rooted)

    @classmethod
    def fromWebLink(cls, url):
        """
        Constructor for RockshipFirmware class from web page link
        :param url: link for the webpage (str)
        """
        soup = GeneralCrawler.get_soup(url)
        return cls(
            RockshipFirmware.get_info(soup, 'field-name-title'),
            RockshipFirmware.get_info(soup, 'field-name-field-android-version2'),
            RockshipFirmware.get_info(soup, 'field-name-changed-date'),
            RockshipFirmware.get_info(soup, 'field-name-field-brand'),
            RockshipFirmware.get_info(soup, 'field-name-field-rooted') == 'Rooted'
        )

    @staticmethod 
    def get_info(soup, name):
        """
        The function will get inforamtion about spesific name, i.e field-name-changed-date
        :param soup: the html of the website (BeautifulSoup)
        :param name: the name of the field to get the info (str, or None if doesn't exists)
        """
        div = soup.find('div', {'class': name})
        if div:
            return div.find('div', {'class': 'field-item'}).text
        return None