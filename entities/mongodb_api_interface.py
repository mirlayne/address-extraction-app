import abc


class MongoAPIInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        '''
        Helper function to check subclass relation
        :param subclass: Name of the subclass
        :return: True or False
        '''
        return (hasattr(subclass, 'read') and
                callable(subclass.read) and
                hasattr(subclass, 'write') and
                callable(subclass.write) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete) and
                hasattr(subclass, 'get_column_names') and
                callable(subclass.get_column_names) and
                hasattr(subclass, 'update_collection') and
                callable(subclass.update_collection)
                )

    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def read(self) -> list:
        '''
        Read data from database
        :return: A list of recovered data
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, data: dict) -> dict:
        '''
        Insert an element into the database
        :param data: new data that will be inserted into the database
        :return: data inserted
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def update(self) -> dict:
        '''
        Edit data into the database
        :return: the new data value
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, data: dict) -> dict:
        '''
        Removes an element from the database
        :param data: element that will be removed
        :return: removed element
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def get_column_names(self) -> list:
        '''
        Auxiliary function to avoid using a global variable
        :return: Value of variable "collist" in line 37 of export2mongodb.py
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def update_collection(self, collection_name: str, data: any) -> None:
        '''
        Given a collection name the function removes all the data and put new information
        :param collection_name: name of the collection that will be updated
        :param data: data to put into the collection
        :return: None
        '''
        raise NotImplementedError




