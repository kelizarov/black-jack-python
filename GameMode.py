from enum import Enum
from Player import Player
from AI import AI


class GameState(Enum):
    START = 0
    ROUND = 1
    END = 2


class GameMode:

    def __init__(self):
        self.__players = []

    def add_player(self, name):
        self.__players.append(Player(name))

    def add_ai(self, name):
        self.__players.append(AI(name))

    def remove_player(self, player_to_remove):
        if self.__players.__contains__(player_to_remove):
            self.__players.remove(player_to_remove)

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
        self.add_player(Player("player"))
        self.add_player(AI("ai"))
