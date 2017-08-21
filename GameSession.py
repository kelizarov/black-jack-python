class GameSession:

    def __init__(self, filename = ""):
        self.__commands = list()
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

    def execute(self, command):
        pass

    def undo(self):
        pass

