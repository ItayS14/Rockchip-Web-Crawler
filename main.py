from RockchipCrawler import RockchipCrawler, RockchipFirmware
from pymongo import MongoClient

def main():
    crawler = RockchipCrawler()
    client = MongoClient()
    db = client.firmware_crawler
    collection = db.rockchip_firmware_metadata
    
    # Function that checks if the name exists in the database, needed for the crawler.get_firms to know which firmwares to yield
    exists = lambda name: collection.count_documents({'device_name': name}) > 0
    
    for firm in crawler.get_firms(exists):
        collection.insert_one(firm.mongo_document)
        firm.download_files()

if __name__ == '__main__':
    main()