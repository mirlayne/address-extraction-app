import logging as log

from pymongo import MongoClient

log.basicConfig(
    filename='app.log',
    filemode='w',
    level=log.DEBUG,
    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s'
)

class MongoAPI:
    def __init__(self, data: dict) -> None:
        self.client = MongoClient("mongodb://localhost:27017/")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self) -> list:
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data: dict) -> dict:
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self) -> dict:
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data: dict) -> dict:
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output