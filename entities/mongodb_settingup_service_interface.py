import abc

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