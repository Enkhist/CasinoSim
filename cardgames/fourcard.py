import cardgames.poker as poker


class FourCard(poker.BasePoker):
    class Hand(poker.BaseHand):
        HIGH = 1
        PAIR = 2
        TWOPAIR = 3
        STRAIGHT = 4
        FLUSH = 5
        THREEOFKIND = 6
        STRAIGHTFLUSH = 7
        FOUROFKIND = 8

    def __init__(self, cards=None):
        self.handLength = 4
        super().__init__(cards)

    def setHand(self):
        """Return the best hand possible with the cards"""
        topDupe = self.bestDupeHand()
        if topDupe[0] == self.Hand.FOUROFKIND:
            self.bestHand = self.Hand.FOUROFKIND
            self.bestCards = topDupe[1][0:self.handLength]
            return
        topStraight = self.bestStraightHand()
        if topStraight[0] == self.Hand.STRAIGHTFLUSH:
            self.bestHand = self.Hand.STRAIGHTFLUSH
            self.bestCards = topStraight[1][0:self.handLength]
            return
        if topDupe[0] == self.Hand.THREEOFKIND:
            self.bestHand = self.Hand.THREEOFKIND
            self.bestCards = topDupe[1][0:self.handLength]
            return
        bestFlush = self.bestFlush()
        if bestFlush[0] == self.Hand.FLUSH:
            self.bestHand = self.Hand.FLUSH
            self.bestCards = bestFlush[0:self.handLength]
            return
        if topStraight[0] == self.Hand.STRAIGHT:
            self.bestHand = self.Hand.STRAIGHT
            self.bestCards = topDupe[1][0:self.handLength]
            return
        else:
            self.bestHand = topDupe[0]
            self.bestCards = topDupe[1][0:self.handLength]
            return
