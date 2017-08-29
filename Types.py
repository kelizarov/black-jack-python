from enum import Enum


class GameState(Enum):
    START = 0
    PLAYING = 1
    END = 2


class ModeState(Enum):
    BIDDING = 1
    SETTING = 2
    ROUND = 3
    RESULT = 4


class Cards(int):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JOKER = 9
    QUEEN = 10
    KING = 11
    ACE = 12

    cards = {
        TWO: 2,
        THREE: 3,
        FOUR: 4,
        FIVE: 5,
        SIX: 6,
        SEVEN: 7,
        EIGHT: 8,
        NINE: 9,
        TEN: 10,
        JOKER: 10,
        QUEEN: 10,
        KING: 10,
        ACE: 11
    }

    @staticmethod
    def get_card_name(card):
        if card == Cards.TWO:
            return "TWO"
        if card == Cards.THREE:
            return "THREE"
        if card == Cards.FOUR:
            return "FOUR"
        if card == Cards.FIVE:
            return "FIVE"
        if card == Cards.SIX:
            return "SIX"
        if card == Cards.SEVEN:
            return "SEVEN"
        if card == Cards.EIGHT:
            return "EIGHT"
        if card == Cards.NINE:
            return "NINE"
        if card == Cards.TEN:
            return "TEN"
        if card == Cards.JOKER:
            return "JOKER"
        if card == Cards.QUEEN:
            return "QUEEN"
        if card == Cards.KING:
            return "KING"
        if card == Cards.ACE:
            return "ACE"
        return "UNKNOWN"

    @staticmethod
    def get_card_value(card):
        return Cards.cards[card]