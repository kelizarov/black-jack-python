class GameSession:

    def __init__(self, filename = ""):
        self.__lastmsg = ""
        pass

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass

    def read_from_file(self, filename):
        pass

    def write_to_file(self, filename):
        pass

    def get_last_message(self):
        return self.__lastmsg

