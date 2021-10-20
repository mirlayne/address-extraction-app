import json
import random
from typing import Iterator

from entities.mongodb_api_interface import MongoAPIInterface as MongoAPIInterface
from entities.mongodb_collections_preprocess_interface import MongoDBCollectionsPreprocessInterface \
    as IMongoDBCollectionsPreprocess


class MongoDBCollectionsPreprocess(IMongoDBCollectionsPreprocess):
    def __init__(self, mongo_api: MongoAPIInterface):
        self.mongo_api = mongo_api

    def load_array_collection(self, filename: str) -> dict:
        '''
        The same as "loadArrayCollection" on export2mongodb.py
        :param filename:
        :return:
        '''

        with open(filename, encoding='utf-8') as f:
            items = json.loads(f.read())
            return items

    def patch_hida(self, filename: str) -> list:
        '''
        The same as "patchHida" on export2mongodb.py file
        :param filename:
        :return:
        '''
        with open(filename, encoding='utf-8') as f:
            hida0: dict = json.loads(f.read())
            monuments = []
            for hid in hida0:
                monument = hida0[hid]
                if "AdresseDict" in monument:
                    adict = monument["AdresseDict"]
                    keys = adict.keys()
                    for str_k in keys:
                        if "." in str_k:
                            str2 = str_k.replace(".", "")
                            adict[str2] = adict[str_k]
                            del adict[str_k]
                            continue
                monuments.append(monument)
            return monuments

    def patch_resolved(self, filename: str, hida_col: list) -> list:
        # TODO: check the part find_one function
        '''
        The same as "patchResolved" on export2mongodb.py file
        :param filename:
        :param hida_col: dictionary from the collection "hida"
        :return:
        '''

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
                                            hidaobj = self._find_one(hida_col, {"OBJ-Dok-Nr": hidaid})
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
                                                hidaobj = self._find_one(hida_col, {"OBJ-Dok-Nr": hidaid})
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
            return resolved

    def project_metadata_hida(self, metadata_col: list, hida_col: list) -> Iterator[dict]:
        '''
        The same as "projectMetaDataHida" on export2mongodb.py
        :param metadata_col:
        :param hida_col:
        :return:
        '''

        for doc in metadata_col:
            if "hidas" in doc:
                hida = {}
                sachbegriff = set([])
                denkmalart = set([])
                denkmalname = set([])
                for hidaid in doc["hidas"]:
                    hidaobj = self._find_one(hida_col, {"OBJ-Dok-Nr": hidaid})
                    if not hidaobj:
                        hidaobj = self._find_one(hida_col, {"Teil-Obj-Dok-Nr": hidaid})
                    if "Denkmalname" in hidaobj:
                        s = hidaobj["Denkmalname"]
                        denkmalname.update(s)

                    if "Denkmalart" in hidaobj:
                        s: str = hidaobj["Denkmalart"]
                        denkmalart.add(s)

                    sachbegriffh = hidaobj["Sachbegriff"]
                    sachbegriff.update(sachbegriffh)

                    hida[hidaid] = hidaobj
                    yield {"_id": doc["_id"],
                            "$set": {
                                "Sachbegriff": list(sachbegriff),
                                "Denkmalart": list(denkmalart),
                                "Denkmalname": list(denkmalname)}
                        }
                    # TODO: remove the comments
                    # metadata_col.update_one(
                    # {"_id": doc["_id"]}, {
                    #     "$set": {
                    #         "Sachbegriff": list(sachbegriff),
                    #         "Denkmalart": list(denkmalart),
                    #         "Denkmalname": list(denkmalname)}
                    # })
            else:
                sachbegriff = set([])
                denkmalart = set([])
                denkmalname = set([])
                yield {"_id": doc["_id"],
                        "$set": {
                            "Sachbegriff": list(sachbegriff),
                            "Denkmalart": list(denkmalart),
                            "Denkmalname": list(denkmalname)}
                    }
                # TODO: remove the comments
                # metadata_col.update_one(
                #     {"_id": doc["_id"]}, {
                #         "$set": {
                #             "Sachbegriff": list(sachbegriff),
                #             "Denkmalart": list(denkmalart),
                #             "Denkmalname": list(denkmalname)}
                #     })

    def load_dict_collection(self, filename: str) -> dict:
        '''
        The same as "loadDictCollection" on export2mongodb.py
        :param filename:
        :return:
        '''

        with open(filename, encoding='utf-8') as f:
            item = json.loads(f.read())
        return item

    def patch_dir(self, folders_dict: list, path: str) -> Iterator[dict]:
        '''
        The same as "patchDir" on export2mongodb.py
        :param folders_dict: all the documents of the collection
        :param path:
        :return:
        '''

        for folder in folders_dict:
            for file in folder["files"]:
                dir = folder["dir"]
                dir = dir.replace(path, "")
                f = file
                if f.endswith(".doc"):
                    f = f.replace(".doc", ".docx")
                if f.endswith(".docx"):
                    print(dir, f)
                    yield {"file": f, "$set": {"dir": dir}}
                    # TODO: remove the comments
                    # resolved_col.update_many(
                    #     {"file": f}, {"$set": {"dir": dir}})

    def patch_keywords(self, topics_dict: list) -> Iterator[dict]:
        '''
        The same as "patchKeywords" on export2mongodb.py
        :param topics_dict: all the documents of the collection
        :return:
        '''

        for topic in topics_dict:
            for theme in topic["keywords"]:
                yield {"file": topic["file"], "$set": {
                        theme: topic["keywords"][theme]
                    }}
                # TODO: remove the comments
                # resolved_col.update_many(
                    # {"file": topic["file"]}, {"$set": {
                    #     theme: topic["keywords"][theme]
                    # }})

    def project_metadata_keywords(self, collection_dict: list) -> Iterator[dict]:
        '''
        The same as "patchMetaDataKeywords" on export2mongodb.py
        :param collection_dict: all the documents of the collection
        :return:
        '''

        for doc in collection_dict:
            if "topic" in doc:
                topic = doc["topic"]
                for theme in topic["keywords"]:
                    yield {"_id": doc["_id"], "$set": {
                             theme: topic["keywords"][theme]
                         }}
                    # TODO: remove comment when will be tested and OK
                    # col.update_many(
                    #     {"_id": doc["_id"]}, {"$set": {
                    #         theme: topic["keywords"][theme]
                    #     }})

    def unproject_metadata_keywords(self, collection_dict: list) -> Iterator[dict]:
        '''
        The same as "unprojectMetaDataKeywords" on export2mongodb.py
        :param collection_dict: all the documents of the collection
        :return:
        '''

        for doc in collection_dict:
            if "topic" in doc:
                topic = doc["topic"]
                for theme in topic["keywords"]:
                    yield {"_id": doc["_id"], "$unset": {theme: None}}
                    # TODO: remove comment when will be tested and OK
                    # col.update_one({"_id": doc["_id"]}, {"$unset": {theme: None}})

    def project_hida(self, resolved_dict: list) -> Iterator[dict]:
        '''
        The same as "projectHida" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :return:
        '''

        for reso0 in resolved_dict:
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
                yield {"file": reso0["file"],
                       "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                                "Denkmalart": list(set(denkmalart)),
                                "Denkmalname": list(set(denkmalname))}
                       }
                # TODO: remove comment when will be tested and OK
                # resolved_col.update_one(
                #     {"file": reso0["file"]}, {
                #         "$set": {"hidas": hidas, "Sachbegriff": list(set(sachbegriff)),
                #                  "Denkmalart": list(set(denkmalart)),
                #                  "Denkmalname": list(set(denkmalname))}
                #     })

    def patch_vorhaben(self, resolved_dict: list) -> Iterator[dict]:
        '''
        The same as "patchVorhaben" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :return:
        '''

        for reso1 in resolved_dict:
            if "vorhaben" in reso1 and len(reso1["vorhaben"]) == 1 and \
                    reso1["vorhaben"][0] == 'Errichtung einer Mega-Light-Werbeanlage':
                print(reso1["file"])
                yield {"file": reso1["file"],
                        "$set": {"vorhaben": []}
                    }
                # TODO: remove comment when will be tested and OK
                # resolved_col.update_one(
                #     {"file": reso1["file"]}, {
                #         "$set": {"vorhaben": []}
                #     })

    def patch_categories(self, vorhabeninv_dict: list) -> list:
        '''
        The same as "patchCategories" on export2mongodb.py
        :param vorhabeninv_dict: all the documents of the collection
        :return:
        '''

        categories = []
        # collist = self.get_column_names()
        # if words in collist: # TODO: this condition must be made in the function that will call this function

        for v in vorhabeninv_dict:
            for wor in v["words"]:
                if not len(v["words"][wor]):
                    categories.append(wor)
        catcolors = {}
        color = self.color_generator(len(categories))
        for idx, elem in enumerate(categories):
            catcolors[elem] = {
                "color": color[idx], "label": elem.upper()}

        return categories
        # cat_col = self.cursor[categoriesname]
        # cat_col.delete_many({})
        # cat_col.insert_one(catcolors)

    def load_embddings(self, filename: str) -> list:
        '''
        The same as "loadEmbddings" on export2mongodb.py
        :param filename:
        :return:
        '''

        items: any = []
        with open(filename, encoding='utf-8') as f:
            mlist = json.loads(f.read())
            for m in mlist:
                items.append({"word": m, "match": mlist[m], "correct": True})
        return items

    def load_no_matches(self, filename: str) -> list:
        '''
        The same as "loadNoMatches" on export2mongodb.py
        :param filename:
        :return:
        '''
        items: any = []
        with open(filename, encoding='utf-8') as f:
            mlist = json.loads(f.read())
            for m in mlist:
                items.append({"word": m, "count": mlist[m]})
        return items

    def patch_inv_taxo(self, resolved_dict: list, invtaxo_col: list) -> Iterator[dict]:
        '''
        The same as "patchInvTaxo" on export2mongodb.py
        :param resolved_dict: all the documents of the collection
        :param invtaxo_col:
        :return:
        '''

        for reso2 in resolved_dict:
            sblist = []
            if "Sachbegriff" in reso2:
                sblist = reso2["Sachbegriff"]
            if len(sblist):
                sl = sblist.copy()
                for sb in sblist:
                    for plist in self._find(invtaxo_col, {"name": sb}):
                        for pa in plist["parents"]:
                            if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                                sl.append(pa)
                yield {"_id": reso2["_id"],
                       "$set": {"Sachbegriff": sl}
                       }
                # resolved_col.update_one({"_id": reso2["_id"]}, {
                #     "$set": {"Sachbegriff": sl}})

    def project_hida_inv_taxo(self, hida_col: list, invtaxo_col: list) -> Iterator[dict]:
        # TODO: fix this function
        '''
        The same as "projectHidaInvTaxo" on export2mongodb.py
        :param hida_col:
        :param invtaxo_col:
        :return:
        '''

        for hida in hida_col:
            sblist = hida["Sachbegriff"]
            if len(sblist):
                sl = sblist
                for sb in sblist:
                    for plist in self._find(invtaxo_col, {"name": sb}):
                        for pa in plist["parents"]:
                            if pa != "ARCHITEKTUR" and pa != "FUNKTION" and pa != "BAUAUFGABE" and not pa in sl:
                                sl.append(pa)
                yield {"_id": hida["_id"],
                       "$set": {"Sachbegriff": sl}
                       }
                # hida_col.update_one({"_id": hida["_id"]}, {
                #     "$set": {"Sachbegriff": sl}})

    @staticmethod
    def _color_generator(number_of_colors: int) -> list:
        '''
        The same as "color_generator" on export2mongodb.py
        :param number_of_colors:
        :return:
        '''

        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
        return color

    @staticmethod
    def _find(collection_list: list, search_term: dict):
        search_term_items = search_term.items()
        key = search_term_items[0][0]
        value = search_term_items[0][1]
        return [i for i in collection_list if i[key] == value]

    @staticmethod
    def _find_one(collection_list: list, search_term: dict):
        search_term_items = search_term.items()
        key = search_term_items[0][0]
        value = search_term_items[0][1]
        for i in collection_list:
            if i[key] == value:
                return i
