import re
from nltk.corpus import words
from wordle_remove_words import *

word_list = words.words()
word_list = [each_word.lower() for each_word in word_list]
five_letter_words = [w for w in word_list if (len(w)==5 and w not in not_common_words)]

# Get words that have at least 3 unique vowels, and 5 distinct letters

vowels = ['a','e','i','o','u','y']
good_start_words = []
for w in five_letter_words:
    vowel_count = 0
    for v in vowels:
        match_pattern = '([' + v + '])'
        if re.findall(match_pattern, w):
            vowel_count += 1

    if vowel_count >= 3 and len(set(w))==5:
        good_start_words.append(w)

