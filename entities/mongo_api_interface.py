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

    @abc.abstractmethod
    def get_column_names(self) -> list:
        '''
        Auxiliary function to avoid using a global variable
        :return: Value of variable "collist" in line 37 of export2mongodb.py
        '''
        pass

    # All the functions interfaces were made from the functions on file export2mongodb.py in https://github.com/cfillies/semkibardoc

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
        pass

    @abc.abstractmethod
    def load_array_collection(self, filename: str, colname: str) -> None:
        '''
        The same as "loadArrayCollection" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_hida(self, filename: str, hidaname: str) -> None:
        '''
        The same as "patchHida" on export2mongodb.py file
        :param hidaname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_resolved(self, resolvedname: str, filename: str, hidaname: str) -> None:
        '''
        The same as "patchResolved" on export2mongodb.py file
        :param filename:
        :param hidaname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def project_metadata_hida(self, metadataname: str, hidaname: str) -> None:
        '''
        The same as "projectMetaDataHida" on export2mongodb.py
        :param metadataname:
        :param hidaname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def load_dict_collection(self, filename: str, colname: str) -> None:
        '''
        The same as "loadDictCollection" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_dir(self, resolvedname: str, folders: str, path: str) -> None:
        '''
        The same as "patchDir" on export2mongodb.py
        :param resolvedname:
        :param folders:
        :param path:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_keywords(self, resolvedname: str, topicsname: str) -> None:
        '''
        The same as "patchKeywords" on export2mongodb.py
        :param resolvedname:
        :param topicsname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def project_metadata_keywords(self, metadataname: str) -> None:
        '''
        The same as "patchMetaDataKeywords" on export2mongodb.py
        :param metadataname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def unproject_metadata_keywords(self, metadataname: str) -> None:
        '''
        The same as "unprojectMetaDataKeywords" on export2mongodb.py
        :param metadataname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def project_hida(self, resolvedname: str) -> None:
        '''
        The same as "projectHida" on export2mongodb.py
        :param resolvedname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_vorhaben(self, resolvedname: str) -> None:
        '''
        The same as "patchVorhaben" on export2mongodb.py
        :param resolvedname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_categories(self, words: str, categoriesname: str) -> None:
        '''
        The same as "patchCategories" on export2mongodb.py
        :param words:
        :param categoriesname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def load_embddings(self, filename: str, colname: str) -> None:
        '''
        The same as "loadEmbddings" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def load_no_matches(self, filename: str, colname: str) -> None:
        '''
        The same as "loadNoMatches" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        pass

    @abc.abstractmethod
    def patch_inv_taxo(self, resolvedname: str, invtaxo: str) -> None:
        '''
        The same as "patchInvTaxo" on export2mongodb.py
        :param resolvedname:
        :param invtaxo:
        :return:
        '''
        pass

    @abc.abstractmethod
    def project_hida_inv_taxo(self, hidaname: str, invtaxo: str) -> None:
        '''
        The same as "projectHidaInvTaxo" on export2mongodb.py
        :param hidaname:
        :param invtaxo:
        :return:
        '''
        pass

    @abc.abstractmethod
    def color_generator(self, number_of_colors) -> list:
        # TODO: Check whether this function should be here
        '''
        The same as "color_generator" on export2mongodb.py
        :param number_of_colors:
        :return:
        '''
        pass
