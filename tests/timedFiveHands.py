import timeit
import unittest


class TestPoker(unittest.TestCase):
    def testRandomHands(self):
        setup = "from cardgames import fivecard;"\
                "from cardgames import fourcard;"\
                "from cardgames import threecard;"\
                "from random import shuffle;"\
                "from cardgames.cards import getDeck;deck = getDeck()"

        test5 = "shuffle(deck);"\
                "fivecard.FiveCard(deck[0:5])"

        test4 = "shuffle(deck);"\
                "fivecard.FiveCard(deck[0:4])"

        test3 = "shuffle(deck);"\
                "fivecard.FiveCard(deck[0:3])"

        print("Five:" + str(timeit.timeit(stmt=test5,
                                          setup=setup, number=100000)))
        print("Four:" + str(timeit.timeit(stmt=test4,
                                          setup=setup, number=100000)))
        print("Three:" + str(timeit.timeit(stmt=test3,
                                           setup=setup, number=100000)))
