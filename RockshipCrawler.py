from GeneralCrawler import GeneralCrawler, Firmware

class RockshipCrawler(GeneralCrawler):
    def __init__(self, server_url):
        super().__init__(server_url)

    def get_firms(self):
        """
        The funcion will get all the firms in Rockship website
        :return: Generator that yield tupple of firmware name and link for it's webpage for every firmware
        """
        for page in self.get_pages():
            soup = GeneralCrawler.get_soup(page)
            # Finding all table rows that contain the link for the firmware webpage
            for link_td in soup.find_all('td', {'class': 'views-field-title'}):
                link = link_td.find('a')
                # Link is relative and in the following format node\{num}, changing it to absolute link 
                abs_link = self._server_url + link['href'].replace('\\', '/')
                yield link.text, abs_link

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
    def __init__(self, device_name, version, build_date):
        super().__init__(device_name, version, build_date)

    