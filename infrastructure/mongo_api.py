import logging as log

from pymongo import MongoClient

from entities.mongodb_api_interface import MongoAPIInterface as IMongoAPI
from entities.mongodb_settings import MongoDBSettings as MongoDBSettings

log.basicConfig(
    filename='app.log',
    filemode='w',
    level=log.DEBUG,
    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s'
)


class MongoAPI(IMongoAPI):
    def __init__(self, mongodb_api_client: MongoClient, data: MongoDBSettings) -> None:
        self.client = mongodb_api_client

        database = data.database
        collection = data.collection
        self.cursor = self.client[database]  # corresponding to "mydb" variable of export2mongodb.py
        self.collection = self.cursor[collection]
        self.data = data

    def read(self) -> list:
        '''
        Read data from database
        :return: A list of recovered data
        '''

        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data: dict) -> dict:
        '''
        Insert an element into the database
        :param data: new data that will be inserted into the database
        :return: data inserted
        '''

        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self, data) -> dict:
        '''
        Edit data into the database
        :return: the new data value
        '''

        filt = data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data: dict) -> dict:
        '''
        Removes an element from the database
        :param data: element that will be removed
        :return: removed element
        '''

        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def get_column_names(self) -> list:
        '''
        Auxiliary function to avoid using a global variable
        :return: Value of variable "collist" in line 37 of export2mongodb.py
        '''
        return self.cursor.list_collection_names() # Value of variable "collist" in line 37 of export2mongodb.py

    def insert_in_collection(self, collection_name: str, data: any) -> None:
        '''
        Given a collection name the function removes all the data and put new information
        :param collection_name: name of the collection that will be updated
        :param data: data to put into the collection
        :return: None
        '''

        collection = self.cursor[collection_name]
        collection.delete_many({})
        collection.insert_many(data)

    def update_collection(self, collection_name: str, data: any) -> None:
        '''
        Given a collection name the function removes all the data and put new information
        :param collection_name: name of the collection that will be updated
        :param data: data to put into the collection
        :return: None
        '''

        collection = self.cursor[collection_name]
        collection.update_many(data)

