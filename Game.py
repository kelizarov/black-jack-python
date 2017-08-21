from InputHandler import InputHandler
from GameMode import GameMode
from GameSession import GameSession


class Game:

    def __init__(self):
        self.__session = GameSession()
        self.__input = InputHandler()
        self.__mode = GameMode()

    def __event_tick(self):
        while True:
            try:
                cmd = self.__input.get_input()
                if cmd[0] == 'add_score':
                    self.__mode.add_score(cmd[1], cmd[2])
                if cmd[0] == 'set_score':
                    self.__mode.set_score(cmd[1], cmd[2])
                if cmd[0] == 'add_player':
                    self.__mode.add_player(cmd[1])
                if cmd[0] == 'add_ai':
                    self.__mode.add_ai(cmd[1])
                if cmd[0] == 'reset':
                    self.__mode.reset_score_for_all_players()
                if cmd[0] == 'exit':
                    break
            except EOFError:
                break
            except IndexError:
                print("Not enough args passed to command")
                continue
            except ValueError:
                print("Wrong argument")
                continue
        self.__event_end_play()

    def __event_begin_play(self):
        print(">>> Starting game")
##        self.__mode.set_up_game()
        self.__event_tick()

    def __event_end_play(self):
        print(">>> Exiting the game")

    def init_game(self):
        self.__event_begin_play()

