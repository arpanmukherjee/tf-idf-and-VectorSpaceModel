# -*- coding:utf-8 -*-
import re
import json
import nltk
import string
import inflect
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()
dgtostr = inflect.engine()
stop_words = stopwords.words('english') + list(string.punctuation)
path = '/home/arpn/Semester 2/Information Retrieval/Assignment 1/testdata'
global_dict = {}


def add_to_dict(words, d_id):
    for w in words:
        if w in global_dict.keys():
            if d_id not in global_dict[w].keys():
                global_dict[w][d_id] = 1
            else:
                global_dict[w][d_id] = global_dict[w][d_id] + 1
        else:
            global_dict[w] = {}
            global_dict[w][d_id] = 1


def has_digit(input_string):
    return any(char.isdigit() for char in input_string)

file_list = [line.rstrip('\n') for line in open('docId.txt')]

for docId in range(len(file_list)):
    print(file_list[docId].split(' ')[0])
    lines = [line.rstrip('\n') for line in open('Dataset/'+file_list[docId].split(' ')[0])]

    clean_words = []
    for sentence in lines:
        try:
            temp_tokens = [i for i in nltk.word_tokenize(sentence.lower().encode('utf-8').strip()) if i not in stop_words]
            tokens = []
            for word in temp_tokens:
                if has_digit(word):
                    for i in nltk.word_tokenize(dgtostr.number_to_words(word)):
                        if i not in stop_words:
                            tokens.append(i)
                else:
                    tokens.append(word)
        except:
            print("Error")
        for w in tokens:
            try:
                clean_words.append(ps.stem(w))
            except:
                print w
    add_to_dict(clean_words, docId)

with open('model.json', 'w') as fp:
    json.dump(global_dict, fp)

print(len(global_dict))
