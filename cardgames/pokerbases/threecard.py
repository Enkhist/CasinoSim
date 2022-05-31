import poker


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
        if topStraight[0] in [self.Hand.MINIROYAL,
                              self.Hand.STRAIGHTFLUSH]:
            self.bestHand = topStraight[0]
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

        else:
            self.bestHand = topDupe[0]
            self.bestCards = topDupe[1][0:self.handLength]
            return
