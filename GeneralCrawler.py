from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import unquote

# General abstract class that each crawler will inherite from
class GeneralCrawler:
    def __init__(self, server_url):
        self._server_url = server_url 
    
    def get_firms(self, exists):
        """
        Generator fucnction that yields all the new firmwares in the website
        :param exists: pointer to function that checks if a firmware exists in memory by it's name (fnc that gets name as arg)
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
    def __init__(self, device_name, model, version, build_date, brand, is_rooted, links_for_files):
        self._device_name = device_name
        self._model = model
        self._version = version
        self._build_date = build_date
        self._brand = brand
        self._is_rooted = is_rooted
        self._links_for_files = links_for_files

    def download_files(self, directory=""):
        """
        The function will download the files of the firmware 
        :param directory: directory to download the files to, by default - current directory (str)
        """
        # Stopping if there is no files to download
        if not self.files:
            return

        # Creating directory: /{brand_name}/{device_name} and inside will be placed list of files
        dir_path = os.path.join(directory, self._brand, self._device_name)
        try:
            os.makedirs(dir_path, exist_ok=True)
        except PermissionError:
            print(f'error: no permission to access {dir_path}')
            exit()

        for file_name, link in zip(self.files, self._links_for_files):
            file_content = requests.get(link).content
            with open(os.path.join(dir_path, file_name), 'wb') as f:
                f.write(file_content)

    @property
    def mongo_document(self):
        """
        Property that returns the class as a dictionary to save in the mongoDB
        """
        return {
            'device_name' : self._device_name,
            'model': self._model,
            'version': self._version,
            'build_date': self._build_date,
            'brand': self._brand,
            'is_rooted': self._is_rooted,
            'files': self.files
        }

    @property
    def files(self):
        """
        Property that returns only the filename from the file url stored in the class, and will url decode the file
        """
        files = []
        for file_link in self._links_for_files:
            file_name = file_link[file_link.rfind('/') + 1:]
            files.append(unquote(file_name))
        return files

    def __str__(self):
        return f'{self._device_name} by {self._brand}, device model is: {self._model}'