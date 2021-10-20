class MongoDBSettings:
    def __init__(self, data: dict):
        self._database = data["database"]
        self._collection = data["collection"]

    @property
    def database(self):
        '''
        The database property
        :return:
        '''
        return self._database

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, value: str):
        self._collection = value

    def __getitem__(self, item):
        try:
            return self._collection[item]
        except KeyError as e:
            raise e
