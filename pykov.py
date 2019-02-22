from functools import reduce
from markov_link import MarkovLink
from possible_follow_up import PossibleFollowUp

class Pykov:
    # Order: int, how many words prior are used to determine the next word
    def __init__(self, order):
        self.__links = []
        self.order = order
    # Source: string[], the source to generate a markov chain off of.
    # Each "phrase" is an element in the array.  Phrases do not influence eachother in terms of probabilities.
    # If the source is a continuous block of text (such as a book), then the source should be one element.
    def set_source(self, source):
        self.source = source
        self.__process_source()

    def __process_source(self):
        for phrase in self.source:
            self.__process_phrase(phrase.split())

    def __process_phrase(self, phrase):
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
    def __print_result(self):
        for link in self.__links:
            print("Link:")
            print("\tWords:")
            for word in link.words:
                print("\t\t" + word)
            print("\tPossible follow ups:")
            for possibleFollowUp in link.possibleFollowUps:
                print("\t\tWord: " + possibleFollowUp.word)
                print("\t\tAmount: " + str(possibleFollowUp.amount))