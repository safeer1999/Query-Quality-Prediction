import os
import sys
import pickle
import re

path = "../data/AspectJ"

fname = []
for root,d_names,f_names in os.walk(path):
	for f in f_names:
		fname.append((os.path.join(root, f),re.search("^[^.]*",f,flags=re.IGNORECASE).group()))

#print(len(fname))
#print(fname[0])
content = []

for i in range(1,len(fname),1) :
	try :
		print(fname[i][1])
		file = open(fname[i][0],'r')
		content.append((fname[i][0],fname[i][1],file.read()))

	except UnicodeDecodeError :
		print('Skipped since it is not a unicode encoded file')
		pass

	finally :
		file.close()

#print(fname[1],':\n\n',content)

print()
print()
print(len(content))


with open('AspectJ_content.dat','wb') as save_file :
	pickle.dump(content,save_file)

print('Completed saving contents')