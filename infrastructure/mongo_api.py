import json
import logging as log
import os
import random

from pymongo.collection import Collection
from pymongo import MongoClient

log.basicConfig(
    filename='app.log',
    filemode='w',
    level=log.DEBUG,
    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s'
)


class MongoAPI:
    def __init__(self, mongodb_api_client: MongoClient, data: dict) -> None:
        self.client = mongodb_api_client

        database = data['database']
        collection = data['collection']
        self.cursor = self.client[database] # corresponding to "mydb" variable of export2mongodb.py
        self.collection = self.cursor[collection]
        self.data = data

    def read(self) -> list:
        '''
        Read data from database
        :return: A list of recovered data
        '''

        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data: dict) -> dict:
        '''
        Insert an element into the database
        :param data: new data that will be inserted into the database
        :return: data inserted
        '''

        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self) -> dict:
        '''
        Edit data into the database
        :return: the new data value
        '''

        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data: dict) -> dict:
        '''
        Removes an element from the database
        :param data: element that will be removed
        :return: removed element
        '''

        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def get_column_names(self) -> list:
        return self.cursor.list_collection_names() # Value of variable "collist" in line 37 of export2mongodb.py

    def mongo_export(self, mongodb_utils_filepath: str, hida_name: str, metadata_name: str, json_folderpath: str) -> None:
        '''
        Function corresponding to "mongoExport" of file export2mongodb
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
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["pattern"]), "pattern")

        if mongodb_column_dict.get("ishida", False):
            self.patch_hida(os.path.join(os.path.join(json_folderpath, mongodb_files_dict["hida"])), hidaname)

        if mongodb_column_dict.get("isresolved", False):
            self.patch_resolved(metadataname, os.path.join(json_folderpath, mongodb_files_dict["resolved"]), hidaname)

        if mongodb_column_dict.get("ismetadatahida", False):
            self.project_metadata_hida(metadataname, hidaname)

        if mongodb_column_dict.get("isfolders", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["files"]), "folders")
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["koepnick_files"]), "koepnick_folders")

        if mongodb_column_dict.get("isbadlist", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["badlist"]), "badlist")

        if mongodb_column_dict.get("isvorhaben", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["vorhaben"]), "vorhaben")

        if mongodb_column_dict.get("isvorhabeninv", False):
            self.load_dict_collection(os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"]), "vorhaben_inv")

        if mongodb_column_dict.get("istaxo", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["taxo"]), "taxo")

        if mongodb_column_dict.get("istopics", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["topics3a"]), "topics")

        if mongodb_column_dict.get("ispatch_dir", False) or mongodb_column_dict.get("isresolved", False):
            self.patch_dir(metadataname, "folders", r"C:\Data\test\KIbarDok") # TODO: Ask what is the use of this file or folder

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("istopics", False) or \
                mongodb_column_dict.get("iskeywords", False):
            self.patch_keywords(metadataname, "topics")

        if mongodb_column_dict.get("ismetadatakeywords", False):
            self.project_metadata_keywords(metadataname)

        if mongodb_column_dict.get("ismetadatanokeywords", False):
            self.unproject_metadata_keywords(metadataname)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatehida", False):
            self.project_hida(metadataname)

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatevorhaben", False):
            self.patch_vorhaben(metadataname)

        if mongodb_column_dict.get("iscategories", False) or mongodb_column_dict.get("isvorhabeninv", False):
            self.patch_categories(os.path.join(json_folderpath, mongodb_files_dict["vorhaben_inv"]), "categories")

        if mongodb_column_dict.get("isemblist", False):
            self.load_embddings(os.path.join(json_folderpath, mongodb_files_dict["all_matches"]), "emblist")

        if mongodb_column_dict.get("isnoemblist", False):
            self.load_no_matches(os.path.join(json_folderpath, mongodb_files_dict["no_matches"]), "noemblist")

        if mongodb_column_dict.get("isinvtaxo", False):
            self.load_array_collection(os.path.join(json_folderpath, mongodb_files_dict["taxo_inv"]), "invtaxo")

        if mongodb_column_dict.get("isresolved", False) or mongodb_column_dict.get("isupdatetaxo", False) or \
                mongodb_column_dict.get("ismetadatahida", False):
            self.patch_inv_taxo(metadataname, "invtaxo")

        if mongodb_column_dict.get("ishida", False) or mongodb_column_dict.get("isupdatehidataxo", False):
            self.project_hida_inv_taxo(hidaname, "invtaxo")

    def load_array_collection(self, filename: str, colname: str):
        '''
        The same as "loadArrayCollection" from export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        col: Collection = self.cursor[colname]
        with open(filename, encoding='utf-8') as f:
            items = json.loads(f.read())
        col.delete_many({})
        col.insert_many(items)

    def patch_hida(self, filename: str, hidaname: str):
        '''
        The same as "patchHida" on export2mongodb.py file
        :param hidaname:
        :return:
        '''
        with open(filename, encoding='utf-8') as f:
            hida0: dict = json.loads(f.read())
            monuments = []
            for hid in hida0:
                monument = hida0[hid]
                # if "K-Begründung" in monument:
                #     del monument["K-Begründung"]
                if "AdresseDict" in monument:
                    adict = monument["AdresseDict"]
                    keys = [x for x in adict]
                    for str in keys:
                        if "." in str:
                            str2 = str.replace(".", "")
                            adict[str2] = adict[str]
                            del adict[str]
                            continue
                monuments.append(monument)
            hida_col = self.cursor[hidaname]
            hida_col.delete_many({})
            hida_col.insert_many(monuments)

    def patch_resolved(self, resolvedname: str, filename: str, hidaname: str):
        '''
        The same as "patchResolved" on export2mongodb.py file
        :param filename:
        :param hidaname:
        :return:
        '''
        hida_col = self.cursor[hidaname]
        resolved_col = self.cursor[resolvedname]
        with open(filename, encoding='utf-8') as f:
            resolvedjs = json.loads(f.read())
            resolved = []
            for directory in resolvedjs:
                el = resolvedjs[directory]
                if "datei" in el:
                    filesjs = el["datei"]
                    for file in filesjs:
                        obj = filesjs[file]
                        vorhaben = obj["vorhaben"]
                        if len(vorhaben) == 1:
                            if vorhaben[0] == "Errichtung einer Mega-Light-Werbeanlage":
                                vorhaben = []
                        vorgang = obj["vorgang"]
                        objnr = obj["objnr"]
                        hida = {}
                        if "method" in objnr:
                            meth = objnr["method"]
                            if len(meth) > 0:
                                for o in objnr:
                                    if o != "method" and o != "behoerde" and o != "hausnummer":
                                        if meth == 'inhalt_direct' and o == "treffer":
                                            treflist = objnr["treffer"][meth]
                                            tref = treflist[0]
                                            hidaid = tref[0]
                                            hidaobj = hida_col.find_one(
                                                {"OBJ-Dok-Nr": hidaid})
                                            listentext = hidaobj["Listentext"]
                                            denkmalname = hidaobj["Denkmalname"]
                                            denkmalart = hidaobj["Denkmalart"]
                                            sachbegriff = hidaobj["Sachbegriff"]
                                            hida[hidaid] = {
                                                "hidaid": hidaid,
                                                "Listentext": listentext,
                                                "Denkmalart": denkmalart,
                                                "Denkmalname": denkmalname,
                                                "Sachbegriff": sachbegriff}
                                        else:
                                            denkmal = objnr[o]
                                            for hidaobj in denkmal["treffer"][meth]:
                                                hidaid = hidaobj[0]
                                                hidaobj = hida_col.find_one(
                                                    {"OBJ-Dok-Nr": hidaid})
                                                listentext = hidaobj["Listentext"]
                                                denkmalname = hidaobj["Denkmalname"]
                                                denkmalart = hidaobj["Denkmalart"]
                                                sachbegriff = hidaobj["Sachbegriff"]
                                                hida[hidaid] = {
                                                    "hidaid": hidaid,
                                                    "Listentext": listentext,
                                                    "Denkmalart": denkmalart,
                                                    "Denkmalname": denkmalname,
                                                    "Sachbegriff": sachbegriff}

                        resolved.append({"file": file, "dir": directory,
                                         "vorgang": vorgang,
                                         "vorhaben": vorhaben,
                                         "hida": hida,
                                         "obj": obj})
            resolved_col.delete_many({})
            resolved_col.insert_many(resolved)
            # print(resolved)

    def project_metadata_hida(self, metadataname: str, hidaname: str):
        '''
        The same as "projectMetaDataHida" on export2mongodb.py
        :param metadataname:
        :param hidaname:
        :return:
        '''
        hida_col = self.cursor[hidaname]
        metadata_col = self.cursor[metadataname]
        for doc in metadata_col.find():
            if "hidas" in doc:
                hida = {}
                sachbegriff = set([])
                denkmalart = set([])
                denkmalname = set([])
                for hidaid in doc["hidas"]:
                    hidaobj = hida_col.find_one(
                        {"OBJ-Dok-Nr": hidaid})
                    if not hidaobj:
                        hidaobj = hida_col.find_one(
                            {"Teil-Obj-Dok-Nr": hidaid})
                    if "Denkmalname" in hidaobj:
                        s = hidaobj["Denkmalname"]
                        denkmalname.update(s)

                    if "Denkmalart" in hidaobj:
                        s: str = hidaobj["Denkmalart"]
                        denkmalart.add(s)

                    sachbegriffh = hidaobj["Sachbegriff"]
                    sachbegriff.update(sachbegriffh)

                    hida[hidaid] = hidaobj
                metadata_col.update_one(
                    {"_id": doc["_id"]}, {
                        "$set": {
                            # "hida": hida,
                            "Sachbegriff": list(sachbegriff),
                            "Denkmalart": list(denkmalart),
                            "Denkmalname": list(denkmalname)}
                    })
            else:
                # hida = {}
                sachbegriff = set([])
                denkmalart = set([])
                denkmalname = set([])
                metadata_col.update_one(
                    {"_id": doc["_id"]}, {
                        "$set": {
                            # "hida": hida,
                            "Sachbegriff": list(sachbegriff),
                            "Denkmalart": list(denkmalart),
                            "Denkmalname": list(denkmalname)}
                    })

    def load_dict_collection(self, filename: str, colname: str):
        '''
        The same as "loadDictCollection" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        col: Collection = self.cursor[colname]
        item: any = {}
        with open(filename, encoding='utf-8') as f:
            item = json.loads(f.read())
        col.delete_many({})
        col.insert_one(item)

    def patch_dir(self, resolvedname: str, folders: str, path: str):
        '''
        The same as "patchDir" on export2mongodb.py
        :param resolvedname:
        :param folders:
        :param path:
        :return:
        '''
        folders_col = self.cursor[folders]
        resolved_col = self.cursor[resolvedname]
        for folder in folders_col.find():
            for file in folder["files"]:
                dir = folder["dir"]
                dir = dir.replace(path, "")
                f = file
                if f.endswith(".doc"):
                    f = f.replace(".doc", ".docx")
                if f.endswith(".docx"):
                    print(dir, f)
                    resolved_col.update_many(
                        {"file": f}, {"$set": {"dir": dir}})

    def patch_keywords(self, resolvedname: str, topicsname: str):
        '''
        The same as "patchKeywords" on export2mongodb.py
        :param resolvedname:
        :param topicsname:
        :return:
        '''
        topics_col = self.cursor[topicsname]
        resolved_col = self.cursor[resolvedname]
        for topic in topics_col.find():
            # print(topic["file"])
            hidas = []
            sachbegriff = []
            denkmalart = []
            denkmalname = []
            if "hida" in topic:
                for hida0 in topic["hida"]:
                    hidas.append(hida0)
                    # ????? weder hidas noch die attributaggregation wird weiter verwendet....
                    sachbegriff += hida0["Sachbegriff"]
                    denkmalart += hida0["Denkmalart"]
                    denkmalname += hida0["Denkmalname"]

            for theme in topic["keywords"]:
                resolved_col.update_many(
                    {"file": topic["file"]}, {"$set": {
                        theme: topic["keywords"][theme]
                    }})

    def project_metadata_keywords(self, metadataname: str):
        '''
        The same as "patchMetaDataKeywords" on export2mongodb.py
        :param metadataname:
        :return:
        '''
        col = self.cursor[metadataname]
        for doc in col.find():
            if "topic" in doc:
                topic = doc["topic"]
                for theme in topic["keywords"]:
                    col.update_many(
                        {"_id": doc["_id"]}, {"$set": {
                            theme: topic["keywords"][theme]
                        }})

    def unproject_metadata_keywords(self, metadataname: str):
        '''
        The same as "unprojectMetaDataKeywords" on export2mongodb.py
        :param metadataname:
        :return:
        '''
        col = self.cursor[metadataname]
        for doc in col.find():
            if "topic" in doc:
                topic = doc["topic"]
                for theme in topic["keywords"]:
                    col.update_one({"_id": doc["_id"]}, {"$unset": {theme: None}})

    def project_hida(self, resolvedname: str):
        '''
        The same as "projectHida" on export2mongodb.py
        :param resolvedname:
        :return:
        '''
        resolved_col = self.cursor[resolvedname]
        for reso0 in resolved_col.find():
            print(reso0["file"])
            hidas = []
            sachbegriff = []
            denkmalart = []
            denkmalname = []
            if "hida" in reso0:
                for hida0 in reso0["hida"]:
                    hidas.append(hida0)
                    if reso0["hida"][hida0]["Sachbegriff"]:
                        sachbegriff += reso0["hida"][hida0]["Sachbegriff"]
                    if reso0["hida"][hida0]["Denkmalart"]:
                        denkmalart.append(reso0["hida"][hida0]["Denkmalart"])
                    if reso0["hida"][hida0]["Denkmalname"]:
                        denkmalname += reso0["hida"][hida0]["Denkmalname"]
                resolved_col.update_one(
                    {"file": reso0["file"]}, {
                        "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                                 "Denkmalart": list(set(denkmalart)),
                                 "Denkmalname": list(set(denkmalname))}
                    })

    def patch_vorhaben(self, resolvedname: str):
        '''
        The same as "patchVorhaben" on export2mongodb.py
        :param resolvedname:
        :return:
        '''
        resolved_col = self.cursor[resolvedname]
        for reso1 in resolved_col.find():
            if "vorhaben" in reso1 and len(reso1["vorhaben"]) == 1 and \
                    reso1["vorhaben"][0] == 'Errichtung einer Mega-Light-Werbeanlage':
                print(reso1["file"])
                resolved_col.update_one(
                    {"file": reso1["file"]}, {
                        "$set": {"vorhaben": []}
                    })

    def patch_categories(self, words: str, categoriesname: str):
        '''
        The same as "patchCategories" on export2mongodb.py
        :param words:
        :param categoriesname:
        :return:
        '''
        collist = self.get_column_names()
        categories = []
        if words in collist:
            vorhabeninv_col = self.cursor[words]
            vorhabeninv = vorhabeninv_col.find()
            for v in vorhabeninv:
                for wor in v["words"]:
                    if len(v["words"][wor]) == 0:
                        categories.append(wor)
        catcolors = {}
        color = self.color_generator(len(categories))
        for i in range(len(categories)):
            catcolors[categories[i]] = {
                "color": color[i], "label": categories[i].upper()}

        cat_col = self.cursor[categoriesname]
        cat_col.delete_many({})
        cat_col.insert_one(catcolors)

    def load_embddings(self, filename: str, colname: str):
        '''
        The same as "loadEmbddings" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        col: Collection = self.cursor[colname]
        items: any = []
        with open(filename, encoding='utf-8') as f:
            mlist = json.loads(f.read())
            for m in mlist:
                items.append({"word": m, "match": mlist[m], "correct": True})
        col.delete_many({})
        col.insert_many(items)

    def load_no_matches(self, filename: str, colname: str):
        '''
        The same as "loadNoMatches" on export2mongodb.py
        :param filename:
        :param colname:
        :return:
        '''
        col: Collection = self.cursor[colname]
        items: any = []
        with open(filename, encoding='utf-8') as f:
            mlist = json.loads(f.read())
            for m in mlist:
                items.append({"word": m, "count": mlist[m]})
        col.delete_many({})
        col.insert_many(items)

    def patch_inv_taxo(self, resolvedname: str, invtaxo: str):
        '''
        The same as "patchInvTaxo" on export2mongodb.py
        :param resolvedname:
        :param invtaxo:
        :return:
        '''
        resolved_col = self.cursor[resolvedname]
        resol = resolved_col.find()
        for reso2 in resol:
            invtaxo_col = self.cursor[invtaxo]
            sblist = []
            if "Sachbegriff" in reso2:
                sblist = reso2["Sachbegriff"]
            if len(sblist) > 0:
                sl = sblist
                for sb in sblist:
                    for plist in invtaxo_col.find({"name": sb}):
                        for pa in plist["parents"]:
                            if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                                sl.append(pa)
                resolved_col.update_one({"_id": reso2["_id"]}, {
                    "$set": {"Sachbegriff": sl}})

    def project_hida_inv_taxo(self, hidaname: str, invtaxo: str):
        '''
        The same as "projectHidaInvTaxo" on export2mongodb.py
        :param hidaname:
        :param invtaxo:
        :return:
        '''
        hida_col = self.cursor[hidaname]
        invtaxo_col = self.cursor[invtaxo]
        hidal = hida_col.find()
        for hida in hidal:
            invtaxo_col = self.cursor["invtaxo"]
            sblist = hida["Sachbegriff"]
            if len(sblist) > 0:
                sl = sblist
                for sb in sblist:
                    for plist in invtaxo_col.find({"name": sb}):
                        for pa in plist["parents"]:
                            if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                                sl.append(pa)
                hida_col.update_one({"_id": hida["_id"]}, {
                    "$set": {"Sachbegriff": sl}})

    def color_generator(self, number_of_colors):
        # TODO: Check whether this function should be here
        '''
        The same as "color_generator" on export2mongodb.py
        :param number_of_colors:
        :return:
        '''
        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        return color