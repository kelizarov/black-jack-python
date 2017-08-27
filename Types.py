from enum import Enum


class GameState(Enum):
    START = 0
    PLAYING = 1
    END = 2


class ModeState(Enum):
    BIDDING = 1
    ROUND = 2
    RESULT = 3


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