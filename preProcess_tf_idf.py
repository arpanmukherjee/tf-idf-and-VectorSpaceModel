import json
import math
import string

import inflect
import nltk
from nltk.corpus import stopwords

ps = nltk.PorterStemmer()
dgtostr = inflect.engine()
stop_words = stopwords.words('english') + list(string.punctuation)
file_list = [line.rstrip('\n') for line in open('docId.txt')]


def has_digit(input_string):
    return any(char.isdigit() for char in input_string)


def pre_process():
    clean_words = []
    for sentence in file_list:
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
                clean_words.append(ps.stem(w).decode("utf-8"))
            except:
                print w
    return clean_words


with open('model.json') as json_data:
    global_dict = json.load(json_data)


# Removing filename
for id in range(len(file_list)):
    temp = file_list[id].split()
    del(temp[0])
    line = ""
    for i in range(len(temp)-1):
        line += (temp[i]+" ")
    line += temp[len(temp)-1]
    file_list[id] = line

header = pre_process()
doc_len = 467
tf_idf = {}
for key in global_dict:
    templist = [0.0] * doc_len
    for id in range(doc_len):
        tid = str(id).decode("utf-8")
        if tid in global_dict[key].keys():
            if global_dict[key] in header:
                templist[id] = (1 + math.log10(global_dict[key][tid]+100)) * math.log10(
                    float(doc_len) / float(len(global_dict[key])))
            else:
                templist[id] = (1+math.log10(global_dict[key][tid]))*math.log10(float(doc_len)/float(len(global_dict[key])))
    tf_idf[key] = templist
with open('tf_idf.json', 'w') as fp:
    json.dump(tf_idf, fp)
