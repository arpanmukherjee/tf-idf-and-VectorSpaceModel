# -*- coding:utf-8 -*-
import nltk
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

doc_len = 467
dgtostr = inflect.engine()


def getPosting(query):
    postingList = {}
    for word in query:
        if word not in tf_idf:
            continue
        temp_list = []
        for id in range(doc_len):
            if tf_idf[word][id] > 0.0:
                temp_list.append(id)
        postingList[word] = temp_list
    return postingList


def spell_corrections(input):
    inp = ""
    for i in input:
        inp += spell(i)+" "
    return inp


def has_digit(input_string):
    return any(char.isdigit() for char in input_string)


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
while True:
    ans = ""
    input_string = spell_corrections(raw_input("Please enter the query:").split())
    if is_cache(input_string):
        continue

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
    query = []
    for w in tokens:
        query.append(ps.stem(w))
    d = getPosting(query)
    int_id = set([i for i in range(467)])
    flag = False
    for word in d:
        if len(d[word]) > 0:
            flag = True
        int_id = int_id & set(d[word])
    if flag == False:
        int_id.clear()
    result = {}
    for id in int_id:
        temp = 0
        for word in query:
            if word not in tf_idf:
                continue
            temp += tf_idf[word][id]
        result[id] = temp

    # print(len(result))
    cnt = 0
    result_set = []
    for key, value in reversed(sorted(result.iteritems(), key=lambda (k, v): (v, k))):
        if cnt == 5:
            break
        result_set.append(key)
        cnt += 1

    file_list = [line.rstrip('\n') for line in open('docId.txt')]
    if len(result_set) == 0:
        ans = ans + "Sorry, no documents found!\n"
    else:
        ans = ans + "Following documents were retrieved for the given query:\n"
        for item in result_set:
            ans = ans + file_list[item].split()[0]+" with the tf-idf value: "+str(result[item])+"\n"

    cache_query.insert(0, input_string)
    cache_ans.insert(0, ans)
    print(ans)
    if len(cache_query) > 20:
        del(cache_query[-1])
        del(cache_ans[-1])
