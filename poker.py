import cards
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
            if self.getHand() > other.getHand():
                return True
            elif self.getHand() < other.getHand():
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
            if self.getHand() > other.getHand():
                return True
            elif self.getHand() < other.getHand():
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

    def _isFlush(self, cards=None):
        """Returns true if full hand is a flush, false if not"""
        if cards is None:
            cards = self.cards

        # Two card flushes is utter nonsense
        if len(cards) < 3:
            return False
        x = None
        for card in cards:
            if x is None:
                x = card.suit
                continue
            if x is not card.suit:
                return False
        return True

    def _straightRoutine(self, cards):
        x = None
        for card in cards:
            if x is None:
                x = card.rank.value
                continue

            if card.rank.value != (x+1):
                if card.rank.value == R.ACE and x is R.KING.value:
                    return True
                return False
            x = card.rank.value
        return True

    def _straightCountRoutine(self, cards):
        x = None
        maxCount = 1
        tempCount = 1
        for card in cards:
            if x is None:
                x = card.rank.value
                continue
            if card.rank.value == (x+1):
                tempCount += 1
            elif card.rank.value == x:
                continue
            else:
                if card.rank.value == R.ACE and x == R.KING.value:
                    tempCount += 1
                maxCount = tempCount
                tempCount = 1
            x = card.rank.value
        return max([maxCount, tempCount])

    def _isSequential(self, cards=None):
        """Returns true if full hand is sequential, false if not"""
        if cards is None:
            cards = self.cards

        # Two card straights is utter nonsense
        if len(cards) < 3:
            return False
        tempHand = copy.copy(cards)
        tempHand.sort(key=lambda x: x.rank.value)

        lowAce = self._straightRoutine(tempHand)
        if not lowAce and tempHand[0].rank.value == 1:
            tempHand.append(tempHand.pop(0))
            return self._straightRoutine(tempHand)

        return lowAce

    def _straightCount(self, cards=None):
        """returns max straight length"""
        if cards is None:
            cards = self.cards

        # Two card straights is utter nonsense
        if len(cards) < 3:
            return False

        finalCount = [0]

        tempHand = copy.copy(cards)
        tempHand.sort(key=lambda x: x.rank.value)

        finalCount.append(self._straightCountRoutine(tempHand))

        if tempHand[0].rank.value == 1:
            tempHand.append(tempHand.pop(0))
            finalCount.append(self._straightCountRoutine(tempHand))
        return max(finalCount)

    def _isStraightFlush(self, cards=None):
        if cards is None:
            cards = self.cards
        return self._isSequential(cards) and self._isFlush(cards)

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
            if "FULLHOUSE" in self.Hand._member_names_:
                for n in dupes:
                    if dupes[n] == 3:
                        tripTarget = n
                        continue
                    if dupes[n] == 2:
                        for card in scrapCards:
                            if card.rank == tripTarget:
                                retHand.append(card)
                        for card in scrapCards:
                            if card.rank == n:
                                retHand.append(card)
                        return [self.Hand.FULLHOUSE, retHand]
            for n in dupes:
                if dupes[n] == 3:
                    tripTarget = n
                    break
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

    def isPair(self):
        dupes = self.countDupes()
        for rank in dupes:
            if dupes[rank] >= 2:
                return True
        return False

    def isFlush(self, maxlen):
        if len(self.cards) < maxlen:
            return False

        groups = self._groupBySuit(self.cards)
        for group in groups:
            if len(group) >= maxlen:
                group.sort(key=lambda x: x.rank, reverse=True)
                return group

    def isStraight(self, maxlen):
        if self._straightCount(self.cards) >= maxlen:
            return True
        return False

    def isThreeOfKind(self):
        dupes = self.countDupes(self.cards)
        for rank in dupes:
            if dupes[rank] >= 3:
                return True
        return False

    def isStraightFlush(self, maxlen):
        response = False

        grouped = self._groupBySuit(self.cards)
        for cardGroup in grouped:
            if len(cardGroup) < maxlen:
                continue
            if self._straightCount(cardGroup) >= maxlen:
                response = True
        return response

    def sortedHand(self):
        return

    def sortedHandHigh(self):
        returnHand = copy.copy(self.cards)
        returnHand.sort(key=lambda x: x.rank, reverse=True)
        if returnHand[-1].rank == R.ACE:
            returnHand.insert(0, returnHand.pop(-1))
        return returnHand[0:self.handLength]


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
