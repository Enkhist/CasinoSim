from cardgames.fivecard import FiveCard
from cardgames.cards import multiCard, Ranks as R, Suits as S, Card
import unittest


class TestPoker(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.fiveHands = {}
        self.fiveHands['RoyalFlush'] = FiveCard(multiCard([[R.TEN, S.SPADE],
                                                           [R.JACK, S.SPADE],
                                                           [R.QUEEN, S.SPADE],
                                                           [R.KING, S.SPADE],
                                                           [R.ACE, S.SPADE]]))

        self.fiveHands['sFlush'] = FiveCard(multiCard([[R.FOUR, S.SPADE],
                                                       [R.FIVE, S.SPADE],
                                                       [R.SIX, S.SPADE],
                                                       [R.SEVEN, S.SPADE],
                                                       [R.EIGHT, S.SPADE]]))

        self.fiveHands['Quads'] = FiveCard(multiCard([[R.ACE, S.SPADE],
                                                      [R.ACE, S.CLUB],
                                                      [R.ACE, S.DIAMOND],
                                                      [R.ACE, S.HEART],
                                                      [R.SEVEN, S.SPADE]]))

        self.fiveHands['FullHouse'] = FiveCard(multiCard([[R.ACE, S.SPADE],
                                                          [R.ACE, S.DIAMOND],
                                                          [R.ACE, S.CLUB],
                                                          [R.KING, S.HEART],
                                                          [R.KING, S.SPADE]]))

        self.fiveHands['Flush'] = FiveCard(multiCard([[R.THREE, S.SPADE],
                                                      [R.EIGHT, S.SPADE],
                                                      [R.FIVE, S.SPADE],
                                                      [R.TWO, S.SPADE],
                                                      [R.JACK, S.SPADE]]))

        self.fiveHands['Straight'] = FiveCard(multiCard([[R.THREE, S.SPADE],
                                                         [R.FOUR, S.CLUB],
                                                         [R.FIVE, S.DIAMOND],
                                                         [R.SIX, S.HEART],
                                                         [R.SEVEN, S.SPADE]]))

        self.fiveHands['Trips'] = FiveCard(multiCard([[R.ACE, S.SPADE],
                                                      [R.ACE, S.CLUB],
                                                      [R.ACE, S.DIAMOND],
                                                      [R.KING, S.SPADE],
                                                      [R.FOUR, S.SPADE]]))

        self.fiveHands['TwoPair'] = FiveCard(multiCard([[R.ACE, S.SPADE],
                                                        [R.ACE, S.CLUB],
                                                        [R.KING, S.DIAMOND],
                                                        [R.KING, S.HEART],
                                                        [R.TWO, S.SPADE]]))

        self.fiveHands['Pair'] = FiveCard(multiCard([[R.ACE, S.SPADE],
                                                     [R.ACE, S.HEART],
                                                     [R.THREE, S.CLUB],
                                                     [R.FOUR, S.CLUB],
                                                     [R.KING, S.CLUB]]))

        self.fiveHands['AceHigh'] = FiveCard(multiCard([[R.KING, S.SPADE],
                                                        [R.THREE, S.CLUB],
                                                        [R.FIVE, S.DIAMOND],
                                                        [R.EIGHT, S.SPADE],
                                                        [R.ACE, S.HEART]]))

        self.fiveHands['HighCard'] = FiveCard(multiCard([[R.TWO, S.SPADE],
                                                         [R.FOUR, S.CLUB],
                                                         [R.FIVE, S.SPADE],
                                                         [R.SIX, S.DIAMOND],
                                                         [R.SEVEN, S.HEART]]))

    def testBestHands(self):
        handDict = {"AceHigh": FiveCard.Hand.HIGH,
                    "HighCard": FiveCard.Hand.HIGH,
                    "Pair": FiveCard.Hand.PAIR,
                    "TwoPair": FiveCard.Hand.TWOPAIR,
                    "Trips": FiveCard.Hand.THREEOFKIND,
                    "Straight": FiveCard.Hand.STRAIGHT,
                    "Flush": FiveCard.Hand.FLUSH,
                    "FullHouse": FiveCard.Hand.FULLHOUSE,
                    "Quads": FiveCard.Hand.FOUROFKIND,
                    "sFlush": FiveCard.Hand.STRAIGHTFLUSH,
                    "RoyalFlush": FiveCard.Hand.ROYALFLUSH}
        for h in handDict:
            self.assertEqual(self.fiveHands[h].getHand(), handDict[h], h)
