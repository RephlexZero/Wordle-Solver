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

# Get frequency distribution of letters in the dictionary words
letter_freq = Counter("".join(words))

# Calculate the probability of each letter in the words
letter_probabilities = {letter: letter_freq[letter] / sum(letter_freq.values()) for letter in letter_freq}

def calculate_entropy(word):
    entropy = -sum(letter_probabilities[letter] * math.log(letter_probabilities[letter], 2) for letter in set(word))
    return entropy

# Calculate entropy for each word
word_entropies = {word: calculate_entropy(word) for word in words}
# Sort words by entropy in descending order
sorted_words = sorted(word_entropies.items(), key=lambda x: x[1], reverse=True)

guesses_to_success = []
# Guess loop
while True:
    guessing_words = sorted_words.copy()
    random_word = random.choice(guessing_words)[0]
    print("Random word:", random_word)

    guesses_taken = 0
    while True:
        highest_entropy_word = guessing_words[0][0]
        print("Length of guessing set:", len(guessing_words))
        print("Guessed:", highest_entropy_word)
        guesses_taken += 1
        
        # Update guess logic here
        
        if highest_entropy_word == random_word:
            break
        else:
            guessing_words.pop(0)
            for letter in letters_not_in_word(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if letter not in word[0]]

            for i, letter in letters_in_incorrect_positions(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if letter not in word[0][i]]

            for i, letter in letters_in_correct_positions(highest_entropy_word, random_word):
                guessing_words = [word for word in guessing_words if word[0][i] == letter]

    print("Guesses taken:", guesses_taken)
    guesses_to_success.append(guesses_taken)
    print("Average guesses to success:", sum(guesses_to_success) / len(guesses_to_success))