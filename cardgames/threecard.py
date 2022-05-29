import cardgames.poker as poker
from cardgames.poker import R
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
        self.handLength = 3
        super().__init__(cards)

    def setHand(self):
        """Return the best hand possible with the cards"""
        topStraight = self.bestStraightHand()
        if topStraight[0] == self.Hand.MINIROYAL:
            self.bestHand = self.Hand.MINIROYAL
            self.bestCards = topStraight[1][0:self.handLength]
            return

        elif topStraight[0] == self.Hand.STRAIGHTFLUSH:
            self.bestHand = self.Hand.STRAIGHTFLUSH
            self.bestCards = topStraight[1][0:self.handLength]
            return

        topDupe = self.bestDupeHand()

        if topDupe[0] == self.Hand.THREEOFKIND:
            self.bestHand = self.Hand.THREEOFKIND
            self.bestCards = topDupe[1][0:self.handLength]
            return

        elif topStraight[0] == self.Hand.STRAIGHT:
            self.bestHand = self.Hand.STRAIGHT
            self.bestCards = topStraight[1][0:self.handLength]
            return

        bestFlush = self.bestFlush()
        if bestFlush[0] == self.Hand.FLUSH:
            self.bestHand = self.Hand.FLUSH
            self.bestCards = bestFlush[0:self.handLength]
            return

        if topDupe[0] == self.Hand.PAIR:
            self.bestHand = self.Hand.PAIR
            self.bestCards = topDupe[1][0:self.handLength]
            return

        else:
            self.bestHand = self.Hand.HIGH
            self.bestCards = topDupe[1][0:self.handLength]
            return

    def getHand(self):
        """Return the best hand possible with the cards"""
        return self.bestHand

    def sortedHand(self):
        hand = self.getHand()
        returnHand = copy.copy(self.cards)
        returnHand.sort(key=lambda x: x.rank, reverse=True)
        if returnHand[-1].rank == R.ACE:
            returnHand.insert(0, returnHand.pop(-1))

        if hand == self.Hand.HIGH:
            return returnHand[0:self.handLength]

        if hand == self.Hand.PAIR:
            dupes = self.countDupes(returnHand)
            for card in dupes:
                if dupes[card] == 2:
                    target = card
            for x in range(0, len(returnHand)):
                if returnHand[x].rank == target:
                    returnHand.insert(0, returnHand.pop(x))
            return returnHand

        if hand == self.Hand.FLUSH:
            if len(returnHand) == self.handLength:
                return returnHand
