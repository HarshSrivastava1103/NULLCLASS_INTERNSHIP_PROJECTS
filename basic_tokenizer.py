# -*- coding: utf-8 -*-
"""Basic Tokenizer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QmEBlMAWhQuaKUDrGv7MyH-fEW_PqYeE

1ST PROJECT FOR NULLCLASS INTERNSHIP - BASIC TOKENIZER
"""

import re #REGULAR EXPRESSION

def tokenize(text):
    #CONVERT TO LOWER CASE
    text = text.lower()
    #HANDLE CONTRACTION
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'m", " am", text)
    text = re.sub(r"'d", " would", text)
    #SEPARATE PUNCTUATION
    text = re.sub(r"([.,!?;:])", r" \1 ", text)

    #SPLIT INTO TOKENS
    tokens = text.split()
    return tokens

#EXample 1
Sample_Text = "Hello, world! Isn't this a great day? We'll have fun."
tokens = tokenize(Sample_Text)
print(tokens)

#EXAMPLE 2
Sample_Text = "Hi there Harsh here working on a project."
tokens = tokenize(Sample_Text)
print(tokens)