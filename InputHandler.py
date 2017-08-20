import sys


class InputHandler:

    __cmd_list = {
        "/help",
        "/start",
        "/exit"}

    def __getattr__(self, item):
        pass

    def parse_input(self):
        string = sys.stdin
        if string[0] == '/':
            if string in self.__cmd_list:
                return string
