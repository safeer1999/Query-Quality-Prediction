from whoosh.qparser import QueryParser
from whoosh import index

import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
stemmer = nltk.PorterStemmer()

import xml.etree.ElementTree as ET
tree = ET.parse('../data/SWT/SWTBugRepository.xml')
root = tree.getroot()


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


def replaceSlash(path):
	new_path = path.split('/')
	new_path = '.'.join(new_path)
	return new_path



def removePath(num,path) :
	count =0 
	for i in range(len(path)) :
		if path[i] == '/' :
			count+=1

		if count == num :
			return replaceSlash(path[(i+1):]) 



ix = index.open_dir('../data/SWT/indexdir')



for bug in root :

	print(bug.attrib['id'])

	qp = QueryParser("content", schema=ix.schema)
	if bug[0][1].text == None:
		continue

	query = preprocess(bug[0][1].text)
	q = qp.parse(query)
	actual = [i.text for i in bug.iter('file')]
	
	with ix.searcher() as s:
		results = s.search(q,limit=20)
		for i in results :
			searched = removePath(4,i['path'])
			print(searched)

			if searched in actual :
				print('match')
				break

	print()


