# Represents one link of a markov chain.  In this context it is a series of words followed by each word that follows it and with what probability.
class MarkovLink:
    def __init__(self, words, possibleFollowUps):
        self.words = words
        self.possibleFollowUps = possibleFollowUps
    @property
    def totalAmount(self):
        return reduce(lambda a,b : a + b.amount, self.possibleFollowUps, 0)
    def __eq__(self, other):
        return self.words == other.words and self.possibleFollowUps == other.possibleFollowUps