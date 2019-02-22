# Represents a possible follow up word to a series of words.  Has a word along with the number of times it is supposed to follow the next word.
class PossibleFollowUp:
    def __init__(self, word, amount = 1):
        self.word = word
        self.amount = amount
    def __eq__(self, other):
        return self.word == other.word and self.amount == other.amount