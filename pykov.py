class Pykov:
    # Order: int, how many words prior are used to determine the next word
    def __init__(self, order):
        self.__links = []
        self.order = order
    # Source: string[], the source to generate a markov chain off of.
    def setSource(self, source):
        self.source = source
        for x in range(len(self.source) - self.order):
            nextWord = None
            if len(self.source) != x + self.order:
                nextWord = self.source[x + self.order]
                
            words = self.source[x : x + self.order]

            markovLink = next((x for x in self.__links if x.words == words), None)
            if markovLink is not None:
                possibleFollowUp = next((x for x in markovLink.possibleFollowUps if x.word == nextWord), None)
                if possibleFollowUp is not None:
                    possibleFollowUp.amount += 1
                else:
                    markovLink.possibleFollowUps.append(PossibleFollowUp(nextWord))
            else:
                markovLink = MarkovLink(words, [PossibleFollowUp(nextWord)])
                self.__links.append(markovLink)


# Represents one link of a markov chain.  In this context it is a series of words followed by each word that follows it and with what probability.
class MarkovLink:
    def __init__(self, words, possibleFollowUps = []):
        self.words = words
        self.possibleFollowUps = possibleFollowUps

# Represents a possible follow up word to a series of words.  Has a word along with the number of times it is supposed to follow the next word.
class PossibleFollowUp:
    def __init__(self, word, amount = 1):
        self.word = word
        self.amount = amount
