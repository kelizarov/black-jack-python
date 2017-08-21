

class InputHandler(str):


    def __init__(self):
        self.__cmd = {"", "", ""}

    def get_input(self):
        line = input()
        if line:
            self.__cmd = [t(s) for t, s in zip((str, str, str), line.rstrip().split())]
            return self.__cmd

    def get_last_cmd(self):
        return self.__cmd