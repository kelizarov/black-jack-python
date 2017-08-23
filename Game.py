from InputHandler import InputHandler
from GameMode import GameMode, GameState
from GameSession import GameSession
import os


class Game:

    def __init__(self):
        self.__session = GameSession()
        self.__input = InputHandler()
        self.__mode = GameMode()
        self.commands = {}

    def __event_tick(self):
        while self.__mode.is_running:
            try:
                line = input()
                self.__input.execute_command(line, self.__mode.commands)
                self.__mode.players_think()
            except EOFError:
                break
            except IndexError as err:
                print("IndexError: {0}".format(err))
                continue
            except ValueError as err:
                print("ValueError: {0}".format(err))
                continue
        self.__event_end_play()

    def __event_begin_play(self):
        if os.path.isfile("temp"):
            self.__session.import_binary("temp")
        self.__event_tick()

    def __event_end_play(self):
        print(">>> Closing the game")
        if self.__mode.state is not GameState.END:
            self.__session.export_binary(self.__input.get_history())
        self.__input.dump_history()

    def init_game(self):
        self.__event_begin_play()

