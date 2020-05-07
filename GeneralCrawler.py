from bs4 import BeautifulSoup
import requests

# General abstract class that each crawler will inherite from
class GeneralCrawler:
    def __init__(self, server_url):
        self._server_url = server_url
    
    def get_firms(self):
        """
        Generator fucnction that yields all the firms in the website
        :return: Generator of Firmware class
        """
        raise NotImplementedError

    @staticmethod
    def get_soup(url):
        """
        The function will get a BeautifulSoup object from the url
        :param url: link to a webpage (str)
        :return: html code of the website as BeautifulSoup object
        """
        res = requests.get(url)
        return BeautifulSoup(res.text, 'html.parser')

# Class that represents a firmware that was crawled
class Firmware:
    def __init__(self, device_name, model, version, build_date, brand, is_rooted, files):
        self._device_name = device_name
        self._model = model
        self._version = version
        self._build_date = build_date
        self._brand = brand
        self._is_rooted = is_rooted
        self._files = files

    def __str__(self):
        return f'Firmware {self._device_name} by {self._brand}, device model is: {self._model}'