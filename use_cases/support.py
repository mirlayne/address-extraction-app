'''
Module corresponding to support.py from https://github.com/cfillies/semkibardoc
'''
from entities.authorities import GetAuthorities as GetAuthorities
from entities.mongodb_api_interface import MongoAPIInterface as MongoAPIInterface

from .utils import Utils as Utils


class Support:
    def __init__(self, get_auth: GetAuthorities):
        self.get_auth = get_auth,

    def init_support(self, hida_col: list, district) -> dict:
        # streets = pd.read_csv(r'hidaData.csv', sep='\t', encoding='utf-8', usecols=['denkmalStrasse'])
        # streetsset = set(streets['denkmalStrasse'].tolist())
        # streetsset.remove(np.nan)
        # item = col.find()
        # if not item:

        util = Utils()
        hidal = util.find_many(hida_col, {"Bezirk": district})

        get_auth = GetAuthorities()
        # hidal = hida_col.find({"Bezirk": district})
        streets = set([])
        for hida in hidal:
            if "AdresseDict" in hida:
                adlist = hida["AdresseDict"]
                streets.update(set(adlist.keys()))
        item = {"streetnames": list(streets),
                "authorities": get_auth.get_authorities(),
                "adcache": {}}
        return item
        # col.delete_many({})
        # col.insert_one(item)
