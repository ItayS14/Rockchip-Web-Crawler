# Rockchip Web Crawler

Command line tool targeted for **Ubuntu 18.04, python 3.6 or higher**,  that crawls websites, finding firmwares download them and store their metadata in MongoDB.

At the momment the only website which is supported is [Rockchip]('https://www.rockchipfirmware.com/')

### Using 

Using is simple as:

```bash
python main.py [options] server_url
```

Make sure you have MongoDB setup, and submit the connection string as an argument with --uri option in case that isn't the default connection string.

Full usage guide:

```bash
usage: main.py [-h] [-u URI] [-v] [-d DIRECTORY] server_url

positional arguments:
  server_url            The url to the website you wish to crawl

optional arguments:
  -h, --help            show this help message and exit
  -u URI, --uri URI     Uri for the mongoDB, default is:
                        mongo://localhost:27017/
  -v, --verbose         If enabled, displaying the output of the program
  -d DIRECTORY, --directory DIRECTORY
                        Directory to download the files to, by default in
                        {current_directory}/{crawler_name}
```

### Installing

Clone the repository and install the dependencies:

 ```bash
git clone https://github.com/ItayS14/Rockchip-Web-Crawler
pip install beautifulsoup4
 ```



