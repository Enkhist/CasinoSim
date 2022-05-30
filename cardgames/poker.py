from cardgames import cards
from cards import Ranks as R
from enum import Enum
from itertools import groupby
import copy

"""
This class is going to try to dedicate itself to general poker utilities.
I intend on making separate 4 card and 3 card utilities.

That said, this library will include utilities for spotting 5 card hands
generally because Let It Ride, Stud, 3 card, and 4 card all have elements
that utilize 5 card poker hands
"""


class BasePoker:
    def __init__(self, cards=None):
        # stores a Hand enum of the best possible hand at that times
        self.bestHand = None
        # stores the best possible hand, at handLength length
        self.bestCards = None
        if cards:
            self.cards = cards
        else:
            self.cards = []
        self.setHand()

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            if self.bestHand > other.bestHand:
                return True
            elif self.bestHand < other.bestHand:
                return False
            else:
                selfHand = self.bestCards
                otherHand = other.bestCards
                for x in range(0, self.handLength):
                    if selfHand[x] > otherHand[x]:
                        return True
                    elif selfHand[x] < otherHand[x]:
                        return False
                    elif selfHand[x] == otherHand[x]:
                        continue
                return True
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            if self.bestHand > other.bestHand:
                return True
            elif self.bestHand < other.bestHand:
                return False
            else:
                selfHand = self.bestCards
                otherHand = other.bestCards
                for x in range(0, self.handLength):
                    if selfHand[x] > otherHand[x]:
                        return True
                    elif selfHand[x] < otherHand[x]:
                        return False
                    elif selfHand[x] == otherHand[x]:
                        continue
                if selfHand[self.handLength-1] == otherHand[self.handLength-1]:
                    return False
        return NotImplemented

    def __le__(self, other):
        return other >= self

    def __lt__(self, other):
        return other > self

    def __repr__(self):
        return str(str(self.bestHand)+str(self.bestCards))

    def _getSortedHand(self):
        """Returns hand sorted by face value"""
        ret = copy.copy(self.cards)
        ret.sort(key=lambda x: x.rank)
        return ret

    def _groupBySuit(self, cardsIn=None):
        if cardsIn is None:
            cardsIn = self.cards
        suitSortedCards = []
        for suit in cards.Suits:
            for card in cardsIn:
                if card.suit == suit:
                    suitSortedCards.append(card)
        return [list(result) for key, result in
                groupby(suitSortedCards, key=lambda card: card.suit)]

    def cardCheck(self, cardCheck):
        """Checks if a specific card can be found in a hand already"""
        for card in self.cards:
            if card.id == cardCheck.id:
                return True
        return False

    def append(self, card):
        if isinstance(card, list):
            self.cards.extend(card)
        elif isinstance(card, cards.Card):
            self.cards.append(card)
        self.setHand()

    def countDupes(self, cards=None, quads=True):
        """returns a dictionary of face values and how many times
        they appear"""
        if cards is None:
            cards = self.cards
        rawx = {}
        sortedx = {}
        for card in self.cards:
            if card.rank in rawx:
                if rawx[card.rank] >= 3 and quads:
                    rawx[card.rank] += 1
                else:
                    rawx[card.rank] += 1
            else:
                rawx.update({card.rank: 1})
        for rank in sorted(rawx, key=lambda x: (-rawx.get(x), -x.value)):
            if rawx[rank] > 1:
                sortedx[rank] = rawx[rank]
        return sortedx

    def bestDupeHand(self):
        """
        returns the best duplicate-based hand possible
        Returns either a None, or a list whose index 0
        is the hand Enum, followed by the self.handLength
        best hand. If no pair, returns a HIGH and sorted
        cards.
        """
        scrapCards = copy.copy(self.cards)
        scrapCards.sort(key=lambda x: x.rank.value, reverse=True)
        isQuads = bool("FOUROFKIND" in self.Hand._member_names_)
        isFullHouse = bool("FULLHOUSE" in self.Hand._member_names_)
        isTwoPair = bool("TWOPAIR" in self.Hand._member_names_)
        dupes = self.countDupes(isQuads)
        if len(dupes) == 0:
            return [self.Hand.HIGH, scrapCards]
        dupeIndex = list(dupes.keys())

        # Quads
        if isQuads and dupes[dupeIndex[0]] == 4:
            for w in range(0, len(scrapCards)):
                if scrapCards[w].rank == dupeIndex[0]:
                    scrapCards.insert(0, scrapCards.pop(w))
            return [self.Hand.FOUROFKIND, scrapCards]
        # Trips and Full house
        elif dupes[dupeIndex[0]] == 3:
            # Sort trips in front
            for z in range(0, len(scrapCards)):
                if scrapCards[z].rank == dupeIndex[0]:
                    scrapCards.insert(0, scrapCards.pop(z))
            if isFullHouse and len(dupes) > 1:
                dupeIndex.sort()
                for dupe in dupeIndex:
                    if dupe == scrapCards[0].rank:
                        continue
                    for z in range(3, len(scrapCards)):
                        if scrapCards[z].rank == dupe:
                            scrapCards.insert(3, scrapCards.pop(z))
                return [self.Hand.FULLHOUSE, scrapCards]
            return [self.Hand.THREEOFKIND, scrapCards]
        # pairs, 2 pairs
        elif dupes[dupeIndex[0]] == 2:
            # sort this pair in front
            for z in range(0, len(scrapCards)):
                if scrapCards[z].rank == dupeIndex[0]:
                    scrapCards.insert(0, scrapCards.pop(z))
            # check for second pair
            if isTwoPair and len(dupes) > 1:
                if scrapCards[z].rank == dupeIndex[1]:
                    scrapCards.insert(2, scrapCards.pop(z))
                return [self.Hand.TWOPAIR, scrapCards]
            return [self.Hand.PAIR, scrapCards]

    def bestStraightHand(self):
        """
        returns the best straight-based hand possible
        Returns either a None, or a list whose index 0
        is the hand Enum, followed by the self.handLength
        best hand. If no straight, returns None
        """
        straights = []
        scrapCards = copy.copy(self.cards)

        sortmeths = [lambda x: x.rank.value]
        for card in scrapCards:
            if card.rank == R.ACE:
                # Holds a low ace value getter, and a high ace value getter.
                sortmeths = [lambda x: x.rank.value, lambda y: y._lowAce()]

        for sortmeth in sortmeths:
            currentStraight = []
            scrapCards.sort(key=sortmeth, reverse=True)
            for card in scrapCards:
                if len(currentStraight) == 0:
                    currentStraight.append(card)
                    continue
                elif currentStraight[-1].rank.value == sortmeth(card)+1:
                    currentStraight.append(card)
                elif currentStraight[-1].rank.value == sortmeth(card):
                    continue
                else:
                    if len(currentStraight) >= self.handLength:
                        straights.append(currentStraight)
                    currentStraight = []
            # a repeat to just dump the currentStraight before the second check
            if len(currentStraight) >= self.handLength:
                straights.append(currentStraight)
            currentStraight = []

        # no straight == we are done here
        if len(straights) == 0:
            return [None, []]

        # sort all straights by first index(which should be highest card)
        straights.sort(key=lambda x: x[0].rank.value)

        # check for any straight flushes
        straightFlushes = []
        for straight in straights:
            for suit in self._groupBySuit(straight):
                if len(suit) >= self.handLength:
                    straightFlushes.append(suit)
        if len(straightFlushes) > 0:
            # check if royal
            rhand = None
            if "ROYALFLUSH" in self.Hand._member_names_:
                rhand = self.Hand.ROYALFLUSH
                royalCards = [R.TEN, R.JACK, R.QUEEN, R.KING, R.ACE]
            elif "MINIROYAL" in self.Hand._member_names_:
                rhand = self.Hand.MINIROYAL
                royalCards = [R.QUEEN, R.KING, R.ACE]
            if rhand:
                for sflush in straightFlushes:
                    royalTest = [n for n in sflush if n.rank in royalCards]
                    if len(royalTest) >= self.handLength:
                        return [rhand, sflush]
            return [self.Hand.STRAIGHTFLUSH, straightFlushes[0]]
        else:
            return [self.Hand.STRAIGHT, straights[0]]

    def bestFlush(self):
        """
        returns the best flush hand possible
        Returns either a None, or a list whose index 0
        is the hand Enum, followed by the self.handLength
        best flush. If no straight, returns None in index 0
        """
        flushes = []
        groups = self._groupBySuit(self.cards)
        for group in groups:
            if len(group) >= self.handLength:
                group.sort(key=lambda x: x.rank, reverse=True)
                flushes.append(group)
        if len(flushes) > 1:
            flushes.sort(key=lambda x: x[0].rank, reverse=True)
            return [self.Hand.FLUSH, flushes[0]]
        elif len(flushes) == 1:
            return [self.Hand.FLUSH, flushes[0]]
        else:
            return [None, []]


class BaseHand(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        return other >= self

    def __lt__(self, other):
        return other > self
