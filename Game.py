import InputHandler
import GameMode
import GameSession


class Game:

    def __init__(self):
        self.__session = GameSession()
        self.__input = InputHandler()
        self.__mode = GameMode()

    def event_tick(self):
        while True:
            if len(self.__input) > 0:
                break
        pass

    def event_begin_play(self):
        pass

    def event_end_play(self):
        pass

    def start_game(self):
        pass



