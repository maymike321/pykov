from functools import reduce
from markov_link import MarkovLink
from possible_follow_up import PossibleFollowUp
import random

class Pykov:
    # Order: int, how many words prior are used to determine the next word
    def __init__(self, order):
        self.__links = []
        self.__startingWords = []
        self.__endingWords = []
        self.__sourceSet = False
        self.__wordEndings = ('.', '!', '?')
        self.order = order
    # Source: string[], the source to generate a markov chain off of.
    # Each "phrase" is an element in the array.  Phrases do not influence eachother in terms of probabilities.
    # If the source is a continuous block of text (such as a book), then the source should be one element.
    def set_source(self, source):
        self.source = source
        self.__process_source()

    def generate_word(self):
        if not self.__sourceSet:
            raise Exception('Source has not been set yet.')

        startingWord = random.choice(self.__startingWords)
        try:
            currentPhrase = random.choice(list(filter(lambda words: words[0] == startingWord, map(lambda links: links.words, self.__links))))
        except:
            print("Offending word is %s" % startingWord)
            raise
        words = list(currentPhrase)
        while currentPhrase[-1] not in self.__endingWords:
            markovLink = next((link for link in self.__links if link.words == currentPhrase), None)
            if markovLink is None:
                raise Exception('Phrase %s was not found in the source but was assumed to be there.  This should never happen.  Yell at a developer somewhere.' % currentPhrase)
                
            nextWord = self.__get_random_next_word_from_link(markovLink)

            words.append(nextWord)

            currentPhrase = currentPhrase[1:]
            currentPhrase.append(nextWord)

        return ' '.join(words)

    def __process_source(self):
        self.__startingWords = []
        self.__endingWords = []
        for phrase in self.source:
            self.__process_phrase(phrase.split())
        self.__get_starting_and_ending_words()
        self.__sourceSet = True

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

    def __get_starting_and_ending_words(self):
        for phrase in self.source:
            splitPhrase = phrase.split()
            for wordPos in range(len(splitPhrase)):
                word = splitPhrase[wordPos]
                if word not in self.__startingWords and self.__is_word_at_position_starting_word(wordPos, splitPhrase):
                    self.__startingWords.append(word)
                if word not in self.__endingWords and self.__is_word_at_position_ending_word(wordPos, splitPhrase):
                    self.__endingWords.append(word)

    def __is_word_at_position_starting_word(self, wordPos, phrase):
        return wordPos <= len(phrase) - self.order and (wordPos == 0 or self.__is_word_at_position_ending_word(wordPos - 1, phrase))
    
    def __is_word_at_position_ending_word(self, wordPos, phrase):
        return wordPos == len(phrase) - 1 or phrase[wordPos].endswith(self.__wordEndings)

    def __get_random_next_word_from_link(self, markovLink):
        randInt = random.randint(1, markovLink.totalAmount)
        currentInt = 0
        for possibleFollowUp in markovLink.possibleFollowUps:
            currentInt += possibleFollowUp.amount
            if randInt <= currentInt:
                return possibleFollowUp.word
        return markovLink.possibleFollowUps[-1].word
                
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