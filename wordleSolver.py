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

def letters_in_word(guess, word):
    positions = []
    for i, letter in enumerate(word):
        if letter in guess:
            positions.append((i, letter))
    return positions

def letters_in_correct_positions(guess, word):
    positions = []
    for i, letter in enumerate(guess):
        if letter == word[i]:
            positions.append((i, letter))
    return positions

# Calculate entropy for each word
# Lowercase words
words = [word.lower() for word in words.words()]
word_entropies = {}
for word in words:
    word_counts = Counter(word)
    word_total_count = sum(word_counts.values())
    word_probabilities = {letter: count / word_total_count for letter, count in word_counts.items()}
    word_entropy = -sum(p * math.log2(p) for p in word_probabilities.values())
    word_entropies[word] = word_entropy

# Sort words by entropy in descending order
sorted_words = sorted(word_entropies.items(), key=lambda x: x[1], reverse=True)

# Guess loop
desired_length = 5
guessing_words = [word for word in sorted_words.copy() if len(word[0]) == desired_length]

# Print top 10 guessing words
print("Top 10 guessing words:")
for word in guessing_words[:10]:
    print(word)

random_word = random.choice(guessing_words)[0]
print("Random word:", random_word)

guesses_taken = 0
while True:
    highest_entropy_word = guessing_words[0][0]
    print("Guessing:", highest_entropy_word)
    guesses_taken += 1
    print("Guesses taken:", guesses_taken)
    
    # Update guess logic here
    
    if highest_entropy_word == random_word:
        break
    else:
        # Remove guessed word from guessing words
        guessing_words.pop(0)

        # Remove words with letters_not_in_word
        guessing_words = [word for word in guessing_words if not letters_not_in_word(highest_entropy_word, random_word)]

        # Remove words without letters_in_word
        guessing_words = [word for word in guessing_words if letters_in_word(highest_entropy_word, random_word)]

        # Remove words without letters_in_correct_positions in correct positions

        
print("Guesses taken:", guesses_taken)





