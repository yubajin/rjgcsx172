import pymongo
from config import *

class Query:

    def __init__(self):
        self.link_dics = []
        self.details_dics = []

    def query_majors(self):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        schools_collection = db[SCHOOLS_COLLECTION]
        for collection in schools_collection.find():
            link_dic = {
                'id':str(collection['_id']),
                'school':collection['school'][7:],
                'link':collection['link']
            }
            self.link_dics.append(link_dic)

        return  self.link_dics

    def query_details(self):
        client = pymongo.MongoClient(MONGO_URL)
        db = client[MONGO_DB]
        majors_collection = db[MAJORS_COLLECTION]

        for collection in majors_collection.find():
            details_dic = {
                'url':collection['details_link'],
                'school':collection['school'],
                'department':collection['department'],
                'marjor':collection['marjor'],
                'direction':collection['direction']
            }
            self.details_dics.append(details_dic)
        return  self.details_dics

    def main(self):
        # majors = self.query_majors()
        major = self.query_details()
if __name__ == '__main__':
    query = Query()
    query.main()