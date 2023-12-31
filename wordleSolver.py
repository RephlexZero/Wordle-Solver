import nltk
from collections import Counter

nltk.download('words')

from nltk.corpus import words
import random
import math

def letters_not_in_word(guess, word):
    return [letter for letter in guess if letter not in word]

def letters_in_incorrect_positions(guess, word):
    return [(i, letter) for i, letter in enumerate(guess) if letter != word[i]]

def letters_in_correct_positions(guess, word):
    return [(i, letter) for i, letter in enumerate(guess) if letter == word[i]]

# Calculate entropy for each word

desired_length = 5
words = [word.lower() for word in words.words() if len(word) == desired_length]
# Reduce words by 1 in 10
words = [word for i, word in enumerate(words) if i % 10 == 0]

def calculate_entropy(words):
    word_entropies = {}
    for guess in words:
        search_entropies = {}
        for search in words:
            guessing_words = words.copy()
            for letter in letters_not_in_word(guess, search):
                guessing_words = [word for word in guessing_words if letter not in word]

            for i, letter in letters_in_incorrect_positions(guess, search):
                guessing_words = [word for word in guessing_words if letter != word[i]]

            for i, letter in letters_in_correct_positions(guess, search):
                guessing_words = [word for word in guessing_words if letter == word[i]]

            p = len(guessing_words) / len(words)
            search_entropies[search] = -p * math.log2(p)
        word_entropies[guess] = sum(search_entropies.values()) / len(search_entropies)

        print(guess, word_entropies[guess])
    return word_entropies

calculate_entropy(words)