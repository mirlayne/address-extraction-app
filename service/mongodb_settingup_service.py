import json
import os

from entities.mongodb_api_interface import MongoAPIInterface as IMongoAPI
from entities.mongodb_collections_preprocess_interface import MongoDBCollectionsPreprocessInterface \
    as IMongoDBCollectionsPreprocess


class MongoDBSettingUpService:

    def __init__(self, mongodb_api_obj: IMongoAPI):
        self.mongodb_api_obj = mongodb_api_obj

    def mongo_export(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
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

        mongodb_api_obj = IMongoAPI()

        if mongodb_column_dict.get("ispattern", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["pattern"])
            mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "pattern"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isfolders", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["files"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "folders"
            mongodb_api_obj.insert_in_collection(data)

            json_path = os.path.join(json_folderpath, mongodb_files_dict["koepnick_files"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "koepnick_folders"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isbadlist", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["badlist"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "badlist"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isvorhaben", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["vorhaben"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "vorhaben"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("istopics", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["topics3a"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "topics"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isvorhabeninv", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "vorhaben_inv"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("istaxo", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["taxo"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "taxo"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isinvtaxo", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["taxo_inv"])
            data = mongodb_col_preproc.load_array_collection(json_path)
            mongodb_api_obj.collection = "invtaxo"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isemblist", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["all_matches"])
            data = mongodb_col_preproc.load_embeddings(json_path)
            mongodb_api_obj.collection = "emblist"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isnoemblist", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["no_matches"])
            data = mongodb_col_preproc.load_no_matches(json_path)
            mongodb_api_obj.collection = "noemblist"
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("ishida", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["hida"])
            data = mongodb_col_preproc.patch_hida(json_path)
            mongodb_api_obj.collection = hidaname
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("isresolved", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["resolved"])
            data = mongodb_col_preproc.patch_resolved(json_path, hida_col_dict)
            mongodb_api_obj.collection = metadataname
            mongodb_api_obj.insert_in_collection(data)

        if mongodb_column_dict.get("iscategories", False) or mongodb_column_dict.get("isvorhabeninv", False):
            json_path = os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"])
            data = mongodb_col_preproc.patch_categories(json_path)
            mongodb_api_obj.collection = "categories"
            mongodb_api_obj.write(data)

        if mongodb_column_dict.get("ismetadatahida", False):
            data_gen = mongodb_col_preproc.project_metadata_hida(metadata_col_obj, hida_col_dict)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ispatch_dir", False) or mongodb_column_dict.get("isresolved", False):
            mongodb_api_obj.collection = "folders"
            folders_coll = mongodb_api_obj.read()
            data_gen = mongodb_col_preproc.patch_dir(folders_coll, r"C:\Data\test\KIbarDok")  # TODO: Ask what the use of this file or folder is
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("istopics", False) or \
                mongodb_column_dict.get("iskeywords", False):
            data_gen = mongodb_col_preproc.patch_keywords(metadata_col_obj)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ismetadatakeywords", False):
            data_gen = mongodb_col_preproc.project_metadata_keywords(metadata_col_obj)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ismetadatanokeywords", False):
            data_gen = mongodb_col_preproc.unproject_metadata_keywords(metadata_col_obj)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatehida", False):
            data_gen = mongodb_col_preproc.project_hida(metadata_col_obj)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatevorhaben", False):
            data_gen = mongodb_col_preproc.patch_vorhaben(metadata_col_obj)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatetaxo", False) or \
                mongodb_column_dict.get("ismetadatahida", False):
            mongodb_api_obj.collection = "invtaxo"
            invtaxo_list = mongodb_api_obj.read()
            data_gen = mongodb_col_preproc.patch_inv_taxo(metadata_col_obj, invtaxo_list)
            mongodb_api_obj.collection = metadataname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ishida", False) or mongodb_column_dict.get("isupdatehidataxo", False):
            mongodb_api_obj.collection = "invtaxo"
            invtaxo_list = mongodb_api_obj.read()
            data_gen = mongodb_col_preproc.project_hida_inv_taxo(hida_col_dict, invtaxo_list)
            mongodb_api_obj.collection = hidaname
            while True:
                try:
                    data = next(data_gen)
                    mongodb_api_obj.update(data)
                except StopIteration:
                    break

    def create_fill_collection(self, collection_name: str, collection_function: any, **function_args) -> None:
        def wrapper():
            data = collection_function(function_args)
            self.mongodb_api_obj.collection = collection_name
            self.mongodb_api_obj.insert_in_collection(data)
        return wrapper

    def extract_metadata(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
        metadataname = metadata_name

        mongodb_api = IMongoAPI()
        with open(mongodb_utils_filepath, 'r') as mongodb_file:
            mongodb_dict = json.load(mongodb_file)

        mongodb_columns_names = mongodb_api.get_column_names()
        # istaxo = (not "taxo" in mongodb_column_dict)
        # isinvtaxo = (not "invtaxo" in mongodb_column_dict)
        # isvorhaben = (not "vorhaben" in mongodb_column_dict)
        # isvorhaben_inv = (not "vorhaben_inv" in mongodb_column_dict)
        # ispattern = (not "pattern" in mongodb_column_dict)
        # isbadlist = (not "badlist" in mongodb_column_dict)

        self.mongo_export(mongodb_utils_filepath, hida_name, metadata_name, json_folderpath)

        if "hida" not in mongodb_columns_names:
            mongodb_column_dict["hida"] = hida_name
            self.mongo_export(mongodb_utils_filepath, hida_name, metadata_name,
                                           json_folderpath)

        hida = mydb["hida"]
        support = mydb["support"]

        metadata = mydb[metadataname]
        extractText(name, path, metadata, tika, 100000, False)
        initSupport(support, hida, district)

        findAddresses(metadata, support, "de")
        folders = mydb[folders]
        folderAddress(folders, hida, path, support, "de", district)
        findMonuments(metadata, hida, support, folders, "de", district)
        mongodb_settingup.mongo_export(metadataname=metadataname, ismetadatahida=True)

        if not "doctypes" in collist:
            doctypes = mydb["doctypes"]
            initDocumentPattern(doctypes)
        findDocType(metadata, doctypes)
        findDates(metadata)
        findProject(metadata)

        vorhabeninv_col = mydb["vorhaben_inv"]
        pattern_col = mydb["pattern"]
        badlist_col = mydb["badlist"]
        all_col = mydb["emblist"]
        no_col = mydb["noemblist"]
        extractintents(metadata, vorhabeninv_col, pattern_col,
                       badlist_col, all_col, no_col)
        mongodb_settingup.mongo_export(metadataname=metadataname, ismetadatakeywords=True)