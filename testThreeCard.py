import threecard
import cards
from cards import Ranks, Suits #syntactic help
import random
import unittest

class TestPoker(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.threeCardHand = {}
        self.threeCardHand['MiniRoyal'] = threecard.ThreeCard(cards.multiCard([[Ranks.QUEEN, Suits.SPADE],
                                                                               [Ranks.KING, Suits.SPADE],
                                                                               [Ranks.ACE, Suits.SPADE]]))

        self.threeCardHand['StraightFlush'] = threecard.ThreeCard(cards.multiCard([[Ranks.SEVEN, Suits.SPADE],
                                                                                  [Ranks.FIVE, Suits.SPADE],
                                                                                  [Ranks.SIX, Suits.SPADE]]))

        self.threeCardHand['ThreeOfKind'] = threecard.ThreeCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                                 [Ranks.ACE, Suits.DIAMOND],
                                                                                 [Ranks.ACE, Suits.CLUB]]))

        self.threeCardHand['Straight'] = threecard.ThreeCard(cards.multiCard([[Ranks.TWO, Suits.SPADE],
                                                                             [Ranks.THREE, Suits.DIAMOND],
                                                                             [Ranks.FOUR, Suits.HEART]]))

        self.threeCardHand['Flush'] = threecard.ThreeCard(cards.multiCard([[Ranks.QUEEN, Suits.SPADE],
                                                                           [Ranks.SEVEN, Suits.SPADE],
                                                                           [Ranks.TWO, Suits.SPADE]]))

        self.threeCardHand['Pair'] = threecard.ThreeCard(cards.multiCard([[Ranks.ACE, Suits.SPADE],
                                                                          [Ranks.ACE, Suits.DIAMOND],
                                                                          [Ranks.SEVEN, Suits.SPADE]]))

        self.threeCardHand['High'] = threecard.ThreeCard(cards.multiCard([[Ranks.THREE, Suits.DIAMOND],
                                                                          [Ranks.SEVEN, Suits.CLUB],
                                                                          [Ranks.TWO, Suits.HEART]]))


    #what follows is a series to make sure the identifiers ONLY tests correct on their hands
    def testMiniRoyal(self):
        for hand in self.threeCardHand:
            if hand == "MiniRoyal":
                self.assertTrue(self.threeCardHand[hand].isMiniRoyal(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isMiniRoyal(), hand)

    def testStraightFlush(self):
        for hand in self.threeCardHand:
            if hand in ["MiniRoyal","StraightFlush"]:
                self.assertTrue(self.threeCardHand[hand].isStraightFlush(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isStraightFlush(), hand)

    def testThreeOfKind(self):
        for hand in self.threeCardHand:
            if hand in ["ThreeOfKind"]:
                self.assertTrue(self.threeCardHand[hand].isThreeOfKind(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isThreeOfKind(), hand)
    def testStraight(self):
        for hand in self.threeCardHand:
            if hand in ["Straight","StraightFlush","MiniRoyal"]:
                self.assertTrue(self.threeCardHand[hand].isStraight(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isStraight(), hand)

    def testFlush(self):
        for hand in self.threeCardHand:
            if hand in ["Flush","StraightFlush","MiniRoyal"]:
                self.assertTrue(self.threeCardHand[hand].isFlush(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isFlush(), hand)

    def testIsPair(self):
        for hand in self.threeCardHand:
            if hand in ["ThreeOfKind","Pair"]:
                self.assertTrue(self.threeCardHand[hand].isPair(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isPair(), hand)

    def testIsHigh(self):
        for hand in self.threeCardHand:
            if hand in ["High"]:
                self.assertTrue(self.threeCardHand[hand].isHighCard(), hand)
            else:
                self.assertFalse(self.threeCardHand[hand].isHighCard(), hand)

    def testBestHands(self):
        handDict = {"High":threecard.ThreeCard.Hand.HIGH,
                    "Pair":threecard.ThreeCard.Hand.PAIR,
                    "Flush":threecard.ThreeCard.Hand.FLUSH,
                    "Straight":threecard.ThreeCard.Hand.STRAIGHT,
                    "ThreeOfKind":threecard.ThreeCard.Hand.THREEOFKIND,
                    "StraightFlush":threecard.ThreeCard.Hand.STRAIGHTFLUSH,
                    "MiniRoyal":threecard.ThreeCard.Hand.MINIROYAL,}
        for hand in handDict:
            self.assertEqual(self.threeCardHand[hand].getHand(), handDict[hand], hand)

    def testHandCoarseComparison(self):
        lastHand = None
        for hand in self.threeCardHand:
            if not lastHand:
                lastHand = hand
                continue
            self.assertTrue(self.threeCardHand[hand]<self.threeCardHand[lastHand], hand)
            self.assertTrue(self.threeCardHand[hand]<=self.threeCardHand[lastHand], hand)
            self.assertFalse(self.threeCardHand[hand]>self.threeCardHand[lastHand], hand)
            self.assertFalse(self.threeCardHand[hand]>=self.threeCardHand[lastHand], hand)
            lastHand = hand

    def testHandFineComparison(self):
        lesserHigh = threecard.ThreeCard(cards.multiCard([[Ranks.TWO, Suits.SPADE],
                                                         [Ranks.THREE, Suits.DIAMOND],
                                                         [Ranks.FIVE, Suits.CLUB]]))
        lesserPair = threecard.ThreeCard(cards.multiCard([[Ranks.SEVEN, Suits.SPADE],
                                                         [Ranks.SEVEN, Suits.DIAMOND],
                                                         [Ranks.THREE, Suits.CLUB]]))
        lesserFlush = threecard.ThreeCard(cards.multiCard([[Ranks.SIX, Suits.SPADE],
                                                         [Ranks.QUEEN, Suits.SPADE],
                                                         [Ranks.TWO, Suits.SPADE]]))

        self.assertTrue(self.threeCardHand["High"]>lesserHigh)
        self.assertTrue(self.threeCardHand["High"]>=lesserHigh)
        self.assertFalse(self.threeCardHand["High"]<=lesserHigh)
        self.assertFalse(self.threeCardHand["High"]<lesserHigh)

        self.assertFalse(lesserHigh>self.threeCardHand["High"])
        self.assertFalse(lesserHigh>=self.threeCardHand["High"])
        self.assertTrue(lesserHigh<=self.threeCardHand["High"])
        self.assertTrue(lesserHigh<self.threeCardHand["High"])




        self.assertTrue(self.threeCardHand["Pair"]>lesserPair)
        self.assertTrue(self.threeCardHand["Pair"]>=lesserPair)
        self.assertFalse(self.threeCardHand["Pair"]<=lesserPair)
        self.assertFalse(self.threeCardHand["Pair"]<lesserPair)

        self.assertTrue(self.threeCardHand["Flush"]>lesserFlush)
        self.assertTrue(self.threeCardHand["Flush"]>=lesserFlush)
        self.assertFalse(self.threeCardHand["Flush"]<=lesserFlush)
        self.assertFalse(self.threeCardHand["Flush"]<lesserFlush)