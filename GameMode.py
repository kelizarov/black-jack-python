from enum import Enum

from InputHandler import InputHandler
from Player import Player
from AI import AI


class GameState(Enum):
    START = 0
    ROUND = 1
    END = 2


class GameMode:

    PLAYER_NAME = "Player"
    AI_NAME = "AI"

    def __init__(self):
        self.input = InputHandler()

        self.players = []
        self.is_playing = False
        self.is_running = True
        self.state = GameState.START
        self.commands = {
            "start_game": self.start_game,
            "end_game": self.end_game,
            "add_score": self.add_score,
            "set_score": self.set_score,
            "add_player": self.add_player,
            "add_ai": self.add_ai,
            "remove_player": self.remove_player,
            "show_players": self.show_players,
            "show_player": self.show_player,
            "reset": self.reset_score_for_all_players,
            "exit": self.exit_game
        }

    def add_player(self, name=PLAYER_NAME):
        self.input.add_command("add_player {0}".format(name))
        for pl in self.players:
            if pl.name == name:
                output = ">>> {0} already exist".format(name)
                self.input.add_command(output)
                return
        self.players.append(Player(name))
        output = ">>> {0} has joined the game".format(name)
        self.input.add_log(output)
        return output

    def add_ai(self, name=AI_NAME):
        self.input.add_command("add_ai {0}".format(name))
        for pl in self.players:
            if pl.name == name:
                output = ">>> {0} already exist".format(name)
                self.input.add_command(output)
                return
        self.players.append(AI(name))
        output = ">>> {0} has joined the game".format(name)
        self.input.add_log(output)
        return output

    def remove_player(self, name):
        self.input.add_command("remove_player {0}".format(name))
        output = ">>> {0} doesn't exist".format(name)
        for pl in self.players:
            if pl.name == name:
                self.players.remove(pl)
                output = ">>> {0} has left the game".format(name)
        self.input.add_log(output)
        return output

    def add_score(self, player, score):
        self.input.add_command("add_score {0} {1}".format(player, score))
        output = ""
        for pl in self.players:
            if pl.name == player:
                pl.add_score(int(score))
                output = ">>> {0} has updated his score: {1}".format(pl.name, pl.score)
        self.input.add_log(output)
        return output

    def set_score(self, player, score):
        self.input.add_command("set_score {0} {1}".format(player, score))
        output = ""
        for pl in self.players:
            if pl.name == player:
                pl.set_score(int(score))
                output = ">>> {0} has updated his score: {1}".format(pl.name, pl.score)
        self.input.add_log(output)
        return output

    def reset_score_for_all_players(self):
        self.input.add_command("reset")
        for player in self.players:
            player.set_score(0)
        output = ">>> All players' score has been reset"
        self.input.add_log(output)
        return output

    def set_up_game(self):
        self.add_player()
        self.add_ai()
        self.start_game()

    def start_game(self):
        self.input.add_command("start_game")
        output = ""
        if not self.is_playing:
            output = ">>> Starting game"
            self.is_playing = True
            self.state = GameState.ROUND
        self.input.add_log(output)
        self.add_score("Player", 500)
        self.add_score("AI", 100)
        return output

    def end_game(self):
        self.input.add_command("end_game")
        output = ""
        if self.is_running and self.is_playing:
            if self.state == GameState.ROUND:
                reason = "Round ended"
            elif self.state == GameState.END:
                reason = "Game closed"
            else:
                reason = "Unknown reason"
            output = ">>> Game is over: {0}".format(reason)
            self.is_playing = False
            self.show_players()
            self.reset_score_for_all_players()
        self.input.add_log(output)
        return output

    def play(self):
        if self.is_running and self.is_playing:
            for player in self.players:
                player.think()
                if player.wants_to_leave:
                    self.show_player(player.name)
                    self.remove_player(player.name)
            if len(self.players) <= 1:
                self.exit_game()

    def show_players(self):
        for player in self.players:
            print(player.__repr__())

    def show_player(self, name):
        for player in self.players:
            if name == player.name:
                print(player.__repr__())

    def exit_game(self):
        self.input.add_command("exit")
        if self.is_playing:
            self.state = GameState.END
            self.end_game()
        if self.is_running:
            self.is_running = False
        output = ">>> Exited"
        self.input.add_log(output)
        return output
