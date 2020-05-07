from RockchipCrawler import RockchipCrawler, RockchipFirmware
from pymongo import MongoClient

def main():
    crawler = RockchipCrawler()
    client = MongoClient()
    db = client.firmware_crawler
    collection = db.rockchip_firmware_metadata
    for firm in crawler.get_firms():
        collection.insert_one(firm.asMongoDocument)
        firm.download_files()

if __name__ == '__main__':
    main()