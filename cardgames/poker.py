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

    def countDupes(self, cards=None):
        """returns a dictionary of face values and how many times
        they appear"""
        if cards is None:
            cards = self.cards
        x = {}
        for card in self.cards:
            if card.rank in x:
                x[card.rank] += 1
            else:
                x.update({card.rank: 1})
        return x

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
        dupes = self.countDupes()
        maxRepeat = max(dupes, key=dupes.get)
        if "FOUROFKIND" in self.Hand._member_names_ and dupes[maxRepeat] == 4:
            retHand = []
            for rank in dupes:
                if dupes[rank] == 4:
                    targetRank = rank
                    break
            for n in range(0, len(scrapCards)):
                if scrapCards[n] == targetRank:
                    retHand.append(scrapCards.pop(n))
            retHand.extend(scrapCards)
            return [self.Hand.FOUROFKIND, retHand]

        elif dupes[maxRepeat] == 3:
            retHand = []
            for n in dupes:
                if dupes[n] == 3:
                    tripTarget = n
                    break
            if "FULLHOUSE" in self.Hand._member_names_:
                for n in dupes:
                    if dupes[n] == 3:
                        continue
                    if dupes[n] == 2:
                        for card in scrapCards:
                            if card.rank == tripTarget:
                                retHand.append(card)
                        for card in scrapCards:
                            if card.rank == n:
                                retHand.append(card)
                        return [self.Hand.FULLHOUSE, retHand]
            for card in range(0, len(scrapCards)):
                if scrapCards[card].rank == tripTarget:
                    scrapCards.insert(0, scrapCards.pop(card))
            return [self.Hand.THREEOFKIND, scrapCards]

        elif dupes[maxRepeat] == 2:
            for dupe in dupes:
                if dupes[dupe] == 2:
                    for card in range(0, len(scrapCards)):
                        if scrapCards[card].rank == dupe:
                            scrapCards.insert(0, scrapCards.pop(card))
            if "TWOPAIR" in self.Hand._member_names_:
                x = 0
                for n in dupes:
                    if dupes[n] == 2:
                        if x == 0:
                            x += 1
                            continue
                        else:
                            return [self.Hand.TWOPAIR, scrapCards]
            return [self.Hand.PAIR, scrapCards]
        else:
            return [self.Hand.HIGH, scrapCards]

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
