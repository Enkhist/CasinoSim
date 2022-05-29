import poker


class FiveCard(poker.BasePoker):
    class Hand(poker.BaseHand):
        HIGH = 1
        PAIR = 2
        TWOPAIR = 3
        THREEOFKIND = 4
        STRAIGHT = 5
        FLUSH = 6
        FULLHOUSE = 7
        FOUROFKIND = 8
        STRAIGHTFLUSH = 9
        ROYALFLUSH = 10

    def __init__(self, cards=None):
        self.handLength = 5
        super().__init__(cards)
    """
    What follows is a block to check if hands are present in the card set.
    They do not ensure that a better hand can be made. For example, A Full
    House hand will test true for isThreeOfKind, as you can make a Three of
    a kind out of those given cards. Similarly, A royal flush is also a
    straight flush.

    There will be a separate function for wittling what the best possible
    hand for those cards are, in order to avoid a madness of recursion in
    every function to test the cards.
    """

    def isRoyalFlush(self, cards=None):
        if self.bestHand == self.Hand.ROYALFLUSH:
            return self.Hand.ROYALFLUSH

    def isStraightFlush(self):
        if self.bestHand in [self.Hand.ROYALFLUSH, self.Hand.STRAIGHTFLUSH]:
            return True
        return False

    def isFourOfKind(self, cards=None):
        if self.bestHand == self.Hand.FOUROFKIND:
            return True
        return False

    def isFullHouse(self, cards=None):
        if self.bestHand == self.Hand.FULLHOUSE:
            return True
        return False

    def isFlush(self):
        return super().isFlush(5)

    def isStraight(self):
        if self.bestHand in [self.Hand.ROYALFLUSH,
                             self.Hand.STRAIGHTFLUSH,
                             self.Hand.STRAIGHT]:
            return True
        return False

    def isThreeOfKind(self, cards=None):
        if self.bestHand in [self.Hand.THREEOFKIND, self.Hand.FULLHOUSE,
                             self.Hand.FOUROFKIND]:
            return True
        return False

    def isTwoPair(self, cards=None):
        if self.bestHand in [self.Hand.FULLHOUSE, self.Hand.TWOPAIR]:
            return True
        return False

    def isPair(self):
        if self.bestHand in [self.Hand.THREEOFKIND, self.Hand.FULLHOUSE,
                             self.Hand.FOUROFKIND, self.Hand.TWOPAIR,
                             self.Hand.PAIR]:
            return True

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

    def setHand(self):
        """Return the best hand possible with the cards"""
        topStraight = self.bestStraightHand()
        if topStraight[0] == self.Hand.ROYALFLUSH:
            self.bestHand = self.Hand.ROYALFLUSH
            self.bestCards = topStraight[1][0:self.handLength]
            return
        elif topStraight[0] == self.Hand.STRAIGHTFLUSH:
            self.bestHand = self.Hand.STRAIGHTFLUSH
            self.bestCards = topStraight[1][0:self.handLength]
            return

        topDupe = self.bestDupeHand()
        if topDupe[0] == self.Hand.FOUROFKIND:
            self.bestHand = self.Hand.FOUROFKIND
            self.bestCards = topDupe[1][0:self.handLength]
            return
        elif topDupe[0] == self.Hand.FULLHOUSE:
            self.bestHand = self.Hand.FULLHOUSE
            self.bestCards = topDupe[1][0:self.handLength]
            return
        bestFlush = self.bestFlush()
        if bestFlush[0] == self.Hand.FLUSH:
            self.bestHand = self.Hand.FLUSH
            self.bestCards = bestFlush[0:self.handLength]
            return
        elif topStraight[0] == self.Hand.STRAIGHT:
            self.bestHand = self.Hand.STRAIGHT
            self.bestCards = topStraight[1][0:self.handLength]
            return
        else:
            # All hands below a straight are based on
            # repeats, so topDupe will correctly identify
            # them.
            self.bestHand = topDupe[0]
            self.bestCards = topDupe[1][0:self.handLength]
            return

    def getHand(self):
        return self.bestHand
