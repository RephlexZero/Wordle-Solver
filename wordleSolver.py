import nltk
from collections import Counter

nltk.download('words')

from nltk.corpus import words
import random
import math

def letters_not_in_word(guess, word):
    not_in_word = []
    for letter in guess:
        if letter not in word:
            not_in_word.append(letter)
    return not_in_word

def letters_in_incorrect_positions(guess, word):
    positions = []
    for i, letter in enumerate(guess):
        if letter in word and letter != word[i]:
            positions.append((i, letter))
    return positions

def letters_in_correct_positions(guess, word):
    positions = []
    for i, letter in enumerate(guess):
        if letter == word[i]:
            positions.append((i, letter))
    return positions

# Calculate entropy for each word

desired_length = 5
words = [word.lower() for word in words.words() if len(word) == desired_length]

def calculate_entropy(words):
    # Get frequency distribution of letters in the words
    letter_freq = Counter("".join(words))

    # Calculate the probability of each letter in the words
    letter_probabilities = {letter: letter_freq[letter] / sum(letter_freq.values()) for letter in letter_freq}

    word_entropies = {}  # Create an empty dictionary to store word entropies

    for word in words:
        entropy = -sum(letter_probabilities[letter] * math.log(letter_probabilities[letter], 2) for letter in set(word))
        word_entropies[word] = entropy  # Add word entropy to the dictionary

    return word_entropies

guesses_to_success = []
# Guess loop
while True:
    guessing_words = words.copy()
    random_word = random.choice(guessing_words)
    print("Random word:", random_word)

    guesses_taken = 0
    while True:
        # Recalculate entropy for each word
        guessing_words = calculate_entropy(guessing_words)      
        highest_entropy_word = max(guessing_words, key=guessing_words.get)
        print("Length of guessing set:", len(guessing_words))
        print("Guessed:", highest_entropy_word, "with entropy", guessing_words[highest_entropy_word])
        guesses_taken += 1
        
        # Update guess logic here
        
        if highest_entropy_word == random_word:
            break
        else:
            guessing_words.pop(highest_entropy_word)
            for letter in letters_not_in_word(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if letter not in word]

            for i, letter in letters_in_incorrect_positions(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if letter not in word[i]]

            for i, letter in letters_in_correct_positions(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if word[i] == letter]

    print("Guesses taken:", guesses_taken)
    guesses_to_success.append(guesses_taken)
    print("Average guesses to success:", sum(guesses_to_success) / len(guesses_to_success))