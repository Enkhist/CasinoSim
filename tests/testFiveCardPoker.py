import fivecard
import cards
from cards import Ranks, Suits #syntactic help
import random
import unittest

class TestPoker(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.fiveCardHands = {}
        self.fiveCardHands['RoyalFlush'] = fivecard.FiveCard(cards.multiCard([[Ranks.TEN, Suits.SPADE],
                                                              [Ranks.JACK, Suits.SPADE],
                                                              [Ranks.QUEEN, Suits.SPADE],
                                                              [Ranks.KING, Suits.SPADE],
                                                              [Ranks.ACE, Suits.SPADE]]))

        self.fiveCardHands['StraightFlush'] = fivecard.FiveCard(cards.multiCard([[Ranks.FOUR, Suits.SPADE],
                                                                 [Ranks.FIVE, Suits.SPADE],
                                                                 [Ranks.SIX, Suits.SPADE],
                                                                 [Ranks.SEVEN, Suits.SPADE],
                                                                 [Ranks.EIGHT, Suits.SPADE]]))

        self.fiveCardHands['FourOfKind'] = fivecard.FiveCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                              [Ranks.ACE, Suits.CLUB],
                                                              [Ranks.ACE, Suits.DIAMOND],
                                                              [Ranks.ACE, Suits.HEART],
                                                              [Ranks.SEVEN, Suits.SPADE]]))

        self.fiveCardHands['FullHouse'] = fivecard.FiveCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                             [Ranks.ACE, Suits.DIAMOND],
                                                             [Ranks.ACE, Suits.CLUB],
                                                             [Ranks.KING, Suits.HEART],
                                                             [Ranks.KING, Suits.SPADE]]))

        self.fiveCardHands['Flush'] = fivecard.FiveCard(cards.multiCard([[Ranks.THREE, Suits.SPADE],
                                                         [Ranks.EIGHT, Suits.SPADE],
                                                         [Ranks.FIVE, Suits.SPADE],
                                                         [Ranks.TWO, Suits.SPADE],
                                                         [Ranks.JACK, Suits.SPADE]]))

        self.fiveCardHands['Straight'] = fivecard.FiveCard(cards.multiCard([[Ranks.THREE, Suits.SPADE],
                                                            [Ranks.FOUR, Suits.CLUB],
                                                            [Ranks.FIVE, Suits.DIAMOND],
                                                            [Ranks.SIX, Suits.HEART],
                                                            [Ranks.SEVEN, Suits.SPADE]]))

        self.fiveCardHands['ThreeOfKind'] = fivecard.FiveCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                               [Ranks.ACE, Suits.CLUB],
                                                               [Ranks.ACE, Suits.DIAMOND],
                                                               [Ranks.KING, Suits.SPADE],
                                                               [Ranks.FOUR, Suits.SPADE]]))

        self.fiveCardHands['TwoPair'] = fivecard.FiveCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                           [Ranks.ACE, Suits.CLUB],
                                                           [Ranks.KING, Suits.DIAMOND],
                                                           [Ranks.KING, Suits.HEART],
                                                           [Ranks.TWO, Suits.SPADE]]))

        self.fiveCardHands['Pair'] = fivecard.FiveCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                        [Ranks.ACE, Suits.HEART],
                                                        [Ranks.THREE, Suits.CLUB],
                                                        [Ranks.FOUR, Suits.CLUB],
                                                        [Ranks.KING, Suits.CLUB]]))

        self.fiveCardHands['AceHigh'] = fivecard.FiveCard(cards.multiCard([[Ranks.KING, Suits.SPADE],
                                                                        [Ranks.THREE, Suits.CLUB],
                                                                        [Ranks.FIVE, Suits.DIAMOND],
                                                                        [Ranks.EIGHT, Suits.SPADE],
                                                                        [Ranks.ACE, Suits.HEART]]))

        self.fiveCardHands['HighCard'] = fivecard.FiveCard(cards.multiCard([[Ranks.TWO, Suits.SPADE],
                                                                        [Ranks.FOUR, Suits.CLUB],
                                                                        [Ranks.FIVE, Suits.SPADE],
                                                                        [Ranks.SIX, Suits.DIAMOND],
                                                                        [Ranks.SEVEN, Suits.HEART]]))


    #what follows is a series to make sure the identifiers ONLY tests correct on their hands
    def testHands(self):
        hands = {}
    def testHandRoyal(self):
        for hand in self.fiveCardHands:
            if hand == "RoyalFlush":
                self.assertTrue(self.fiveCardHands[hand].isRoyalFlush(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isRoyalFlush(), hand)


    def testHandStraightFlush(self):
        for hand in self.fiveCardHands:
            if hand in ["StraightFlush", "RoyalFlush"]:
                self.assertTrue(self.fiveCardHands[hand].isStraightFlush(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isStraightFlush(), hand)

    def testHandFourOfKind(self):
        for hand in self.fiveCardHands:
            if hand == "FourOfKind":
                self.assertTrue(self.fiveCardHands[hand].isFourOfKind(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isFourOfKind(), hand)

    def testHandFullHouse(self):
        for hand in self.fiveCardHands:
            if hand == "FullHouse":
                self.assertTrue(self.fiveCardHands[hand].isFullHouse(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isFullHouse(), hand)

    def testHandStraight(self):
        for hand in self.fiveCardHands:
            if hand in ["Straight", "StraightFlush","RoyalFlush"]:
                self.assertTrue(self.fiveCardHands[hand].isStraight(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isStraight(), hand)

    def testHandFlush(self):
        for hand in self.fiveCardHands:
            if hand in ["Flush","StraightFlush", "RoyalFlush"]:
                self.assertTrue(self.fiveCardHands[hand].isFlush(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isFlush(), hand)

    def testHandThreeOfKind(self):
        for hand in self.fiveCardHands:
            if hand in ["ThreeOfKind","FullHouse", "FourOfKind"]:
                self.assertTrue(self.fiveCardHands[hand].isThreeOfKind(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isThreeOfKind(), hand)
    def testHandTwoPair(self):
        for hand in self.fiveCardHands:
            if hand in ["FullHouse","TwoPair"]:
                self.assertTrue(self.fiveCardHands[hand].isTwoPair(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isTwoPair(), hand)
    def testHandPair(self):
        for hand in self.fiveCardHands:
            if hand in ["FullHouse","TwoPair","Pair","FourOfKind","ThreeOfKind"]:
                self.assertTrue(self.fiveCardHands[hand].isPair(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isPair(), hand)
    def testHandHigh(self):
        for hand in self.fiveCardHands:
            if hand in ["AceHigh","HighCard"]:
                self.assertTrue(self.fiveCardHands[hand].isHighCard(), hand)
            else:
                self.assertFalse(self.fiveCardHands[hand].isHighCard(), hand)
    def testBestHands(self):
        handDict = {"AceHigh":fivecard.FiveCard.Hand.HIGH,
                    "HighCard":fivecard.FiveCard.Hand.HIGH,
                    "Pair":fivecard.FiveCard.Hand.PAIR,
                    "TwoPair":fivecard.FiveCard.Hand.TWOPAIR,
                    "ThreeOfKind":fivecard.FiveCard.Hand.THREEOFKIND,
                    "Straight":fivecard.FiveCard.Hand.STRAIGHT,
                    "Flush":fivecard.FiveCard.Hand.FLUSH,
                    "FullHouse":fivecard.FiveCard.Hand.FULLHOUSE,
                    "FourOfKind":fivecard.FiveCard.Hand.FOUROFKIND,
                    "StraightFlush":fivecard.FiveCard.Hand.STRAIGHTFLUSH,
                    "RoyalFlush":fivecard.FiveCard.Hand.ROYALFLUSH}
        for hand in handDict:
            self.assertEqual(self.fiveCardHands[hand].getHand(), handDict[hand], hand)


    def testAppendedHands(self):
        self.fiveCardHands["RoyalFlush"].append(cards.Card(Ranks.ACE, Suits.CLUB))
        self.fiveCardHands["StraightFlush"].append(cards.Card(Ranks.ACE, Suits.CLUB))
        self.assertTrue(self.fiveCardHands["RoyalFlush"].isRoyalFlush())
        self.assertTrue(self.fiveCardHands["StraightFlush"].isStraightFlush())
