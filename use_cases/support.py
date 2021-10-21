from entities.authorities import GetAuthorities as GetAuthorities
from entities.mongodb_api_interface import MongoAPIInterface as MongoAPIInterface


class Support:
    def __init__(self, get_auth: GetAuthorities, mongo_api: MongoAPIInterface):
        self.get_auth = get_auth,
        self.mongo_api = mongo_api

    def init_support(self, coll_name: str, hida_name: str, district) -> None:
        # streets = pd.read_csv(r'hidaData.csv', sep='\t', encoding='utf-8', usecols=['denkmalStrasse'])
        # streetsset = set(streets['denkmalStrasse'].tolist())
        # streetsset.remove(np.nan)
        # item = col.find()
        # if not item:
        col = self.mongo_api[coll_name]
        hida_col = self.mongo_api[hida_name]

        get_auth = GetAuthorities()
        hidal = hida_col.find({"Bezirk": district})
        streets = set([])
        for hida in hidal:
            if "AdresseDict" in hida:
                adlist = hida["AdresseDict"]
                streets.update(set(adlist.keys()))
        item = {"streetnames": list(streets),
                "authorities": get_auth.get_authorities(),
                "adcache": {}}
        col.delete_many({})
        col.insert_one(item)