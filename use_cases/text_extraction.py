'''
Module corresponding to extractText.py module in https://github.com/cfillies/semkibardoc
'''
import os

from pydantic import NonNegativeInt
import requests

from use_cases.utils import Utils as Utils


class TextExtraction:
    '''
    Extract metadata from documents using Apache Tika
    '''

    def __init__(self, tika_server: str) -> None:
        self.tika_client = tika_server

    def extract_text(self, file_path: str) -> str:
        '''
        Function corresponding to extract_text in module extractText.py from https://github.com/cfillies/semkibardoc
        :param file_path:
        :return:
        '''
        d = open(file_path, 'rb')
        r = requests.put(self.tika_client + "/tika", data=d)
        r.encoding = r.apparent_encoding
        return r.text

    def extract_meta(self, file_path: str) -> dict:
        '''
        Function corresponding to extract_meta in module extractText.py from https://github.com/cfillies/semkibardoc
        :param file_path:
        :return:
        '''
        file_name = str.split(file_path, '\\')[-1]
        response = requests.put(self.tika_client + "/meta", data=open(file_path,
                                                                      'rb'), headers={"Accept": "application/json"})
        try:
            result = response.json()
        except:
            result = {}
        result['file_name'] = file_name
        return result

    def process_document(self, district: str, path: str, col: list, startindex: NonNegativeInt, deleteall: bool) -> None:
        '''
        Function corresponding to extractText in module extractText.py from https://github.com/cfillies/semkibardoc
        :param district:
        :param path:
        :param col:
        :param startindex:
        :param deleteall:
        :return:
        '''

        i = startindex  # TODO: Ask for this variable
        m = 0
        # if deleteall:  # TODO: This should be done in the function that calls this one
        #     col.delete_many({})
        for root, d_names, f_names in os.walk(path):
            for f in f_names:
                if not f.endswith(".xml"):
                    i = i + 1

                    ff = os.path.join(root, f)
                    ext = os.path.splitext(ff)[1]

                    if ext == ".jpg" or ext == ".JPG" or ext == ".tif" or ext == ".wmf" or ext == ".gif":
                        continue

                    txt = self.extract_text(ff)
                    print(i, " ", os.path.join(root, ff))
                    met = {}
                    try:
                        util = Utils()
                        res = util.find_one(col, {"file": f, "ext": ext, "path": root})
                        yield {"file": f, "ext": ext, "path": root,
                               "$set": {"meta": met, "text": txt, "district": district}
                               }
                        # res = col.find_one_and_update({"file": f, "ext": ext, "path": root},
                        #                               {"$set": {"meta": met, "text": txt, "district": district}})
                        if not res:
                            # this is only needed if new documents are added:
                            # m = col.find().sort({"docid":-1}).limit(1)+1
                            m += 1
                            yield {"docid": m, "district": district, "file": f, "ext": ext, "path": root, "meta": met,
                                 "text": txt}
                            # col.insert_one(
                            #     {"docid": m, "district": district, "file": f, "ext": ext, "path": root, "meta": met,
                            #      "text": txt})
                    except:
                        print("TIKA Problem: ", ff)
                        pass
