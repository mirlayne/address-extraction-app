import json
import os

from entities.mongo_api_interface import MongoAPIInterface as IMongoAPI
from entities.mongodb_collections_preprocess_interface import MongoDBCollectionsPreprocessInterface \
    as IMongoDBCollectionsPreprocess


class MongoDBSettingUpService:
    def mongo_export(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
        '''
        Function corresponding to "mongoExport" on file export2mongodb.py
        :param mongodb_utils_filepath: json file that stores the necessary data such as column names and utils json file names
        :param hida_name: name of hida file
        :param metadata_name: name of metadata
        :param json_folderpath: folder where are stored the json files
        :return:
        '''
        with open(mongodb_utils_filepath, 'r') as mongodb_file:
            mongodb_dict = json.load(mongodb_file)

        mongodb_column_dict = mongodb_dict["columns"]
        mongodb_files_dict = mongodb_dict["json_files"]

        hidaname = hida_name
        metadataname = metadata_name

        if mongodb_column_dict.get("ispattern", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["pattern"]), "pattern")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("ishida", False):
            data = IMongoDBCollectionsPreprocess.patch_hida(os.path.join(os.path.join(json_folderpath, mongodb_files_dict["hida"])), hidaname)
            IMongoAPI.update_collection(hidaname, data)

        if mongodb_column_dict.get("isresolved", False):
            data = IMongoDBCollectionsPreprocess.patch_resolved(metadataname, os.path.join(json_folderpath, mongodb_files_dict["resolved"]), hidaname)
            IMongoAPI.update_collection(hidaname, data)

        if mongodb_column_dict.get("ismetadatahida", False):
            data_gen = IMongoDBCollectionsPreprocess.project_metadata_hida(metadataname, hidaname)
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isfolders", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["files"]), "folders")
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["koepnick_files"]), "koepnick_folders")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isbadlist", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["badlist"]), "badlist")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isvorhaben", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["vorhaben"]), "vorhaben")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isvorhabeninv", False):
            data = IMongoDBCollectionsPreprocess.load_dict_collection(os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"]), "vorhaben_inv")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("istaxo", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["taxo"]), "taxo")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("istopics", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["topics3a"]), "topics")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("ispatch_dir", False) or mongodb_column_dict.get("isresolved", False):
            data_gen = IMongoDBCollectionsPreprocess.patch_dir(metadataname, "folders", r"C:\Data\test\KIbarDok") # TODO: Ask what the use of this file or folder is
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("istopics", False) or \
                mongodb_column_dict.get("iskeywords", False):
            data_gen = IMongoDBCollectionsPreprocess.patch_keywords(metadataname, "topics")
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ismetadatakeywords", False):
            data_gen = IMongoDBCollectionsPreprocess.project_metadata_keywords(metadataname)
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ismetadatanokeywords", False):
            data_gen = IMongoDBCollectionsPreprocess.unproject_metadata_keywords(metadataname)
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatehida", False):
            data_gen = IMongoDBCollectionsPreprocess.project_hida(metadataname)
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatevorhaben", False):
            data_gen = IMongoDBCollectionsPreprocess.patch_vorhaben(metadataname)
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("iscategories", False) or mongodb_column_dict.get("isvorhabeninv", False):
            data = IMongoDBCollectionsPreprocess.patch_categories(os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"]), "categories")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isemblist", False):
            data = IMongoDBCollectionsPreprocess.load_embddings(os.path.join(json_folderpath, mongodb_files_dict["all_matches"]), "emblist")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isnoemblist", False):
            data = IMongoDBCollectionsPreprocess.load_no_matches(os.path.join(json_folderpath, mongodb_files_dict["no_matches"]), "noemblist")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isinvtaxo", False):
            data = IMongoDBCollectionsPreprocess.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["taxo_inv"]), "invtaxo")
            IMongoAPI.update_collection("pattern", data)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatetaxo", False) or \
                mongodb_column_dict.get("ismetadatahida", False):
            data_gen = IMongoDBCollectionsPreprocess.patch_inv_taxo(metadataname, "invtaxo")
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break

        if mongodb_column_dict.get("ishida", False) or mongodb_column_dict.get("isupdatehidataxo", False):
            data_gen = IMongoDBCollectionsPreprocess.project_hida_inv_taxo(hidaname, "invtaxo")
            while True:
                try:
                    data = next(data_gen)
                    IMongoAPI.update("pattern", data)
                except StopIteration:
                    break
