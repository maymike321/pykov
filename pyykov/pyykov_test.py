import unittest
from .pyykov import Pyykov
from .markov_link import MarkovLink
from .possible_follow_up import PossibleFollowUp

class PyykovTests(unittest.TestCase):
    def setUp(self):
        self.markovGenerator = Pyykov(3)
        self.maxDiff = None

    def test_when_given_single_phrase_parses_correctly(self):
        source = ["The big bad dog was a big bad dog who was a big bad dog who was bad."]
        self.markovGenerator.set_source(source)
        expectedLinks = [
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
        expectedStartingWords = ["The"]
        expectedEndingWords = ["bad."]
        self.assertEqual(expectedLinks, self.markovGenerator._Pyykov__links)
        self.assertEqual(expectedStartingWords, self.markovGenerator._Pyykov__startingWords)
        self.assertEqual(expectedEndingWords, self.markovGenerator._Pyykov__endingWords)

    def test_when_given_multiple_phrases_parses_correctly(self):
        source = [
            "This is the first phrase.",
            "This is the second phrase.  It shouldn't influence the first phrase."
        ]
        self.markovGenerator.set_source(source)
        expectedLinks = [
            MarkovLink(["This", "is", "the"], [PossibleFollowUp("first", 1), PossibleFollowUp("second", 1)]),
            MarkovLink(["is", "the", "first"], [PossibleFollowUp("phrase.", 1)]),
            MarkovLink(["the", "first", "phrase."], []),
            MarkovLink(["is", "the", "second"], [PossibleFollowUp("phrase.", 1)]),
            MarkovLink(["the", "second", "phrase."], [PossibleFollowUp("It", 1)]),
            MarkovLink(["second", "phrase.", "It"], [PossibleFollowUp("shouldn't", 1)]),
            MarkovLink(["phrase.", "It", "shouldn't"], [PossibleFollowUp("influence", 1)]),
            MarkovLink(["It", "shouldn't", "influence"], [PossibleFollowUp("the", 1)]),
            MarkovLink(["shouldn't", "influence", "the"], [PossibleFollowUp("first", 1)]),
            MarkovLink(["influence", "the", "first"], [PossibleFollowUp("phrase.", 1)]),
        ]
        expectedStartingWords = ["This", "It"]
        expectedEndingWords = ["phrase."]
        self.assertEqual(expectedLinks, self.markovGenerator._Pyykov__links)
        self.assertEqual(expectedStartingWords, self.markovGenerator._Pyykov__startingWords)
        self.assertEqual(expectedEndingWords, self.markovGenerator._Pyykov__endingWords)

    def test_recognized_all_ways_to_end_a_sentence(self):
        source = ["This sentence has a period.  This sentence has an exclamation mark!  This sentence has a question mark?"]
        self.markovGenerator.set_source(source)
        expectedEndingWords = ["period.", "mark!", "mark?"]
        self.assertEqual(expectedEndingWords, self.markovGenerator._Pyykov__endingWords)

    def test_when_phrase_ends_without_proper_ending_still_recognizes_ending_word(self):
        source = ["This sentence doesn't have a period oops"]
        self.markovGenerator.set_source(source)
        expectedEndingWords = ["oops"]
        self.assertEqual(expectedEndingWords, self.markovGenerator._Pyykov__endingWords)
    
    def test_when_potential_starting_word_is_too_close_to_end_it_is_removed_as_a_starting_word(self):
        source = ["This is sentence one.  Sentence two."]
        self.markovGenerator.set_source(source)
        expectedStartingWords = ["This"] #note "Sentence" is not expected
        self.assertEqual(expectedStartingWords, self.markovGenerator._Pyykov__startingWords)

class MarkovLinkTests(unittest.TestCase):
    def test_calculates_total_amount_properly(self):
        markovLink = MarkovLink(None, [
            PossibleFollowUp(None, 1),
            PossibleFollowUp(None, 2),
            PossibleFollowUp(None, 9)])
        self.assertEqual(12, markovLink.totalAmount)

if __name__ == '__main__':
    unittest.main()