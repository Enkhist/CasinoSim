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
        super().__init__(cards)

    def isFourOfKind(self):
        dupeList = self.countDupes()
        for dupe in dupeList:
            if dupeList[dupe]>=4:
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
            if dupeList[dupe]>=2:
                count+=1
        if count>=2:
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
        if self.isFourOfKind():
            return self.Hand.FOUROFKIND
        if self.isStraightFlush():
            return self.Hand.STRAIGHTFLUSH
        if self.isThreeOfKind():
            return self.Hand.THREEOFKIND
        if self.isFlush():
            return self.Hand.FLUSH
        if self.isStraight():
            return self.Hand.STRAIGHT
        if self.isTwoPair():
            return self.Hand.TWOPAIR
        if self.isPair():
            return self.Hand.PAIR