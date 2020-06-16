import pickle
import re
import nltk
from nltk.corpus import stopwords 
stop = stopwords.words('english')
stemmer = nltk.PorterStemmer()

#Loading source code- Dataset
contents = None

with open('../data/SWT/SWT_content.dat','rb') as load_file :
	contents = pickle.load(load_file)


#Building schema for whoosh search engine
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import SimpleAnalyzer,RegexTokenizer

def preprocess(text):
	punct = '''!"#$%'()*+,-/:;?@[\]^_`{|}~=&'''
	text_remove_punct = ''
	for i in text:
		if i in punct:
			continue

		text_remove_punct+=i

	text_remove_punct = text_remove_punct.lower()
	tokens = re.split(r'[\s\.]+',text_remove_punct)
	tokens_without_stopwords = []
	for i in tokens:
		if i not in stop:
			tokens_without_stopwords.append(i)

	tokens_stemmed = list(map(lambda x:stemmer.stem(x),tokens_without_stopwords))

	return ' '.join(tokens_stemmed)

schema = Schema(title = TEXT(stored=True),path=STORED,content=TEXT(analyzer=RegexTokenizer(r'([a-zA-Z_\.0-9()]+)')))

#Create index for documents
import os, os.path
from whoosh import index

ix = None

if not os.path.exists("../data/SWT/indexdir"):
	os.mkdir("../data/SWT/indexdir")
if not index.exists_in("../data/SWT/indexdir") :
	ix = index.create_in("../data/SWT/indexdir", schema)

else :
	ix = index.open_dir('../data/SWT/indexdir')



#Add Documents
writer = ix.writer()
for i in range(len(contents)) :
	print('title :',contents[i][1])
	print('path :',contents[i][0])
	try:
		writer.add_document(title=preprocess(contents[i][1]),path=contents[i][0], content=preprocess(contents[i][2]))
	except Exception as e:
		print("Add Failed")
		print(e)
		break

	print()
	print()

writer.commit()