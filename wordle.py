
"""
Used the following to download list of words:
    import nltk
    nltk.download()

Then selected "words" under tab "Corpora"
"""
import random
import re
from nltk.corpus import words
from wordle_remove_words import *

game_size = 5

word_list = words.words()
word_list = [each_word.lower() for each_word in word_list]

five_letter_words = [w for w in word_list if (len(w)==game_size and w not in not_common_words)]
#five_letter_words = [w for w in five_letter_words if (w[3:5].lower()=='id' and w[1:2].lower()=='i')]
#print(five_letter_words)
#for w in five_letter_words:
#    print(w)

five_letter_words = list(set(five_letter_words))   # remove duplicates

wordle_answer = five_letter_words[random.randint(0,len(five_letter_words)-1)]

# print(len(word_list)) # 236,736 words
#print(len(five_letter_words))  # 10,422 words

available_letters = 'abcdefghijklmnopqrstuvwxyz'

def start_with(list_of_words):
    # return a "good" starting word: has 3 unique vowels and 5 unique letters
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    has = 3

    # starting words with letters that occur an "average" number of times - trying to quickly cut down remaining words
    #vowels = ['y', 'u', 't', 'm', 'h', 'd', 'o']
    #has = 4

    good_start_words = []
    for w in list_of_words:
        vowel_count = 0
        for v in vowels:
            #match_pattern = '([' + v + '])'
            if re.findall('([' + v + '])', w):
                vowel_count += 1

        if vowel_count >= has and len(set(w)) == game_size:
            good_start_words.append(w)
    return good_start_words

def compare(a,b):
    # check if letters from a are anywhere in b, returns upper case letter to indicate 'not found'
    found_letters = [L if (L in [char for char in b]) else L.upper() for L in [char for char in a]]

    # check if letters from a are in the same position in b, returns letter in correct position
    correct_positions = ['']*game_size
    i = 0
    for x, y in zip(a,b):
        correct_positions[i] = x if x==y else x.upper()
        i += 1
    return found_letters, correct_positions

def display_status(N, N_words, guess, yes_letters, position_info, N_letters_left):
    mystr = f'{N:<3} {N_words:<16} {guess:<7} {yes_letters:<15} '

    for pi in position_info:
        if pi == pi.lower():
            mystr += f'{pi} '
        elif pi == pi.upper():
            mystr += f'_ '

    mystr += f'        {N_letters_left}'

    print(mystr)

# Pick a random word to start with
list_of_start_words = five_letter_words
print(f'Start Words: {len(list_of_start_words)}')
start_word = list_of_start_words[random.randint(0,len(list_of_start_words)-1)]

guessed_word = start_word
must_have_letters = []
debug = False

print('\n--- ---------------- ------- --------------- ----------------- ---------------------')
print(' N   Possible Words   Guess   Known Letters   Known Positions   N Letters Remaining ')
print('--- ---------------- ------- --------------- ----------------- ---------------------')

for i in range(1,15):

    # compare to answer
    letters, positions = compare(guessed_word, wordle_answer)

    # remove letters from available set that were not found in the answer
    remove_letters = [u.lower() for u in letters if u == u.upper()]
    available_letters = [a for a in available_letters if a not in remove_letters]
    must_have_letters.extend([u for u in letters if u == u.lower()])
    must_have_letters = list(set(must_have_letters))

    display_status(i, len(five_letter_words), guessed_word, ''.join(must_have_letters), positions, len(available_letters))

    if guessed_word == wordle_answer:
        print(f'\nCORRECT! ... took {i} guesses to get {wordle_answer.upper()}')
        break

    if debug: print(f"Must have letters: {''.join(must_have_letters)}")
    # pick a word from the word list that contains only the available letters
    if debug: print('Remaining letters: ' + ''.join(available_letters))

    # remove guessed word from list of available words
    try:
        five_letter_words.remove(guessed_word)
    except ValueError:
        pass

    # reduce list of words to ones containing only the available letters
    match_pattern = '[' + ''.join(available_letters) + ']' + '*' + '[' + ''.join(available_letters) + ']'
    five_letter_words = [word for word in five_letter_words if (re.fullmatch(match_pattern,word) is not None)]

    # reduce list further to those that contain the required letters
    if must_have_letters:
        match_pattern = '[' + ''.join(must_have_letters) + ']' + '*' + '[' + ''.join(must_have_letters) + ']'
        five_letter_words = [word for word in five_letter_words if (len(set(must_have_letters) & set(word))==len(must_have_letters))]

    # reduce list further to those that contain any found letter in correct position
    # and remove words where a letter is not in a specific position
    if len(''.join(positions)):
        for index, p in enumerate(positions,0):
            if p == p.lower():
                # lower case result indicates correct letter in correct position
                match_pattern = '(^.{' + str(index) + '}[' + p + '])'
                five_letter_words = [word for word in five_letter_words if re.findall(match_pattern, word) != []]
            elif p == p.upper():
                # upper case result indicates this position is not this letter
                match_pattern = '(^.{' + str(index) + '}[^' + p + '])'
                five_letter_words = [word for word in five_letter_words if re.findall(match_pattern, word) != []]

    if debug: print('-----------------------')

    guessed_word = five_letter_words[random.randint(0,len(five_letter_words)-1)]

