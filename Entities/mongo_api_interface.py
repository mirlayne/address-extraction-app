import abc


class MongoAPIInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
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
        pass

    @abc.abstractmethod
    def write(self, data: dict) -> dict:
        pass

    @abc.abstractmethod
    def update(self) -> dict:
        pass

    @abc.abstractmethod
    def delete(self, data: dict) -> dict:
        pass
