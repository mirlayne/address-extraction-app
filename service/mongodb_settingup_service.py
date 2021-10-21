import json
import os
from typing import Any, Callable

from entities.mongodb_api_interface import MongoAPIInterface as IMongoAPI
from entities.mongodb_collections_preprocess_interface import MongoDBCollectionsPreprocessInterface \
    as IMongoDBCollectionsPreprocess


class MongoDBSettingUpService:

    def __init__(self, mongodb_api_obj: IMongoAPI, mongodb_col_preproc: IMongoDBCollectionsPreprocess, json_folderpath: str):
        self.mongodb_api_obj = mongodb_api_obj
        self.mongodb_col_preproc = mongodb_col_preproc
        self.json_folderpath = json_folderpath

    def mongo_export(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str) -> None:
        '''
        Function corresponding to "mongoExport" on file export2mongodb.py
        :param mongodb_utils_filepath: json file that stores the necessary data such as column names and utils json file names
        :param hida_name: name of hida file
        :param metadata_name: name of metadata
        :param json_folderpath: folder where the json files are stored
        :return:
        '''

        with open(mongodb_utils_filepath, 'r') as mongodb_file:
            mongodb_dict = json.load(mongodb_file)

        mongodb_column_dict = mongodb_dict["columns"]
        mongodb_files_dict = mongodb_dict["json_files"]

        hidaname = hida_name
        metadataname = metadata_name

        mongodb_col_preproc = IMongoDBCollectionsPreprocess()

        self.mongodb_api_obj.collection = metadataname
        metadata_col_obj = self.mongodb_api_obj.read()

        self.mongodb_api_obj.collection = hidaname
        hida_col_dict = self.mongodb_api_obj.read()

        if mongodb_column_dict.get("ispattern", False):
            self.create_fill_collection(mongodb_files_dict["pattern"])

        if mongodb_column_dict.get("isfolders", False):
            self.create_fill_collection(mongodb_files_dict["files"])
            self.create_fill_collection(mongodb_files_dict["koepnick_files"])

        if mongodb_column_dict.get("isbadlist", False):
            self.create_fill_collection(mongodb_files_dict["badlist"])

        if mongodb_column_dict.get("isvorhaben", False):
            self.create_fill_collection(mongodb_files_dict["vorhaben"])

        if mongodb_column_dict.get("istopics", False):
            self.create_fill_collection(mongodb_files_dict["topics3a"])

        if mongodb_column_dict.get("isvorhabeninv", False):
            self.create_fill_collection(mongodb_files_dict["vorhaben_inv"])

        if mongodb_column_dict.get("istaxo", False):
            self.create_fill_collection(mongodb_files_dict["taxo"])

        if mongodb_column_dict.get("isinvtaxo", False):
            self.create_fill_collection(mongodb_files_dict["taxo_inv"])

        if mongodb_column_dict.get("isemblist", False):
            self.create_fill_collection(mongodb_files_dict["all_matches"])

        if mongodb_column_dict.get("isnoemblist", False):
            self.create_fill_collection(mongodb_files_dict["no_matches"])

        if mongodb_column_dict.get("ishida", False):
            self.create_fill_collection(mongodb_files_dict["hida"])

        if mongodb_column_dict.get("isresolved", False):
            self.create_fill_collection(mongodb_files_dict["resolved"])

        if mongodb_column_dict.get("iscategories", False) or mongodb_column_dict.get("isvorhabeninv", False):
            json_path = os.path.join(self.json_folderpath, mongodb_files_dict["vorhaben_inv"])
            data = mongodb_col_preproc.patch_categories(json_path)
            self.mongodb_api_obj.collection = "categories"
            self.mongodb_api_obj.write(data)

        if mongodb_column_dict.get("ismetadatahida", False):
            self.create_insert_one(self.mongodb_col_preproc.project_metadata_hida, metadataname, metadata_col_obj, hida_col_dict)

        if mongodb_column_dict.get("ismetadatanokeywords", False):
            self.create_insert_one(self.mongodb_col_preproc.unproject_metadata_keywords, metadataname, metadata_col_obj)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatehida", False):
            self.create_insert_one(self.mongodb_col_preproc.project_hida, metadataname, metadata_col_obj)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatevorhaben", False):
            self.create_insert_one(self.mongodb_col_preproc.patch_vorhaben, metadataname, metadata_col_obj)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatetaxo", False) or \
                mongodb_column_dict.get("ismetadatahida", False):
            self.mongodb_api_obj.collection = "invtaxo"
            invtaxo_list = self.mongodb_api_obj.read()
            self.create_insert_one(self.mongodb_col_preproc.project_metadata_hida, metadataname, metadata_col_obj, invtaxo_list)

        if mongodb_column_dict.get("ishida", False) or mongodb_column_dict.get("isupdatehidataxo", False):
            self.mongodb_api_obj.collection = "invtaxo"
            invtaxo_list = self.mongodb_api_obj.read()
            self.create_insert_one(self.mongodb_col_preproc.project_metadata_hida, hidaname, metadata_col_obj, invtaxo_list)

        if mongodb_column_dict.get("ispatch_dir", False) or mongodb_column_dict.get("isresolved", False):
            self.mongodb_api_obj.collection = "folders"
            folders_coll = self.mongodb_api_obj.read()
            data_gen = mongodb_col_preproc.patch_dir(folders_coll, r"C:\Data\test\KIbarDok")  # TODO: Ask what the use of this file or folder is
            self.mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    self.mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("istopics", False) or \
                mongodb_column_dict.get("iskeywords", False):
            data_gen = mongodb_col_preproc.patch_keywords(metadata_col_obj)
            self.mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    self.mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ismetadatakeywords", False):
            data_gen = mongodb_col_preproc.project_metadata_keywords(metadata_col_obj)
            self.mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    self.mongodb_api_obj.update(data)
                except StopIteration:
                    break

    def create_fill_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to create a collection
        :param collection_function: function that will get the data to fill the collection
        :return:
        '''
        def wrapper(*args, **kwargs):
            data = collection_function(*args, **kwargs)
            self.mongodb_api_obj.collection = args[0]  # collection_name: str
            self.mongodb_api_obj.insert_in_collection(data)
        return wrapper

    @create_fill_collection
    def collection_from_json(self, collection_name: str):
        '''
        Get the data to fill a collection
        :param collection_name: name of the collection that will be created
        :return:
        '''
        json_path = os.path.join(self.json_folderpath, collection_name)
        return self.mongodb_col_preproc.load_array_collection(json_path)

    def insert_one_in_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to insert one element into a collection
        :param collection_function: function that gets the element that will be inserted in the collection
        :return:
        '''
        def wrapper(*args, **kwargs):
            data_gen = collection_function(*args, **kwargs)
            self.mongodb_api_obj.collection = kwargs["collection_name"]  # collection_name: str
            while True:
                try:
                    data = next(data_gen)
                    self.mongodb_api_obj.write(data)
                except StopIteration:
                    break
        return wrapper

    @insert_one_in_collection
    def create_insert_one(self, **kwargs):
        '''
        Get an element that will be inserted in a collection
        :param kwargs:
        :return:
        '''
        collection_name = kwargs["collection_name"]
        function_ref = kwargs["function_ref"]
        function_args = kwargs["function_args"]
        json_path = os.path.join(self.json_folderpath, collection_name)
        return function_ref(*function_args, json_path)

    def insert_many_in_collection(self, collection_function: Callable) -> None:
        '''
        Decorator to insert many elements in a collection
        :param collection_function:
        :return:
        '''
        def wrapper(*args, **kwargs):
            data_gen = collection_function(*args, **kwargs)
            self.mongodb_api_obj.collection = kwargs["collection_name"]  # collection_name: str
            while True:
                try:
                    data = next(data_gen)
                    self.mongodb_api_obj.update(data)
                except StopIteration:
                    break
        return wrapper

    @insert_many_in_collection
    def create_insert_many(self, **kwargs) -> Any:
        '''
        Gets a list of elements that will be inserted in a collection
        :param kwargs:
        :return:
        '''
        collection_name = kwargs["collection_name"]
        function_ref = kwargs["function_ref"]
        function_args = kwargs["function_args"]
        json_path = os.path.join(self.json_folderpath, collection_name)
        return function_ref(*function_args, json_path)

    def extract_metadata(self, mongodb_utils_filepath: str, folders: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
        metadataname = metadata_name

        mongodb_collections_names = self.mongodb_api_obj.get_column_names()
        istaxo = (not "taxo" in mongodb_collections_names)
        isinvtaxo = (not "invtaxo" in mongodb_collections_names)
        isvorhaben = (not "vorhaben" in mongodb_collections_names)
        isvorhaben_inv = (not "vorhaben_inv" in mongodb_collections_names)
        ispattern = (not "pattern" in mongodb_collections_names)
        isbadlist = (not "badlist" in mongodb_collections_names)

        self.mongo_export(mongodb_utils_filepath, hida_name, metadata_name, json_folderpath)

        if "hida" not in mongodb_collections_names:
            mongodb_collections_names["hida"] = hida_name
            self.mongo_export(mongodb_utils_filepath, hida_name, metadata_name,
                                           json_folderpath)

        hida = self.mongodb_api_obj["hida"]
        support = self.mongodb_api_obj["support"]

        metadata = self.mongodb_api_obj[metadataname]
        extractText(name, path, metadata, tika, 100000, False)
        initSupport(support, hida, district)

        findAddresses(metadata, support, "de")
        folders = self.mongodb_api_obj[folders]
        folderAddress(folders, hida, path, support, "de", district)
        findMonuments(metadata, hida, support, folders, "de", district)
        mongodb_settingup.mongo_export(metadataname=metadataname, ismetadatahida=True)

        if not "doctypes" in mongodb_collections_names:
            doctypes = self.mongodb_api_obj["doctypes"]
            initDocumentPattern(doctypes)
        findDocType(metadata, doctypes)
        findDates(metadata)
        findProject(metadata)

        vorhabeninv_col = self.mongodb_api_obj["vorhaben_inv"]
        pattern_col = self.mongodb_api_obj["pattern"]
        badlist_col = self.mongodb_api_obj["badlist"]
        all_col = self.mongodb_api_obj["emblist"]
        no_col = self.mongodb_api_obj["noemblist"]
        extractintents(metadata, vorhabeninv_col, pattern_col,
                       badlist_col, all_col, no_col)
        self.mongo_export(metadataname=metadataname, ismetadatakeywords=True)