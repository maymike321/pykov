from functools import reduce

class Pykov:
    # Order: int, how many words prior are used to determine the next word
    def __init__(self, order):
        self.__links = []
        self.order = order
    # Source: string[], the source to generate a markov chain off of.
    def setSource(self, source):
        self.source = source
        self.__processSource()

    def __processSource(self):
        for x in range(len(self.source) - self.order + 1):
            nextWord = None
            if x + self.order < len(self.source):
                nextWord = self.source[x + self.order]

            words = self.source[x : x + self.order]

            markovLink = next((x for x in self.__links if x.words == words), None)
            if markovLink is not None:
                possibleFollowUp = next((x for x in markovLink.possibleFollowUps if x.word == nextWord), None)
                if possibleFollowUp is not None:
                    possibleFollowUp.amount += 1
                else:
                    if nextWord is not None:
                        markovLink.possibleFollowUps.append(PossibleFollowUp(nextWord))
            else:
                possibleFollowUps = [PossibleFollowUp(nextWord)] if nextWord is not None else []
                markovLink = MarkovLink(words, possibleFollowUps)
                self.__links.append(markovLink)


# Represents one link of a markov chain.  In this context it is a series of words followed by each word that follows it and with what probability.
class MarkovLink:
    def __init__(self, words, possibleFollowUps = []):
        self.words = words
        self.possibleFollowUps = possibleFollowUps
    @property
    def totalAmount(self):
        return reduce(lambda a,b : a + b.amount, self.possibleFollowUps, 0)
    def __eq__(self, other):
        return self.words == other.words and self.possibleFollowUps == other.possibleFollowUps

# Represents a possible follow up word to a series of words.  Has a word along with the number of times it is supposed to follow the next word.
class PossibleFollowUp:
    def __init__(self, word, amount = 1):
        self.word = word
        self.amount = amount
    def __eq__(self, other):
        return self.word == other.word and self.amount == other.amount