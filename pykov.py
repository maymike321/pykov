from functools import reduce

class Pykov:
    # Order: int, how many words prior are used to determine the next word
    def __init__(self, order):
        self.__links = []
        self.order = order
    # Source: string[], the source to generate a markov chain off of.
    # Each "phrase" is an element in the array.  Phrases do not influence eachother in terms of probabilities.
    # If the source is a continuous block of text (such as a book), then the source should be one element.
    def setSource(self, source):
        self.source = source
        self.__processSource()

    def __processSource(self):
        for phrase in self.source:
            self.__processPhrase(phrase.split())

    def __processPhrase(self, phrase):
        for wordPos in range(len(phrase) - self.order + 1):
            nextWord = None
            if wordPos + self.order < len(phrase):
                nextWord = phrase[wordPos + self.order]
                
            words = phrase[wordPos : wordPos + self.order]
            
            markovLink = next((link for link in self.__links if link.words == words), None)
            if markovLink is not None:
                possibleFollowUp = next((followUp for followUp in markovLink.possibleFollowUps if followUp.word == nextWord), None)
                if possibleFollowUp is not None:
                    possibleFollowUp.amount += 1
                else:
                    if nextWord is not None:
                        markovLink.possibleFollowUps.append(PossibleFollowUp(nextWord))
            else:
                possibleFollowUps = [PossibleFollowUp(nextWord)] if nextWord is not None else []
                markovLink = MarkovLink(words, possibleFollowUps)
                self.__links.append(markovLink)
                
    # For debugging purposes only
    def __printResult(self):
        for link in self.__links:
            print("Link:")
            print("\tWords:")
            for word in link.words:
                print("\t\t" + word)
            print("\tPossible follow ups:")
            for possibleFollowUp in link.possibleFollowUps:
                print("\t\tWord: " + possibleFollowUp.word)
                print("\t\tAmount: " + str(possibleFollowUp.amount))



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

# Represents a possible follow up word to a series of words.  Has a word along with the number of times it is supposed to follow the next word.
class PossibleFollowUp:
    def __init__(self, word, amount = 1):
        self.word = word
        self.amount = amount
    def __eq__(self, other):
        return self.word == other.word and self.amount == other.amount