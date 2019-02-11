import unittest
from pykov import Pykov, MarkovLink, PossibleFollowUp

class PykovTests(unittest.TestCase):
    def setUp(self):
        self.markovGenerator = Pykov(3)
        self.maxDiff = None
    def test_when_given_small_source_parses_correctly(self):
        source = ["The", "big", "bad", "dog", "was", "a", "nerd."]
        self.markovGenerator.setSource(source)
        expected = [
            MarkovLink(["The", "big", "bad"], [PossibleFollowUp("dog", 1)]),
            MarkovLink(["big", "bad", "dog"], [PossibleFollowUp("was", 1)]),
            MarkovLink(["bad", "dog", "was"], [PossibleFollowUp("a", 1)]),
            MarkovLink(["dog", "was", "a"], [PossibleFollowUp("nerd.", 1)]),
            MarkovLink(["was", "a", "nerd."], []),
        ]
        self.assertEqual(expected, self.markovGenerator._Pykov__links)
    def test_when_given_source_with_multiple_repeats_parses_correctly(self):
        source = ["The", "big", "bad", "dog", "was", "a", "big", "bad", "dog", "who", "was", "a", "big", "bad", "dog", "who", "was", "bad."]
        self.markovGenerator.setSource(source)
        expected = [
            MarkovLink(["The", "big", "bad"], [PossibleFollowUp("dog", 1)]),
            MarkovLink(["big", "bad", "dog"], [PossibleFollowUp("was", 1), PossibleFollowUp("who", 2)]),
            MarkovLink(["bad", "dog", "was"], [PossibleFollowUp("a", 1)]),
            MarkovLink(["dog", "was", "a"], [PossibleFollowUp("big", 1)]),
            MarkovLink(["was", "a", "big"], [PossibleFollowUp("bad", 2)]),
            MarkovLink(["a", "big", "bad"], [PossibleFollowUp("dog", 2)]),
            MarkovLink(["bad", "dog", "who"], [PossibleFollowUp("was", 2)]),
            MarkovLink(["dog", "who", "was"], [PossibleFollowUp("a", 1), PossibleFollowUp("bad.", 1)]),
            MarkovLink(["who", "was", "a"], [PossibleFollowUp("big", 1)]),
            MarkovLink(["who", "was", "bad."], []),
        ]
        self.assertEqual(expected, self.markovGenerator._Pykov__links)

if __name__ == '__main__':
    unittest.main()