import Player
import AI


class GameMode:

    def __init__(self):
        self.__players = []
        pass

    def __getattr__(self, item):
        pass

    def __setattr__(self, key, value):
        pass

    def add_player(self, player_to_add):
        if (isinstance(player_to_add, Player) or isinstance(player_to_add, AI)):
            self.__players.append(player_to_add)

    def remove_player(self, player_to_remove):
        if (self.__players.__contains__(player_to_remove)):
            self.__players.remove(player_to_remove)