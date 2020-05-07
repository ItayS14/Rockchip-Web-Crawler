# Rockchip Web Crawler

Command line tool targeted for **Ubuntu 18.04, python 3.6 or higher**,  that crawls websites, finding firmwares download them and store their metadata in MongoDB.

At the momment the only website which is supported is [Rockchip]('https://www.rockchipfirmware.com/')

### Using 

Using is simple as:

```bash
python main.py [options] server_url
```

Make sure you have MongoDB setup, and submit the connection string as an argument with --uri option in case that isn't the default connection string.

### Installing

Clone the repository and install the decencies:

 ```bash
git clone https://github.com/ItayS14/Rockchip-Web-Crawler
pip install beautifulsoup4
 ```



