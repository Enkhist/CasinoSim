from cardgames.fourcard import FourCard
from cardgames.cards import multiCard, Ranks as R, Suits as S
import unittest


class TestPoker(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.fcpHands = {}
        self.fcpHands['FourOfKind'] = FourCard(multiCard([[R.ACE, S.SPADE],
                                                          [R.ACE, S.DIAMOND],
                                                          [R.ACE, S.CLUB],
                                                          [R.ACE, S.HEART]]))

        self.fcpHands['sFlush'] = FourCard(multiCard([[R.FOUR, S.SPADE],
                                                      [R.FIVE, S.SPADE],
                                                      [R.SIX, S.SPADE],
                                                      [R.SEVEN, S.SPADE]]))

        self.fcpHands['Trips'] = FourCard(multiCard([[R.ACE, S.SPADE],
                                                     [R.ACE, S.CLUB],
                                                     [R.ACE, S.DIAMOND],
                                                     [R.KING, S.HEART]]))

        self.fcpHands['Flush'] = FourCard(multiCard([[R.ACE, S.SPADE],
                                                     [R.SEVEN, S.SPADE],
                                                     [R.TWO, S.SPADE],
                                                     [R.EIGHT, S.SPADE]]))

        self.fcpHands['Straight'] = FourCard(multiCard([[R.FOUR, S.SPADE],
                                                        [R.FIVE, S.CLUB],
                                                        [R.SIX, S.DIAMOND],
                                                        [R.SEVEN, S.HEART]]))

        self.fcpHands['TwoPair'] = FourCard(multiCard([[R.ACE, S.SPADE],
                                                       [R.ACE, S.HEART],
                                                       [R.KING, S.CLUB],
                                                       [R.KING, S.DIAMOND]]))

        self.fcpHands['Pair'] = FourCard(multiCard([[R.ACE, S.SPADE],
                                                    [R.ACE, S.DIAMOND],
                                                    [R.SIX, S.HEART],
                                                    [R.SEVEN, S.CLUB]]))

        self.fcpHands['High'] = FourCard(multiCard([[R.SEVEN, S.SPADE],
                                                    [R.THREE, S.CLUB],
                                                    [R.NINE, S.DIAMOND],
                                                    [R.TWO, S.HEART]]))

    def testBestHands(self):
        handDict = {"High": FourCard.Hand.HIGH,
                    "Pair": FourCard.Hand.PAIR,
                    "TwoPair": FourCard.Hand.TWOPAIR,
                    "Straight": FourCard.Hand.STRAIGHT,
                    "Flush": FourCard.Hand.FLUSH,
                    "Trips": FourCard.Hand.THREEOFKIND,
                    "sFlush": FourCard.Hand.STRAIGHTFLUSH,
                    "FourOfKind": FourCard.Hand.FOUROFKIND}
        for h in handDict:
            self.assertEqual(self.fcpHands[h].bestHand, handDict[h], h)
