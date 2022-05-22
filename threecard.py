import poker
from poker import Ranks, Suits
import copy
class ThreeCard(poker.BasePoker):
    class Hand(poker.BaseHand):
        HIGH = 1
        PAIR = 2
        FLUSH = 3
        STRAIGHT = 4
        THREEOFKIND = 5
        STRAIGHTFLUSH = 6
        MINIROYAL = 7

    def __init__(self, cards=None):
        super().__init__(cards)
        self.handLength = 3

    def isMiniRoyal(self):
        royalCards = [Ranks.QUEEN, Ranks.KING, Ranks.ACE]

        testStack = []

        for card in self.cards:
            if card.rank in royalCards:
                testStack.append(card)
        grouped = self._groupBySuit(testStack)
        for cardGroup in grouped:
            if self._isSequential(cardGroup):
                return True
        return False

    def isStraightFlush(self):
        return super().isStraightFlush(3)

    def isThreeOfKind(self):
        return super().isThreeOfKind()

    def isStraight(self):
        return super().isStraight(3)

    def isFlush(self):
        return super().isFlush(3)

    def isPair(self):
        return super().isPair()

    def isHighCard(self):
        """Checks that the hand is nothing but a useless high card hand.
        This function has the distinction of being reliant on the cards 
        not being anything else.
        """
        dupes = self.countDupes()
        for card in dupes:
            if dupes[card]>1:
                return False
        if self.isFlush():
            return False
        if self.isStraight():
            return False
        return True

    def getHand(self):
        """Return the best hand possible with the cards"""
        if self.isHighCard():
            return self.Hand.HIGH
        if self.isMiniRoyal():
            return self.Hand.MINIROYAL
        if self.isStraightFlush():
            return self.Hand.STRAIGHTFLUSH
        if self.isThreeOfKind():
            return self.Hand.THREEOFKIND
        if self.isStraight():
            return self.Hand.STRAIGHT
        if self.isFlush():
            return self.Hand.FLUSH
        if self.isPair():
            return self.Hand.PAIR

    def sortedHand(self):
        hand = self.getHand()
        returnHand = copy.copy(self.cards)
        returnHand.sort(key=lambda x: x.rank, reverse=True)
        if returnHand[-1].rank == Ranks.ACE:
            returnHand.insert(0,returnHand.pop(-1))

        if hand == self.Hand.HIGH:
            return returnHand[0:self.handLength]

        if hand == self.Hand.PAIR:
            pair = []
            dupes = self.countDupes(returnHand)
            for card in dupes:
                if dupes[card] == 2:
                    target = card
            for x in range(0,len(returnHand)):
                if returnHand[x].rank == target:
                    pair.append(returnHand[x])
            for x in range(0,len(returnHand)):
                if returnHand[x].rank != target:
                    pair.append(returnHand[x])
            return pair

        if hand == self.Hand.FLUSH:
            if len(returnHand) == self.handLength:
                return returnHand
