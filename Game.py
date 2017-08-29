from GameMode import GameMode, GameState
from GameSession import GameSession
import os


class Game:

    def __init__(self):
        self.__session = GameSession()
        self.__mode = GameMode()
        self.commands = {}

    def __event_tick(self):
        while self.__mode.is_running:
            try:
                self.__mode.play()
            # except IndexError as err:
            #     print("IndexError: {0}".format(err))
            #     continue
            # except ValueError as err:
            #     print("ValueError: {0}".format(err))
            #     continue
            # except TypeError as err:
            #     print("TypeError: {0}".format(err))
            #     continue
            except (KeyboardInterrupt, EOFError) as err:
                self.__mode.input.add_log(err)
                break
            except Exception as err:
                self.__mode.input.add_log(err)
                break
        self.__event_end_play()

    def __event_begin_play(self):
        if os.path.isfile(self.__session.binfile):
            try:
                history = self.__session.import_binary()
                self.__mode.input.notify = False
                self.__mode.input.add_log("Recovering old session")
                for cmd in history:
                    self.__mode.input.execute_command(cmd, self.__mode.commands, False)
                os.remove(self.__session.binfile)
                self.__mode.input.add_log("Old session has been recovered")
                self.__mode.input.notify = True
                self.__mode.set_up_game(True)
            except Exception as err:
                print("Error while trying to recover old session: {0}".format(err))
                # os.remove(self.__session.binfile)
                exit()
        else:
            self.__mode.set_up_game()
        self.__event_tick()

    def __event_end_play(self):
        if self.__mode.game_state is not GameState.END:
            self.__session.export_binary(self.__mode.input.commands)
            self.__session.export_text(self.__mode.input.history)
        else:
            self.__session.export_text(self.__mode.input.history)

    def init_game(self):
        self.__event_begin_play()

