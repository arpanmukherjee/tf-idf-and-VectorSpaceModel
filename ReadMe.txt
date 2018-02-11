indexParsing.py file was used for the extraction of filename and header titles. Manually after removal HTML tags, this python script was used for the extraction of file mapping and title, which later was stored in docId.txt.

preProcess.py file was used for the preprocessing, by which model.json file was created. In json file I stored list of term frequency(tf) for each document in a dictionary where key values are unique words after preprocessing. So length of the value list of any word is the document frequency(df).

preProcess_tf_idf.py file was used for creation of tf_idf.json file, which is basically tf-idf matrix. for each unique word I stored it's tf for each doc and idf in that dictionary.

solve_tf_idf.py file was used for the query solving purpose using tf_idf based document retrieval technique.

solve_vector_space.py file was used for the query solving purpose using vector space document retrieval technique.


Assumptions:

i)	In given query if there are n unique words(t1,t2,...,tn), both the techniques will return those files which contains all the unique words. If no documents exist containing all the words, then "Sorry, no documents found!" message will be shown, else based on the technique top 5 relevant documents will be retrieved and stored in cache for later retrieval.

ii)	I added extra 50 tf value for document title prioritization purpose.

iii)	For the cache storing purpose, I assumed program will be in a single execution. If program restarts, then all the cached data stored in the previous execution will be erased.

iv)	Considering all the header title is present in the main file, I did not check manually.