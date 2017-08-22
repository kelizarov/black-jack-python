from InputHandler import InputHandler
from GameMode import GameMode
from GameSession import GameSession


class Game:

    def __init__(self):
        self.__session = GameSession()
        self.__input = InputHandler()
        self.__mode = GameMode()
        self.__commands = {
            "start_game": self.__mode.start_game,
            "add_score": self.__mode.add_score,
            "set_score": self.__mode.set_score,
            "add_player": self.__mode.add_player,
            "add_ai": self.__mode.add_ai,
            "remove_player": self.__mode.remove_player,
            "show_players": self.__mode.show_players,
            "show_player": self.__mode.show_player,
            "reset": self.__mode.reset_score_for_all_players,
            "exit": self.exit_game
        }

    def __event_tick(self):
        while True:
            try:
                cmd = self.__input.get_input()
                for key, value in self.__commands.items():
                    if key == cmd[0]:
                        if len(cmd) == 3:
                            value(cmd[1], cmd[2])
                        elif len(cmd) == 2:
                            value(cmd[1])
                        else:
                            value()
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
        self.__event_tick()

    def __event_end_play(self):
        print(">>> Exiting the game")

    def init_game(self):
        self.__event_begin_play()

    def exit_game(self):
        raise EOFError

