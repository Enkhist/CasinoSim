from threecard import ThreeCard
from cards import multiCard, Ranks as R, Suits as S
import unittest


class TestPoker(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.TCPHand = {}
        self.TCPHand['MiniRoyal'] = ThreeCard(multiCard([[R.QUEEN, S.SPADE],
                                                         [R.KING, S.SPADE],
                                                         [R.ACE, S.SPADE]]))

        self.TCPHand['sFlush'] = ThreeCard(multiCard([[R.SEVEN, S.SPADE],
                                                      [R.FIVE, S.SPADE],
                                                      [R.SIX, S.SPADE]]))

        self.TCPHand['Trips'] = ThreeCard(multiCard([[R.ACE, S.SPADE],
                                                     [R.ACE, S.DIAMOND],
                                                     [R.ACE, S.CLUB]]))

        self.TCPHand['Straight'] = ThreeCard(multiCard([[R.TWO, S.SPADE],
                                                        [R.THREE, S.DIAMOND],
                                                        [R.FOUR, S.HEART]]))

        self.TCPHand['Flush'] = ThreeCard(multiCard([[R.QUEEN, S.SPADE],
                                                     [R.SEVEN, S.SPADE],
                                                     [R.TWO, S.SPADE]]))

        self.TCPHand['Pair'] = ThreeCard(multiCard([[R.ACE, S.SPADE],
                                                    [R.ACE, S.DIAMOND],
                                                    [R.SEVEN, S.SPADE]]))

        self.TCPHand['High'] = ThreeCard(multiCard([[R.THREE, S.DIAMOND],
                                                    [R.SEVEN, S.CLUB],
                                                    [R.TWO, S.HEART]]))

    def testBestHands(self):
        handDic = {"High": ThreeCard.Hand.HIGH,
                   "Pair": ThreeCard.Hand.PAIR,
                   "Flush": ThreeCard.Hand.FLUSH,
                   "Straight": ThreeCard.Hand.STRAIGHT,
                   "Trips": ThreeCard.Hand.THREEOFKIND,
                   "sFlush": ThreeCard.Hand.STRAIGHTFLUSH,
                   "MiniRoyal": ThreeCard.Hand.MINIROYAL}
        for hand in handDic:
            self.assertEqual(self.TCPHand[hand].getHand(), handDic[hand], hand)

    def testHandCoarseComparison(self):
        lastHand = None
        for h in self.TCPHand:
            if not lastHand:
                lastHand = h
                continue
            self.assertTrue(self.TCPHand[h] < self.TCPHand[lastHand], h)
            self.assertTrue(self.TCPHand[h] <= self.TCPHand[lastHand], h)
            self.assertFalse(self.TCPHand[h] > self.TCPHand[lastHand], h)
            self.assertFalse(self.TCPHand[h] >= self.TCPHand[lastHand], h)
            lastHand = h

    def testHandFineComparison(self):
        lesser = {}
        lesser["High"] = ThreeCard(multiCard([[R.TWO, S.SPADE],
                                              [R.THREE, S.DIAMOND],
                                              [R.FIVE, S.CLUB]]))
        lesser["Pair"] = ThreeCard(multiCard([[R.SEVEN, S.SPADE],
                                              [R.SEVEN, S.DIAMOND],
                                              [R.THREE, S.CLUB]]))
        lesser["Flush"] = ThreeCard(multiCard([[R.SIX, S.SPADE],
                                               [R.QUEEN, S.SPADE],
                                               [R.TWO, S.SPADE]]))
        lesser["Straight"] = ThreeCard(multiCard([[R.ACE, S.SPADE],
                                                  [R.TWO, S.SPADE],
                                                  [R.THREE, S.CLUB]]))
        lesser["Trips"] = ThreeCard(multiCard([[R.KING, S.SPADE],
                                               [R.KING, S.CLUB],
                                               [R.KING, S.DIAMOND]]))
        lesser["sFlush"] = ThreeCard(multiCard([[R.ACE, S.SPADE],
                                                [R.TWO, S.SPADE],
                                                [R.THREE, S.SPADE]]))
        lesser["MiniRoyal"] = ThreeCard(multiCard([[R.SIX, S.SPADE],
                                                   [R.QUEEN, S.SPADE],
                                                   [R.TWO, S.SPADE]]))
        for h in self.TCPHand:
            if h == "MiniRoyal":
                continue
            self.assertTrue(self.TCPHand[h] > lesser[h], h)
            self.assertTrue(self.TCPHand[h] >= lesser[h], h)
