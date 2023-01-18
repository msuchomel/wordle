import io
import re
from nltk.corpus import words
from wordle_remove_words import *
import pandas as pd

word_list = words.words()
word_list = [each_word.lower() for each_word in word_list]
five_letter_words = [w for w in word_list if (len(w)==5 and w not in not_common_words)]

# Analyze for most common letters by position

letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z avg'
zeros = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'

 #           letter  total pos1  pos2  pos3  pos4  pos5
list_vals = [letters,zeros,zeros,zeros,zeros,zeros,zeros]
df = pd.read_csv(io.StringIO('\n'.join(list_vals)), delim_whitespace=True)

for w in five_letter_words:
   chars = [char for char in w]
   for i, char in enumerate(chars,1):
      df[char][0] += 1  # total count for this letter
      df[char][i] += 1  # position count for this letter

L = [char for char in letters if char != ' ']


df['avg'] = df.iloc[:,:-1].mean(axis=1)

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)