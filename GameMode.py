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
            "exit": self.exit_game
        }
        self.pool = 0

    def add_player(self, name=PLAYER_NAME):
        self.input.add_command("add_player {0}".format(name))
        for pl in self.players:
            if pl.name == name:
                output = ">>> {0} already exist".format(name)
                self.input.add_log(output)
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
                self.input.add_log(output)
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

    def reset(self):
        self.input.add_command("reset")
        for player in self.players:
            player.reset_cards()
        output = ">>> All players' cards has been reset"
        self.input.add_log(output)
        return output

    def set_up_game(self, is_recovered=False):
        if not is_recovered:
            self.add_ai()
            self.add_player()
            self.start_game()

    def start_game(self):
        self.input.add_command("start_game")
        output = ""
        if not self.is_playing:
            output = ">>> Starting game"
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
            output = ">>> Game is over: {0}".format(reason)
            self.is_playing = False
        self.input.add_log(output)
        return output

    def play(self):
        if self.is_playing:
            for player in self.players:
                player.think(self.mode_state)
                if player.wants_to_leave:
                    self.show_player(player.name)
                    self.remove_player(player.name)
                if len(self.players) <= 1:
                    self.exit_game()
                if self.mode_state == ModeState.BIDDING:
                    if player.bid > 0:
                        self.place_bid(player.name, player.bid)
                elif self.mode_state == ModeState.ROUND:
                    if player.number_of_cards < 2:
                        self.give_card(player.name, random.randint(0, len(Cards.cards) - 1))
                    else:
                        self.mode_state = ModeState.RESULT
            if self.mode_state == ModeState.RESULT:
                self.end_game()
        else:
            winner = None
            points = 0
            for player in self.players:
                if player.points > points:
                    points = player.points
                    winner = player
            if winner:
                print(">>> The winner is {0}".format(winner.name))
                self.add_score(winner.name, 1)
            else:
                print(">>> Nobody wins")
            self.show_players()
            self.start_game()

    def give_card(self, name, card):
        card = int(card)
        self.input.add_command("give_card {0} {1}".format(name, card))
        for player in self.players:
            if name == player.name:
                player.give_card(self.get_card_by_nmb(card))
                self.input.add_log(">>> Card {0} has been given to {1}".format(Cards.cards[self.get_card_by_nmb(card)], name))

    def get_card_by_nmb(self, card):
        if card == 0:
            return Cards.TWO
        if card == 1:
            return Cards.THREE
        if card == 2:
            return Cards.FOUR
        if card == 3:
            return Cards.FIVE
        if card == 4:
            return Cards.SIX
        if card == 5:
            return Cards.SEVEN
        if card == 6:
            return Cards.EIGHT
        if card == 7:
            return Cards.NINE
        if card == 8:
            return Cards.TEN
        if card == 9:
            return Cards.JOKER
        if card == 10:
            return Cards.QUEEN
        if card == 11:
            return Cards.KING
        if card == 12:
            return Cards.ACE
        return None

    def place_bid(self, name, amount):
        self.input.add_command("place_bid {0} {1}".format(name, amount))
        for player in self.players:
            if player.name == name:
                self.pool += amount
                player.bid = 0
        self.input.add_log(">>> {0} has bidden {1}".format(name, amount))
        for player in self.players:
            if player.bid > 0:
                return
        self.mode_state = ModeState.ROUND

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
            self.end_game()
        if self.is_running:
            self.is_running = False
        self.game_state = GameState.END
        output = ">>> Exited"
        self.show_players()
        self.input.add_log(output)
        return output
