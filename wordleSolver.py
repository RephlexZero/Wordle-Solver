import nltk
from collections import Counter

nltk.download('words')

from nltk.corpus import words
import random
import math

def calculate_letter_probability(words, word_length):
    letter_frequency = [Counter() for _ in range(word_length)]
    letter_probability = [Counter() for _ in range(word_length)]

    for word in words:
        for i, letter in enumerate(word):
            letter_frequency[i][letter] += 1

    for i in range(word_length):
        total_count = sum(letter_frequency[i].values())
        for letter, count in letter_frequency[i].items():
            letter_probability[i][letter] = count / total_count

    return letter_probability


def calculate_word_entropy(word, letter_probability):
    entropy = 0
    for i, letter in enumerate(word):
        probability = letter_probability[i][letter] / word.count(letter)
        entropy += -probability * math.log2(probability)
    return entropy

def calculate_word_entropy_dict(words, letter_probability):
    word_entropy_dict = {}

    for word in words:
        entropy = calculate_word_entropy(word, letter_probability)
        word_entropy_dict[word] = entropy

    return word_entropy_dict

def cull_word_list(word_list, guessed_word, target_word):
    for i, letter in enumerate(guessed_word):
        if letter == target_word[i]:
            word_list = [word for word in word_list if word[i] == letter]
        elif letter in target_word:
            word_list = [word for word in word_list if word[i] != letter]
        elif letter not in target_word:
            word_list = [word for word in word_list if letter not in word]
    return word_list

def guess_highest_entropy_word(word_entropy_dict):
    return max(word_entropy_dict, key=word_entropy_dict.get)

def __main__(word_length=5, word_list_length=900):
    word_list = [word.lower() for word in words.words() if len(word) == word_length]
    # Make the list of length k with random words, real wordle is k = 900
    word_list = random.choices(word_list, k=word_list_length)
    # Choose a random word from the list
    target_word = random.choice(word_list)

    letter_probability = calculate_letter_probability(word_list, word_length)
    word_entropy_dict = calculate_word_entropy_dict(word_list, letter_probability)
    
    guesses = 0
    print("Guess:\tList Size:")
    while (True):
        guesses += 1
        guessed_word = guess_highest_entropy_word(word_entropy_dict)
        print(guessed_word,"\t", len(word_list))
        if guessed_word == target_word:
            print("Correct! In", guesses, "guesses.")
            return guesses
        word_list = cull_word_list(word_list, guessed_word, target_word)
        # letter_probability = calculate_letter_probability(word_list, word_length)
        word_entropy_dict = calculate_word_entropy_dict(word_list, letter_probability)

total_guesses = 0
for i in range(100):
    total_guesses += __main__()
    print("Average:", round(total_guesses / (i + 1), 2),"\n")
 


