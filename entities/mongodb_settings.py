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
    def setting(self, value: str):
        self._collection = value
