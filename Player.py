class Player:

    def __init__(self, id, name, score = 0):
        self.__id = id
        self.__name = name
        self.__score = score
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass
