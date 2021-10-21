class Utils:

    @staticmethod
    def find_many(collection_list: list, search_term: dict = None) -> list:
        if not search_term:
            return collection_list
        # for i in collection_list:
        #     for term in search_term:
        #         if i[term] == search_term[term]
        return [i for i in collection_list for term in search_term if i[term] == search_term[term]]

    @staticmethod
    def find_one(collection_list: list, search_term: dict = None) -> dict:
        if not search_term:
            return collection_list[0]
        for i in collection_list:
            for term in search_term:
                if i[term] == search_term[term]:
                    return i
