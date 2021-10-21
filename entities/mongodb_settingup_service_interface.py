import abc
from typing import Any, Callable

# All the functions interfaces were made from the functions on file export2mongodb.py in
# https://github.com/cfillies/semkibardoc


class MongoDBSettingUpService:
    @classmethod
    def __subclasshook__(cls, subclass):
        '''
        Helper function to check subclass relation
        :param subclass: Name of the subclass
        :return: True or False
        '''
        return (hasattr(subclass, 'mongo_export') and
                callable(subclass.mongo_export)
                )

    @abc.abstractmethod
    def create_fill_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to create a collection
        :param collection_function: function that will get the data to fill the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    @create_fill_collection
    def collection_from_json(self, collection_name: str):
        '''
        Get the data to fill a collection
        :param collection_name: name of the collection that will be created
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def insert_one_in_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to insert one element into a collection
        :param collection_function: function that gets the element that will be inserted in the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    @insert_one_in_collection
    def create_insert_one(self, **kwargs):
        '''
        Get an element that will be inserted in a collection
        :param kwargs:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def insert_many_in_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to insert many elements in a collection
        :param collection_function:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    @insert_many_in_collection
    def create_insert_many(self, **kwargs) -> Any:
        '''
        Gets a list of elements that will be inserted in a collection
        :param kwargs:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def mongo_export(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
        '''
        Function corresponding to "mongoExport" on file export2mongodb.py
        :param mongodb_utils_filepath: json file that stores the necessary data such as column names and utils json file names
        :param hida_name: name of hida file
        :param metadata_name: name of metadata
        :param json_folderpath: folder where are stored the json files
        :return:
        '''
        raise NotImplementedError