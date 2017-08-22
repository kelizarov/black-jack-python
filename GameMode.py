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

    def __init__(self):
        self.__players = []
        self.__is_playing = False

    def add_player(self, name = PLAYER_NAME):
        for pl in self.__players:
            if pl.name == name:
                print(">>> %s already exist" % pl.name)
                return
        self.__players.append(Player(name))
        print(">>> %s has been added" % name)

    def add_ai(self, name = AI_NAME):
        for pl in self.__players:
            if pl.name == name:
                print(">>> %s already exist" % pl.name)
                return
        self.__players.append(AI(name))
        print(">>> %s has been added"% name)

    def remove_player(self, name):
        for pl in self.__players:
            if pl.name == name:
                self.__players.remove(pl)
                print(">>> %s has been deleted" % pl.name)
                return
        print(">>> %s doesn't exist" % name)

    def add_score(self, player, score):
        for pl in self.__players:
            if pl.name == player:
                pl.add_score(int(score))

    def set_score(self, player, score):
        for pl in self.__players:
            if pl.name == player:
                pl.set_score(int(score))

    def reset_score_for_all_players(self):
        for player in self.__players:
            player.set_score(0)

    def set_up_game(self):
        self.add_player()
        self.add_ai()

    def start_game(self):
        if not self.__is_playing:
            self.__is_playing = True
            self.set_up_game()
            print(">>> Starting game")

    def players_think(self):
        if self.__is_playing:
            for player in self.__players:
                player.think()

    def show_players(self):
        for player in self.__players:
            print(player.__repr__())

    def show_player(self, name):
        for player in self.__players:
            if name == player.name:
                print(player.__repr__())
