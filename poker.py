import cards
from cards import Ranks, Suits
from enum import Enum
from itertools import groupby

"""
This class is going to try to dedicate itself to general poker utilities.
I intend on making separate 4 card and 3 card utilities. 

That said, this library will include utilities for spotting 5 card hands
generally because Let It Ride, Stud, 3 card, and 4 card all have elements
that utilize 5 card poker hands
"""


class BasePoker:
    def __init__(self, cards=None):
        if cards:
            self.cards = cards
            self.handLength = None
            self.bestHand = None #stores the best possible hand, at handLength length
            self.hand = None #stores a Hand enum of the best possible hand at that time
        else:
            self.cards = []

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            if self.getHand()>other.getHand():
                return True
            elif self.getHand()<other.getHand():
                return False
            else:
                selfHand = self.sortedHand()
                otherHand = other.sortedHand()
                for x in range(0,self.handLength):
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
            if self.getHand()>other.getHand():
                return True
            elif self.getHand()<other.getHand():
                return False
            else:
                selfHand = self.sortedHand()
                otherHand = other.sortedHand()
                for x in range(0,self.handLength):
                    if selfHand[x] > otherHand[x]:
                        return True
                    elif selfHand[x] < otherHand[x]:
                        return False
                    elif selfHand[x] == otherHand[x]:
                        continue
                if selfHand[handLength-1] == otherHand[handLength-1]:
                    return False
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            if self.getHand()>other.getHand():
                return False
            elif self.getHand()<other.getHand():
                return True
            else:
                selfHand = self.sortedHand()
                otherHand = other.sortedHand()
                for x in range(0,self.handLength):
                    if selfHand[x] > otherHand[x]:
                        return False
                    elif selfHand[x] < otherHand[x]:
                        return True
                    elif selfHand[x] == otherHand[x]:
                        continue
                return True
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.getHand()>other.getHand():
                return False
            elif self.getHand()<other.getHand():
                return True
            else:
                selfHand = self.sortedHand()
                otherHand = other.sortedHand()
                for x in range(0,self.handLength):
                    if selfHand[x] > otherHand[x]:
                        return False
                    elif selfHand[x] < otherHand[x]:
                        return True
                    elif selfHand[x] == otherHand[x]:
                        continue
                if selfHand[handLength-1] == otherHand[handLength-1]:
                    return False
        return NotImplemented


    def __repr__(self):
        return str(self.cards)

    def _getSortedHand(self):
        """Returns hand sorted by face value"""
        return self.cards.sort(key=lambda x: x.rank)

    def _groupBySuit(self, cardsIn=None):
        if cardsIn == None:
            cardsIn = self.cards
        suitSortedCards = []
        for suit in cards.Suits:
            for card in cardsIn:
                if card.suit == suit:
                    suitSortedCards.append(card)

        return [list(result) for key, result in groupby(suitSortedCards, key=lambda card: card.suit)]

    def cardCheck(self, cardCheck):
        """Checks if a specific card can be found in a hand already"""
        for card in self.cards:
            if card.id == cardCheck.id:
                return True
        return False

    def append(self, card):
        self.cards.append(card)

    def _isFlush(self, cards=None):
        """Returns true if full hand is a flush, false if not"""
        if cards == None:
            cards = self.cards

        #Two card flushes is utter nonsense
        if len(cards)<3:
            return False
        x = None
        for card in cards:
            if x == None:
                x = card.suit
                continue
            if x is not card.suit:
                return False
        return True

    def _straightRoutine(self, cards):
        x = None
        for card in cards:
            if x == None:
                x = card.rank.value
                continue

            if card.rank.value != (x+1):
                if card.rank.value == Ranks.ACE and x is Ranks.KING.value:
                    return True
                return False
            x = card.rank.value
        return True

    def _straightCountRoutine(self, cards):
        x = None
        maxCount = 1
        tempCount = 1
        for card in cards:
            if x == None:
                x = card.rank.value
                continue
            if card.rank.value == (x+1):
                tempCount += 1
            elif card.rank.value == x:
                continue
            else:
                if card.rank.value == Ranks.ACE and x == Ranks.KING.value:
                    tempCount += 1
                maxCount = tempCount
                tempCount = 1
            x = card.rank.value
        return max([maxCount,tempCount])

    def _isSequential(self, cards=None):
        """Returns true if full hand is sequential, false if not"""
        if cards == None:
            cards = self.cards

        #Two card straights is utter nonsense
        if len(cards)<3:
            return False
        tempHand = cards
        tempHand.sort(key=lambda x: x.rank.value)

        lowAce = self._straightRoutine(tempHand)
        if not lowAce and tempHand[0].rank.value == 1:
            tempHand.append(tempHand.pop(0))
            return self._straightRoutine(tempHand)

        return lowAce

    def _straightCount(self, cards=None):
        """returns max straight length"""
        if cards == None:
            cards = self.cards

        #Two card straights is utter nonsense
        if len(cards)<3:
            return False

        finalCount = [0]

        tempHand = cards
        tempHand.sort(key=lambda x: x.rank.value)

        finalCount.append(self._straightCountRoutine(tempHand))

        if tempHand[0].rank.value == 1:
            tempHand.append(tempHand.pop(0))
            finalCount.append(self._straightCountRoutine(tempHand))
        return max(finalCount)


    def _isStraightFlush(self, cards=None):
        if cards == None:
            cards = self.cards
        return self._isSequential(cards) and self._isFlush(cards)

    def countDupes(self, cards=None):
        """returns a dictionary of face values and how many times they appear"""
        if cards == None:
            cards = self.cards
        x = {}
        for card in self.cards:
            if card.rank in x:
                x[card.rank]+=1
            else:
                x.update({card.rank:1})
        return x

    def isPair(self):
        dupes = self.countDupes()
        pairCount = 0
        for rank in dupes:
            if dupes[rank]>=2:
                return True
        return False

    def isFlush(self, maxlen):
        if len(self.cards)<maxlen:
            return False

        groups = self._groupBySuit(self.cards)
        for group in groups:
            if len(group) >= maxlen:
                return True

    def isStraight(self,maxlen):
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
            if len(cardGroup)<maxlen:
                continue
            if self._straightCount(cardGroup)>=maxlen:
                response = True
        return response
        
    def sortedHand(self):
        return

    def sortedHandHigh(self):
        returnHand = self.cards
        returnHand.sort(key=lambda x: x.rank, reverse=True)
        if returnHand[-1].rank == Ranks.ACE:
            returnHand.insert(0,returnHand.pop(-1))
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
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented       