# -*- coding:utf-8 -*-
import nltk
import math
import json
import string
import inflect
from autocorrect import spell
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()
stop_words = stopwords.words('english') + list(string.punctuation)
with open('tf_idf.json') as json_data:
    tf_idf = json.load(json_data)

with open('model.json') as json_data:
    global_dict = json.load(json_data)

doc_len = 467
dgtostr = inflect.engine()
file_list = [line.rstrip('\n') for line in open('docId.txt')]


def get_ith_vector(i):
    return [tf_idf[x][i] for x in tf_idf]


def spell_corrections(input):
    inp = ""
    for i in input:
        inp += spell(i)+" "
    return inp


def has_digit(input_string):
    return any(char.isdigit() for char in input_string)


def calculate_cosine(v1, v2):
    t1 = [(i * i) for i in v1]
    t2 = [(i * i) for i in v2]
    num = 0.0
    for i, j in zip(v1, v2):
        num += (i*j)
    denom = float(math.sqrt(sum(t1)) * math.sqrt(sum(t2)))
    if denom > 0.0:
        return num/denom
    else:
        return 0.0


def is_cache(input_string):
    if input_string not in cache_query:
        return False
    ind = cache_query.index(input_string)
    output_string = cache_ans[ind]
    t_id = ind - 1
    while t_id >= 0:
        cache_query[t_id + 1] = cache_query[t_id]
        cache_ans[t_id + 1] = cache_ans[t_id]
    cache_ans[0] = output_string
    cache_query[0] = input_string
    print(output_string)
    return True


cache_query = []
cache_ans = []

# Vector space creation from tf-idf matrix
vector_space = []
for i in range(doc_len):
    vector_space.append(get_ith_vector(i))
while True:
    ans = ""
    input_string = spell_corrections(raw_input("Please enter the query:").split())
    if is_cache(input_string):
        print("Cache")
        continue
    if len(input_string)==0:
        break
    ans = ans + "Query after spelling correction:"+input_string+"\n"

    temp_tokens = [i for i in nltk.word_tokenize(input_string.lower().encode('utf-8').strip()) if i not in stop_words]
    tokens = []
    for word in temp_tokens:
        if has_digit(word):
            for i in nltk.word_tokenize(dgtostr.number_to_words(word)):
                if i not in stop_words:
                    tokens.append(i)
        else:
            tokens.append(word)
    query_dict = {}
    for w in tokens:
        temp = ps.stem(w)
        if temp in query_dict.keys():
            query_dict[temp] += 1
        else:
            query_dict[temp] = 1


    # Creation of query vector
    query_vector = []
    for key in tf_idf:
        if key in query_dict.keys():
            tf = (1+math.log10(query_dict[key]))
            query_vector.append(tf)
        else:
            query_vector.append(0.0)

    result = {}

    for d_id in range(doc_len):
        result[d_id] = calculate_cosine(query_vector, vector_space[d_id])
        # print(file_list[d_id].split()[0]+" "+str(result[d_id]))

    cnt = 0
    result_set = []
    for key, value in reversed(sorted(result.iteritems(), key=lambda (k, v): (v, k))):
        if cnt == 5:
            break
        result_set.append(key)
        cnt += 1

    if len(result_set) == 0:
        ans = ans + "Sorry, no documents found!\n"
    else:
        ans = ans + "Following documents were retrieved for the given query:\n"
        for item in result_set:
            ans = ans + file_list[item].split()[0]+" with the tf-idf value: "+str(result[item])+"\n"
    cache_query.append(input_string)
    cache_ans.append(ans)
    print(ans)
    if len(cache_query) > 20:
        del (cache_query[-1])
        del (cache_ans[-1])