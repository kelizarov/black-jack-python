from enum import Enum
from Player import Player
from AI import AI


class GameState(Enum):
    START = 0
    ROUND = 1
    END = 2


class GameMode:

    PLAYER_NAME = "Player"
    AI_NAME = "AI"

    def __init__(self, is_debug):
        self.players = []
        self.is_playing = False
        self.is_running = True
        self.state = GameState.START
        self.is_debug = is_debug
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
        for pl in self.players:
            if pl.name == name:
                if self.is_debug:
                    print(">>> %s already exist" % pl.name)
                return
        self.players.append(Player(name))
        if self.is_debug:
            print(">>> %s has been added" % name)

    def add_ai(self, name=AI_NAME):
        for pl in self.players:
            if pl.name == name:
                if self.is_debug:
                    print(">>> %s already exist" % pl.name)
                return
        self.players.append(AI(name))
        if self.is_debug:
            print(">>> %s has been added"% name)

    def remove_player(self, name):
        for pl in self.players:
            if pl.name == name:
                self.players.remove(pl)
                if self.is_debug:
                    print(">>> %s has been deleted" % pl.name)
                return
        if self.is_debug:
            print(">>> %s doesn't exist" % name)

    def add_score(self, player, score):
        for pl in self.players:
            if pl.name == player:
                pl.add_score(int(score))
                if self.is_debug:
                    print(">>> {0} has updated his score: {1}".format(pl.name, pl.score))

    def set_score(self, player, score):
        for pl in self.players:
            if pl.name == player:
                pl.set_score(int(score))
                if self.is_debug:
                    print(">>> {0} has updated his score: {1}".format(pl.name, pl.score))

    def reset_score_for_all_players(self):
        for player in self.players:
            player.set_score(0)
        if self.is_debug:
            print(">>> All players' score has been reset")

    def set_up_game(self):
        self.add_player()
        self.add_ai()

    def start_game(self):
        if not self.is_playing:
            if self.is_debug:
                print(">>> Starting game")
            self.is_playing = True
            self.state = GameState.ROUND
            self.set_up_game()

    def end_game(self):
        if self.is_running and self.is_playing:
            if self.state == GameState.ROUND:
                reason = "Round ended"
            elif self.state == GameState.END:
                reason = "Game closed"
            else:
                reason = "Unknown reason"
            if self.is_debug:
                print(">>> Game has been ended: {0}".format(reason))
            self.is_playing = False
            self.show_players()
            self.reset_score_for_all_players()

    def players_think(self):
        if self.is_running and self.is_playing:
            for player in self.players:
                player.think()

    def show_players(self):
        for player in self.players:
            print(player.__repr__())

    def show_player(self, name):
        for player in self.players:
            if name == player.name:
                print(player.__repr__())

    def exit_game(self):
        if self.is_playing:
            self.state = GameState.END
            self.end_game()
        self.is_running = False

