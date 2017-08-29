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
    DEALER_NAME = "Dealer"

    def __init__(self):
        self.input = InputHandler()
        self.is_recovered = False
        self.players = []
        self.is_playing = False
        self.is_running = True
        self.game_state = GameState.START
        self.mode_state = ModeState.BIDDING
        self.dealer = AI(self.DEALER_NAME)
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
        if name == self.DEALER_NAME:
            return self.dealer
        for player in self.players:
            if player.name == name:
                return player
        return None

    def add_score(self, player, score):
        output = ""
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("add_score {0} {1}".format(player.name, score))
        if player is not None:
            player.add_score(int(score))
            output = "{0} has updated his score: {1}".format(player.name, player.score)
        self.input.add_log(output)
        return output

    def set_score(self, player, score):
        output = ""
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("set_score {0} {1}".format(player.name, score))
        if player is not None:
            player.set_score(int(score))
            output = "{0} has updated his score: {1}".format(player.name, player.score)
        self.input.add_log(output)
        return output

    def give_card(self, player, card):
        if card == 0:
            card = random.randint(Cards.TWO, Cards.ACE)
        else:
            card = int(card)
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("give_card {0} {1}".format(player.name, card))
        if player is not None:
            if Cards.get_card_name(card) == "ACE":
                if player.points + Cards.get_card_value(card) < 21:
                    points_to_give = 11
                else:
                    points_to_give = 1
            else:
                points_to_give = Cards.get_card_value(card)
            if player.points + points_to_give < 21:
                player.take_card(points_to_give)
                self.input.notify_player(player, "You have been given card {0} of value {1}".format(
                    Cards.get_card_name(card),
                    points_to_give))
                self.input.add_log("Card {0} has been given to {1}".format(
                    Cards.get_card_name(card),
                    player.name))
            else:
                return False
        return True

    def place_bid(self, player, amount):
        amount = int(amount)
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("place_bid {0} {1}".format(player.name, amount))
        if player is not None:
            self.pool += amount
            player.pocket -= amount
        self.input.add_log("{0} has bidden {1}".format(player.name, amount))
        return "{0} has bidden {1}".format(player.name, amount)

    @staticmethod
    def check_player(player):
        if player.pocket <= 0:
            return False
        return True

    def check_players(self):
        for player in self.players:
            if player.wants_to_leave:
                self.show_player(player.name)
                self.remove_player(player.name)

    def show_players(self):
        print(self.dealer.__repr__())
        for player in self.players:
            print(player.__repr__())

    def show_player(self, name):
        player = self.get_player_by_name(name)
        if player is not None:
            print(player.__repr__())

    def players_ready(self):
        for player in self.players:
            if not player.is_ready:
                return False
        return True

    def players_got_all_cards(self):
        for player in self.players:
            if player.number_of_cards < 2:
                return False
        return True

    def reset(self):
        self.input.add_command("reset")
        self.dealer.reset()
        for player in self.players:
            player.reset()
        output = "All players' cards has been reset"
        self.input.add_log(output)
        return output

    def set_up_game(self, recovered=False):
        if recovered:
            self.determine_mode_state()
        else:
            self.add_player()
            self.start_game()

    def determine_mode_state(self):
        if self.players_got_all_cards():
            self.mode_state = ModeState.ROUND
        elif self.players_ready():
            self.mode_state = ModeState.SETTING

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

    def player_lost(self, player):
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("player_lost {0}".format(player.name))
        self.dealer.add_score(1)
        self.input.notify_player(player, "You have lost {0} credits".format(int(player.bid)))
        self.input.add_log("{0} has lost {1} points".format(player.name, int(player.bid)))

    def player_won(self, player):
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("player_won {0}".format(player.name))
        player.add_score(1)
        player.pocket += int(player.bid * 1.5)
        self.input.notify_player(player, "You have won {0} credits".format(int(player.bid * 1.5)))
        self.input.add_log("{0} has won {1} points".format(player.name, int(player.bid)))

    def player_draw(self, player):
        if isinstance(player, str):
            player = self.get_player_by_name(player)
        self.input.add_command("player_draw {0}".format(player.name))
        player.pocket += player.bid
        self.input.notify_player(player, "It's a draw. Nobody wins")
        self.input.add_log("{0} has same cards as Dealer. Nobody wins.".format(player.name))

    def determine_winner(self, player):
        if self.dealer.points > 21 or player.points > self.dealer.points:
            self.player_won(player)
        elif player.points == self.dealer.points:
            self.player_draw(player)
        elif player.points > 21 or player.points < self.dealer.points:
            self.player_lost(player)
        player.bid = 0

    def play(self):
        if self.is_playing:
            if len(self.players) == 0:
                self.exit_game()
            self.check_players()
            if self.mode_state == ModeState.BIDDING:
                for player in self.players:
                    if player.pocket > 0:
                        self.input.notify_player(player, "Place your bid. You have {0} credits.".format(player.pocket))
                    else:
                        self.input.notify_player(player, "You don't have any credits. Type 'quit' or Ctrl+C to exit.")
                    player.think(self.mode_state)
                    if player.bid > 0:
                        self.place_bid(player, player.bid)
                if self.players_ready():
                    self.mode_state = ModeState.SETTING
            elif self.mode_state == ModeState.SETTING:
                self.give_card(self.dealer, random.randint(Cards.TWO, Cards.ACE))
                while not self.players_got_all_cards():
                    for player in self.players:
                        self.give_card(player, random.randint(Cards.TWO, Cards.ACE))
                self.mode_state = ModeState.ROUND
            elif self.mode_state == ModeState.ROUND:
                for player in self.players:
                    player.think(self.mode_state)
                    if not self.give_card(player, random.randint(Cards.TWO, Cards.ACE)):
                        self.mode_state = ModeState.RESULT
                        break
                if not self.give_card(self.dealer, random.randint(Cards.TWO, Cards.ACE)):
                    self.mode_state = ModeState.RESULT
            elif self.mode_state == ModeState.RESULT:
                self.end_game()
                for player in self.players:
                    self.determine_winner(player)
                self.show_players()
                self.start_game()
