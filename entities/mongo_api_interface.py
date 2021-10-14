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
                callable(subclass.delete)
                )

    @abc.abstractmethod
    def read(self) -> list:
        '''
        Read data from database
        :return: A list of recovered data
        '''
        pass

    @abc.abstractmethod
    def write(self, data: dict) -> dict:
        '''
        Insert an element into the database
        :param data: new data that will be inserted into the database
        :return: data inserted
        '''
        pass

    @abc.abstractmethod
    def update(self) -> dict:
        '''
        Edit data into the database
        :return: the new data value
        '''
        pass

    @abc.abstractmethod
    def delete(self, data: dict) -> dict:
        '''
        Removes an element from the database
        :param data: element that will be removed
        :return: removed element
        '''
        pass
