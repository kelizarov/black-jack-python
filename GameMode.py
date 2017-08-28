import random

from InputHandler import InputHandler
from Player import Player
from AI import AI
from Types import GameState
from Types import ModeState
from Types import Cards


class GameMode:

    PLAYER_NAME = "Player"
    AI_NAME = "AI"

    def __init__(self):
        self.input = InputHandler()
        self.is_recovered = False
        self.players = []
        self.is_playing = False
        self.is_running = True
        self.game_state = GameState.START
        self.mode_state = ModeState.BIDDING
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
            "reset": self.reset,
            "give_card": self.give_card,
            "place_bid": self.place_bid,
            "exit": self.exit_game
        }
        self.pool = 0

    def add_player(self, name=PLAYER_NAME):
        self.input.add_command("add_player {0}".format(name))
        for pl in self.players:
            if pl.name == name:
                output = "{0} already exist".format(name)
                self.input.add_log(output)
                return
        self.players.append(Player(name))
        output = "{0} has joined the game".format(name)
        self.input.add_log(output)
        return output

    def add_ai(self, name=AI_NAME):
        self.input.add_command("add_ai {0}".format(name))
        for pl in self.players:
            if pl.name == name:
                output = "{0} already exist".format(name)
                self.input.add_log(output)
                return
        self.players.append(AI(name))
        output = "{0} has joined the game".format(name)
        self.input.add_log(output)
        return output

    def remove_player(self, name):
        self.input.add_command("remove_player {0}".format(name))
        output = "{0} doesn't exist".format(name)
        for pl in self.players:
            if pl.name == name:
                self.players.remove(pl)
                output = "{0} has left the game".format(name)
        self.input.add_log(output)
        return output

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def add_score(self, name, score):
        self.input.add_command("add_score {0} {1}".format(name, score))
        output = ""
        player = self.get_player_by_name(name)
        if player is not None:
            player.add_score(int(score))
            output = "{0} has updated his score: {1}".format(player.name, player.score)
        self.input.add_log(output)
        return output

    def set_score(self, name, score):
        self.input.add_command("set_score {0} {1}".format(name, score))
        output = ""
        player = self.get_player_by_name(name)
        if player is not None:
            player.set_score(int(score))
            output = "{0} has updated his score: {1}".format(player.name, player.score)
        self.input.add_log(output)
        return output

    def give_card(self, name, card = 0):
        if card == 0:
            card = random.randint(Cards.TWO, Cards.ACE)
        else:
            card = int(card)
        self.input.add_command("give_card {0} {1}".format(name, card))
        player = self.get_player_by_name(name)
        if player is not None:
            if Cards.get_card_name(Cards(), card) == "ACE":
                if player.points + Cards.get_card_value(Cards(), card) < 21:
                    points_to_give = 11
                else:
                    points_to_give = 1
            else:
                points_to_give = Cards.get_card_value(Cards(), card)
            if player.points + points_to_give < 21:
                player.give_card(points_to_give)
                self.input.notify_player(player, "You have been given card {0} of value {1}".format(
                    Cards.get_card_name(Cards(), card), points_to_give))
                self.input.add_log("Card {0} has been given to {1}".format(Cards.get_card_name(Cards(), card), name))
            else:
                return False
        return True

    def place_bid(self, name, amount):
        self.input.add_command("place_bid {0} {1}".format(name, amount))
        amount = int(amount)
        player = self.get_player_by_name(name)
        if player is not None:
            self.pool += amount
            player.bid = 0
            player.pocket -= amount
        self.input.add_log("{0} has bidden {1}".format(name, amount))
        for player in self.players:
            if player.bid > 0:
                return
        self.mode_state = ModeState.ROUND
        return "{0} has bidden {1}".format(name, amount)

    def check_player(self, player):
        if player.points > 21:
            self.mode_state = ModeState.RESULT
            return False
        if player.wants_to_leave:
            self.show_player(player.name)
            self.remove_player(player.name)
            return False
        return True

    def show_players(self):
        for player in self.players:
            print(player.__repr__())

    def show_player(self, name):
        player = self.get_player_by_name(name)
        if player is not None:
            print(player.__repr__())

    def reset(self):
        self.input.add_command("reset")
        for player in self.players:
            player.reset_cards()
        output = "All players' cards has been reset"
        self.input.add_log(output)
        return output

    def set_up_game(self):
        self.add_ai()
        self.add_player()
        self.start_game()

    def start_game(self):
        self.input.add_command("start_game")
        output = ""
        if not self.is_playing:
            output = "Starting game"
            self.is_playing = True
            self.game_state = GameState.PLAYING
            self.mode_state = ModeState.BIDDING
            self.reset()
        self.input.add_log(output)
        return output

    def end_game(self):
        self.input.add_command("end_game")
        output = ""
        if self.is_playing:
            if self.game_state == GameState.PLAYING:
                reason = "Round ended"
                self.game_state = GameState.START
            elif self.game_state == GameState.END:
                reason = "Game closed"
            else:
                reason = "Unknown reason"
            output = "Game is over: {0}".format(reason)
            self.is_playing = False
        self.input.add_log(output)
        return output

    def exit_game(self):
        self.input.add_command("exit")
        self.game_state = GameState.END
        if self.is_playing:
            self.end_game()
        if self.is_running:
            self.is_running = False
        output = "Exited"
        self.show_players()
        self.input.add_log(output)
        return output

    def determine_winner(self):
        winner = None
        points = 0
        for player in self.players:
            if player.points != points:
                if player.points > points:
                    points = player.points
                    winner = player
            else:
                winner = None
        return winner

    def play(self):
        if self.is_playing:
            if len(self.players) <= 1:
                self.exit_game()
            for player in self.players:
                if self.mode_state == ModeState.BIDDING:
                    self.input.notify_player(player, "Place your bid")
                player.think(self.mode_state)
                if not self.check_player(player):
                    break
                if self.mode_state == ModeState.ROUND:
                    if not self.give_card(player.name):
                        self.mode_state = ModeState.RESULT
                if self.mode_state == ModeState.BIDDING:
                    if player.bid > 0:
                        self.place_bid(player.name, player.bid)
            if self.mode_state == ModeState.RESULT:
                self.end_game()
        else:
            winner = self.determine_winner()
            if winner:
                print("The winner is {0}".format(winner.name))
                self.add_score(winner.name, 1)
            else:
                print("Nobody wins")
            self.show_players()
            self.start_game()
