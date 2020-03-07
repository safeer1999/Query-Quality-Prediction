import pickle

#Loading source code- Dataset
contents = None

with open('AspectJ_content.dat','rb') as load_file :
	contents = pickle.load(load_file)


#Building schema for whoosh search engine
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import SimpleAnalyzer

schema = Schema(title = TEXT(stored=True),path=STORED,content=TEXT(analyzer=SimpleAnalyzer()))

#Create index for documents
import os, os.path
from whoosh import index

ix = None

if not os.path.exists("indexdir"):
	os.mkdir("indexdir")
if not index.exists_in("indexdir") :
	ix = index.create_in("indexdir", schema)

else :
	ix = index.open_dir('indexdir')



#Add Documents
writer = ix.writer()
for i in range(len(contents)) :
	print('title :',contents[i][1])
	print('path :',contents[i][0])
	try:
		writer.add_document(title=contents[i][1],path=contents[i][0], content=contents[i][2])
	except Exception as e:
		print("Add Failed")
		print(e)
		break

	print()
	print()

writer.commit()