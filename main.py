from RockchipCrawler import RockchipCrawler, RockchipFirmware
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import argparse


def validate_client(client):
    """
    The function will check if it the MongoClient is valid (was initialized with valid uri)
    :param client: the mongodb client to check
    :return: client is valid or not (bool)
    """
    try:
        client.admin.command('ismaster') 
    except ConnectionFailure:
        return False
    else:
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_url', help='The url to the website you wish to crawl')
    parser.add_argument('-u', '--uri', help='Uri for the mongoDB, default is: mongo://localhost:27017/', default='mongodb://localhost:27017/')
    parser.add_argument('-v', '--verbose', help='If enabled, displaying the output of the program', action='store_true')
    parser.add_argument('-d', '--directory', help='Directory to download the files to, by default in {current_directory}/{crawler_name}', default='')
    args = parser.parse_args()
    
    client = MongoClient(args.uri, serverSelectionTimeoutMS=2)
    if not validate_client(client):
        print('error: MongoDB server not available')
        exit()
    db = client.firmware_crawler
    if args.verbose:
        print(f'Connected to db in {args.uri}')
        
    # Any new crawler will be added here with it's collection
    supported_websites = {
        'https://www.rockchipfirmware.com/': (RockchipCrawler(), db.rockchip_firmware_metadata)
    }
    
    if args.server_url not in supported_websites.keys():
        print(f'error: "{args.server_url}" website is not supported at the moment')
        print('Supported websites:')
        print('\n'.join(supported_websites.keys()))
        exit()

    crawler, collection = supported_websites[args.server_url]

    # Function that checks if the name exists in the database, needed for the crawler.get_firms to know which firmwares to yield
    exists = lambda name: collection.count_documents({'device_name': name}) > 0
    for firm in crawler.get_firms(exists):
        if args.verbose:
            print('New firm found:', firm)
            print('Downloading:', firm.files)
        collection.insert_one(firm.mongo_document)
        firm.download_files(args.directory)


if __name__ == '__main__':
    main()