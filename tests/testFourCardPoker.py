import fourcard as fcp
import cards
from cards import Ranks, Suits #syntactic help
import random
import unittest

class TestPoker(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.fourCardHands = {}
        self.fourCardHands['FourOfKind'] = fcp.FourCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                           [Ranks.ACE, Suits.DIAMOND],
                                                                           [Ranks.ACE, Suits.CLUB],
                                                                           [Ranks.ACE, Suits.HEART]]))

        self.fourCardHands['StraightFlush'] = fcp.FourCard(cards.multiCard([[Ranks.FOUR, Suits.SPADE],
                                                                           [Ranks.FIVE, Suits.SPADE],
                                                                           [Ranks.SIX, Suits.SPADE],
                                                                           [Ranks.SEVEN, Suits.SPADE]]))

        self.fourCardHands['ThreeOfKind'] = fcp.FourCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                           [Ranks.ACE, Suits.CLUB],
                                                                           [Ranks.ACE, Suits.DIAMOND],
                                                                           [Ranks.KING, Suits.HEART]]))

        self.fourCardHands['Flush'] = fcp.FourCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                      [Ranks.SEVEN, Suits.SPADE],
                                                                      [Ranks.TWO, Suits.SPADE],
                                                                      [Ranks.EIGHT, Suits.SPADE]]))

        self.fourCardHands['Straight'] = fcp.FourCard(cards.multiCard([[Ranks.FOUR, Suits.SPADE],
                                                                           [Ranks.FIVE, Suits.CLUB],
                                                                           [Ranks.SIX, Suits.DIAMOND],
                                                                           [Ranks.SEVEN, Suits.HEART]]))

        self.fourCardHands['TwoPair'] = fcp.FourCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                           [Ranks.ACE, Suits.HEART],
                                                                           [Ranks.KING, Suits.CLUB],
                                                                           [Ranks.KING, Suits.DIAMOND]]))

        self.fourCardHands['Pair'] = fcp.FourCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                     [Ranks.ACE, Suits.DIAMOND],
                                                                     [Ranks.SIX, Suits.HEART],
                                                                     [Ranks.SEVEN, Suits.CLUB]]))

        self.fourCardHands['High'] = fcp.FourCard(cards.multiCard([[Ranks.SEVEN, Suits.SPADE],
                                                                     [Ranks.THREE, Suits.CLUB],
                                                                     [Ranks.NINE, Suits.DIAMOND],
                                                                     [Ranks.TWO, Suits.HEART]]))

    def testBestHands(self):
        handDict = {"High":fcp.FourCard.Hand.HIGH,
                    "Pair":fcp.FourCard.Hand.PAIR,
                    "TwoPair":fcp.FourCard.Hand.TWOPAIR,
                    "Straight":fcp.FourCard.Hand.STRAIGHT,
                    "Flush":fcp.FourCard.Hand.FLUSH,
                    "ThreeOfKind":fcp.FourCard.Hand.THREEOFKIND,
                    "StraightFlush":fcp.FourCard.Hand.STRAIGHTFLUSH,
                    "FourOfKind":fcp.FourCard.Hand.FOUROFKIND,}
        for hand in handDict:
            self.assertEqual(self.fourCardHands[hand].getHand(), handDict[hand], hand)

