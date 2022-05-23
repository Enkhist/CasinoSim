import poker
from poker import Ranks
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
        super().__init__(cards)
        self.handLength = 5
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
        if cards == None:
            cards = self.cards

        if len(cards)<5:
            return False

        royalCards = [Ranks.TEN, Ranks.JACK, Ranks.QUEEN, Ranks.KING, Ranks.ACE]

        testStack = []

        for card in cards:
            if card.rank in royalCards:
                testStack.append(card)
        grouped = self._groupBySuit(testStack)
        for cardGroup in grouped:
            if self._isSequential(cardGroup):
                return True
        return False

    def isStraightFlush(self):
        return super().isStraightFlush(5)

    def isFourOfKind(self, cards=None):
        if cards == None:
            cards = self.cards

        if len(cards)<4:
            return False

        dupes = self.countDupes(cards)
        for card in dupes:
            if dupes[card] >= 4:
                return True
        return False

    def isFullHouse(self, cards=None):
        if cards == None:
            cards = self.cards

        if len(cards)<5:
            return False

        hasThree = False
        hasTwo = False
        dupes = self.countDupes(cards)
        for card in dupes:
            if dupes[card] == 3:
                hasThree = True
            if dupes[card] == 2:
                hasTwo = True
        return hasThree and hasTwo

    def isFlush(self):
        return super().isFlush(5)

    def isStraight(self):
        return super().isStraight(5)

    def isThreeOfKind(self, cards=None):
        return super().isThreeOfKind()

    def isTwoPair(self, cards=None):
        dupes = self.countDupes(cards)
        pairCount = 0
        for rank in dupes:
            if dupes[rank]>=2:
                pairCount+=1
        if pairCount>=2:
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

    def setHand(self):
        """Return the best hand possible with the cards"""
        if self.isHighCard():
            self.bestHand = self.Hand.HIGH
            return
        if self.isRoyalFlush():
            self.bestHand = self.Hand.ROYALFLUSH
            return
        if self.isStraightFlush():
            self.bestHand = self.Hand.STRAIGHTFLUSH
            return
        if self.isFourOfKind():
            self.bestHand = self.Hand.FOUROFKIND
            return
        if self.isFullHouse():
            self.bestHand = self.Hand.FULLHOUSE
            return
        if self.isFlush():
            self.bestHand = self.Hand.FLUSH
            return
        if self.isStraight():
            self.bestHand = self.Hand.STRAIGHT
            return
        if self.isThreeOfKind():
            self.bestHand = self.Hand.THREEOFKIND
            return
        if self.isTwoPair():
            self.bestHand = self.Hand.TWOPAIR
            return
        if self.isPair():
            self.bestHand = self.Hand.PAIR
            return


    def getHand(self):
        return self.bestHand