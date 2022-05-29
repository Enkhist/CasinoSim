import poker


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

    def isFourOfKind(self):
        dupeList = self.countDupes()
        for dupe in dupeList:
            if dupeList[dupe] >= 4:
                return True
            return False

    def isStraightFlush(self):
        return super().isStraightFlush(4)

    def isThreeOfKind(self):
        return super().isThreeOfKind()

    def isFlush(self):
        return super().isFlush(4)

    def isStraight(self):
        return super().isStraight(4)

    def isTwoPair(self):
        dupeList = self.countDupes()
        count = 0
        for dupe in dupeList:
            if dupeList[dupe] >= 2:
                count += 1
        if count >= 2:
            return True
        return False

    def isPair(self):
        return super().isPair()

    def isHighCard(self):
        """Checks that the hand is nothing but a useless high card hand.
        This function has the distinction of being reliant on the cards
        not being anything else.
        """
        dupes = self.countDupes(self.cards)
        for card in dupes:
            if dupes[card] > 1:
                return False
        if self.isFlush():
            return False
        if self.isStraight():
            return False
        return True

    def getHand(self):
        return self.bestHand

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
        if topDupe[0] == self.Hand.TWOPAIR:
            self.bestHand = self.Hand.TWOPAIR
            self.bestCards = topDupe[1][0:self.handLength]
            return
        if topDupe[0] == self.Hand.PAIR:
            self.bestHand = self.Hand.PAIR
            self.bestCards = topDupe[1][0:self.handLength]
            return
        else:
            self.bestHand = self.Hand.HIGH
            self.bestCards = topDupe[1][0:self.handLength]
            return
