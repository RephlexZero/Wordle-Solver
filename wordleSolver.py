import nltk
from collections import Counter
import random
import math

# Assuming nltk has been downloaded and setup
from nltk.corpus import words

def calculate_letter_probability(word_list, word_length):
    letter_frequency = [Counter() for _ in range(word_length)]
    letter_probability = [Counter() for _ in range(word_length)]

    for word in word_list:
        for i, letter in enumerate(word):
            letter_frequency[i][letter] += 1

    for i in range(word_length):
        total_count = sum(letter_frequency[i].values())
        for letter, count in letter_frequency[i].items():
            letter_probability[i][letter] = count / total_count

    return letter_probability

def calculate_word_entropy(word, letter_probability, word_length):
    entropy = 0
    letter_seen = set()
    for i, letter in enumerate(word):
        if letter not in letter_seen:
            probability = letter_probability[i][letter]
            entropy += -probability * math.log2(probability)
            letter_seen.add(letter)
    return entropy

def cull_word_list(word_list, guessed_word, target_word):
    culled_word_list = []
    for word in word_list:
        match = True
        for i, letter in enumerate(guessed_word):
            if letter == target_word[i]:
                if word[i] != letter:
                    match = False
                    break
            elif letter in target_word:
                if word[i] == letter or letter not in word:
                    match = False
                    break
            else:  # letter not in target_word
                if letter in word:
                    match = False
                    break
        if match:
            culled_word_list.append(word)
    return culled_word_list

def guess_highest_entropy_word(word_entropy_dict):
    return max(word_entropy_dict, key=word_entropy_dict.get)

def main(word_length=5, word_list_length=900):
    word_list = [word.lower() for word in words.words() if len(word) == word_length]
    word_list = random.sample(word_list, k=word_list_length)  # Use sample to avoid duplicates
    target_word = random.choice(word_list)

    letter_probability = calculate_letter_probability(word_list, word_length)
    
    word_entropy_dict = {word: calculate_word_entropy(word, letter_probability, word_length) for word in word_list}
    
    guesses = 0
    print("Guess:\tList Size:")
    while True:
        guesses += 1
        guessed_word = guess_highest_entropy_word(word_entropy_dict)
        print(guessed_word, "\t", len(word_list))
        if guessed_word == target_word:
            print("Correct! In", guesses, "guesses.")
            break
        word_list = cull_word_list(word_list, guessed_word, target_word)
        # Update entropy only for remaining words, using pre-calculated values
        word_entropy_dict = {word: word_entropy_dict[word] for word in word_list}

    return guesses

# For testing and averaging
total_guesses = 0
n_runs = 100
for i in range(n_runs):
    total_guesses += main()
    print("Average after", i + 1, "runs:", round(total_guesses / (i + 1), 2), "\n")
