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
