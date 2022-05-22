# -*- coding:utf-8 -*-

import math
from enum import Enum, IntEnum

class Suits(Enum):
    HEART = 0
    CLUB = 1
    DIAMOND = 2
    SPADE = 3

class Ranks(IntEnum):
    JOKER = -1
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

uidEng = {
    1:"Ace",
    2:"Two",
    3:"Three",
    4:"Four",
    5:"Five",
    6:"Six",
    7:"Seven",
    8:"Eight",
    9:"Nine",
    10:"Ten",
    11:"Jack",
    12:"Queen",
    13:"King"
}
uidEngShort = {
    1:" A",
    2:" 2",
    3:" 3",
    4:" 4",
    5:" 5",
    6:" 6",
    7:" 7",
    8:" 8",
    9:" 9",
    10:"10",
    11:" J",
    12:" Q",
    13:" K"
}

suitEng = {
    0:"Hearts",
    1:"Club",
    2:"Diamonds",
    3:"Spades"
}
suitEngShort = {
    0:"♡",
    1:"♣",
    2:"♢",
    3:"♠"
}
class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank


    def __ge__(self, other):
        if self.__class__ is other.__class__:
            if self.rank == Ranks.ACE:
                return True
            return self.rank >= other.rank
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            if self.rank == Ranks.ACE:
                if other.rank == Ranks.ACE:
                    return False
                return True
            return self.rank > other.rank
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            if self.rank == Ranks.ACE:
                if self.rank == other.rank:
                    return True
                return False
            return self.rank <= other.rank
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.rank == Ranks.ACE:
                return False
            return self.rank < other.rank
        return NotImplemented

    def __repr__(self):
        return self.getShortName()

    def __eq__(self, other):
        if not isinstance(other, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.rank == other.rank

    def getCardName(self):
        return uidEng[self.uid]+" of "+suitEng[self.suit]

    def getShortName(self):
        return ""+uidEngShort[self.rank.value]+suitEngShort[self.suit.value]+""

def multiCard(input):
    """takes an array of card suits and values, and returns an array of card objects"""
    response = []
    for card in input:
        response.append(Card(*card))
    return response

def getDeck():
    """Create standard deck"""
    deck = []
    for suit in Suits:
        for rank in Ranks:
            if rank is Ranks.JOKER:
                continue
            deck.append(Card(rank, suit))
    return deck