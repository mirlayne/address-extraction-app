import abc
from typing import Iterator

class MongoDBCollectionsPreprocessInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        '''
        Helper function to check subclass relation
        :param subclass: Name of the subclass
        :return: True or False
        '''
        return (hasattr(subclass, 'load_array_collection') and
                callable(subclass.load_array_collection) and
                hasattr(subclass, 'patch_hida') and
                callable(subclass.patch_hida) and
                hasattr(subclass, 'patch_resolved') and
                callable(subclass.patch_resolved) and
                hasattr(subclass, 'project_metadata_hida') and
                callable(subclass.project_metadata_hida) and
                hasattr(subclass, 'patch_dir') and
                callable(subclass.patch_dir) and
                hasattr(subclass, 'patch_keywords') and
                callable(subclass.patch_keywords) and
                hasattr(subclass, 'project_metadata_keywords') and
                callable(subclass.project_metadata_keywords) and
                hasattr(subclass, 'unproject_metadata_keywords') and
                callable(subclass.unproject_metadata_keywords) and
                hasattr(subclass, 'project_hida') and
                callable(subclass.project_hida) and
                hasattr(subclass, 'patch_vorhaben') and
                callable(subclass.patch_vorhaben) and
                hasattr(subclass, 'patch_categories') and
                callable(subclass.patch_categories) and
                hasattr(subclass, 'load_embddings') and
                callable(subclass.load_embddings) and
                hasattr(subclass, 'load_no_matches') and
                callable(subclass.load_no_matches) and
                hasattr(subclass, 'patch_inv_taxo') and
                callable(subclass.patch_inv_taxo) and
                hasattr(subclass, 'project_hida_inv_taxo') and
                callable(subclass.project_hida_inv_taxo) and
                hasattr(subclass, '_color_generator') and
                callable(subclass._color_generator)
                )

    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def load_array_collection(self, filename: str) -> dict:
        '''
        The same as "loadArrayCollection" on export2mongodb.py
        :param filename:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_hida(self, filename: str) -> list:
        '''
        The same as "patchHida" on export2mongodb.py file
        :param filename:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_resolved(self, filename: str, hida_col: list) -> list:
        # TODO: check the part find_one function
        '''
        The same as "patchResolved" on export2mongodb.py file
        :param filename:
        :param hida_col: dictionary from the collection "hida"
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def project_metadata_hida(self, metadata_col: list, hida_col: list) -> Iterator[dict]:
        # TODO: check the part find_one function
        '''
        The same as "projectMetaDataHida" on export2mongodb.py
        :param metadata_col:
        :param hida_col:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_dir(self, folders_dict: list, path: str) -> Iterator[dict]:
        '''
        The same as "patchDir" on export2mongodb.py
        :param folders_dict: all the documents of the collection
        :param path:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_keywords(self, topics_dict: list) -> Iterator[dict]:
        '''
        The same as "patchKeywords" on export2mongodb.py
        :param topics_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def project_metadata_keywords(self, collection_dict: list) -> Iterator[dict]:
        '''
        The same as "patchMetaDataKeywords" on export2mongodb.py
        :param collection_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def unproject_metadata_keywords(self, collection_dict: list) -> Iterator[dict]:
        '''
        The same as "unprojectMetaDataKeywords" on export2mongodb.py
        :param collection_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def project_hida(self, resolved_dict: list) -> Iterator[dict]:
        '''
        The same as "projectHida" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_vorhaben(self, resolved_dict: list) -> Iterator[dict]:
        '''
        The same as "patchVorhaben" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_categories(self, vorhabeninv_dict: list) -> list:
        '''
        The same as "patchCategories" on export2mongodb.py
        :param vorhabeninv_dict: all the documents of the collection
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def load_embeddings(self, filename: str) -> list:
        '''
        The same as "loadEmbddings" on export2mongodb.py
        :param filename:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def load_no_matches(self, filename: str) -> list:
        '''
        The same as "loadNoMatches" on export2mongodb.py
        :param filename:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def patch_inv_taxo(self, resolved_dict: list, invtaxo: list) -> Iterator[dict]:
        # TODO: fix this function
        '''
        The same as "patchInvTaxo" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :param invtaxo:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def project_hida_inv_taxo(self, hida_col: list, invtaxo_col: list) -> Iterator[dict]:
        # TODO: fix this function
        '''
        The same as "projectHidaInvTaxo" on export2mongodb.py
        :param hida_col:
        :param invtaxo_col:
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def _color_generator(self, number_of_colors: int) -> list:
        '''
        The same as "color_generator" on export2mongodb.py
        :param number_of_colors:
        :return:
        '''
        raise NotImplementedError