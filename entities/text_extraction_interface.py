import abc

from pydantic import NonNegativeInt


class TextExtraction(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        '''
        Helper function to check subclass relation
        :param subclass: Name of the subclass
        :return: True or False
        '''
        return (hasattr(subclass, '__init__') and
                callable(subclass.__init__) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) and
                hasattr(subclass, 'extract_meta') and
                callable(subclass.extract_meta) and
                hasattr(subclass, 'process_document') and
                callable(subclass.process_document)
                )

    @abc.abstractmethod
    def __init__(self, tika_server: str) -> None:
        self.tika_client = tika_server

    @abc.abstractmethod
    def extract_text(self, file_path: str) -> str:
        '''
        Function corresponding to extract_text in module extractText.py from https://github.com/cfillies/semkibardoc
        :param file_path:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def extract_meta(self, file_path: str) -> dict:
        '''
        Function corresponding to extract_meta in module extractText.py from https://github.com/cfillies/semkibardoc
        :param file_path:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def process_document(self, district: str, path: str, col: list, startindex: NonNegativeInt,
                         deleteall: bool) -> None:
        '''
        Function corresponding to extractText in module extractText.py from https://github.com/cfillies/semkibardoc
        :param district:
        :param path:
        :param col:
        :param startindex:
        :param deleteall:
        :return:
        '''
        raise NotImplementedError
