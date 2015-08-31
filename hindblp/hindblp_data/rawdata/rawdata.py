def done1():
	authornameset = set()
	papertitleset = set()
	fr = open('rawdata1.txt','rb')
	line = 'NA'
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		for authorname in line.split(','):
			authornameset.add(authorname)
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		papertitle = line
		papertitleset.add(papertitle)
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
	fr.close()
	fw = open('rawdata2.txt','w')
	for authorname in sorted(authornameset):
		fw.write(authorname+'\n')
	fw.close()
	fw = open('rawdata3.txt','w')
	for papertitle in sorted(papertitleset):
		fw.write(papertitle+'\n')
	fw.close()

def done2():
	word2freq = {}
	fr = open('rawdata3.txt','rb')
	line = 'NA'
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		myline = line.lower()
		l = len(myline)
		word = ''
		for i in range(0,l):
			if myline[i].isalpha():
				word += myline[i]
			else:
				if len(word) > 0:
					if not word in word2freq:
						word2freq[word] = 0
					word2freq[word] += 1
				word = ''
		if len(word) > 0:
			if not word in word2freq:
				word2freq[word] = 0
			word2freq[word] += 1
	fr.close()
	fw = open('word2freq1.txt','w')
	for word,freq in sorted(word2freq.items(),key=lambda x:-x[1]):
		fw.write(word+','+str(freq)+'\n')
	fw.close()
	
def done3():
	wordset = set()
	fr = open('rawdata5.txt','rb')
	for line in fr:
		word = line.strip('\r\n')
		if len(word) > 0 and word.isalpha():
			wordset.add(word)
	fr.close()
	fw = open('stopword.txt','w')
	for word in sorted(wordset):
		fw.write(word+'\n')
	fw.close()
	fw = open('word2freq2.txt','w')
	fr = open('word2freq1.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		word = arr[0]
		if not word in wordset:
			fw.write(line.strip('\r\n')+'\n')
	fr.close()
	fw.close()
	
def done4():
	wordset = set()
	fr = open('word2freq2.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		word = arr[0]
		wordset.add(word)
	fr.close()
	fw = open('abstractword.txt','w')
	fr = open('rawdata3.txt','rb')
	line = 'NA'
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		fw.write(line+'\n')
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		fw.write(line+'\n')
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		word2freq = {}
		myline = line.lower()
		l = len(myline)
		word = ''
		for i in range(0,l):
			if myline[i].isalpha():
				word += myline[i]
			else:
				if word in wordset:
					if not word in word2freq:
						word2freq[word] = 0
					word2freq[word] += 1
				word = ''
		if word in wordset:
			if not word in word2freq:
				word2freq[word] = 0
			word2freq[word] += 1
		s = ''
		if len(word2freq) > 0:
			for word,freq in sorted(word2freq.items(),key=lambda x:-x[1]):
				s += ';'+word+','+str(freq)
			s = s[1:]
		fw.write(s+'\n')
	fr.close()

def rawdata2():
	authornameset = set()
	authorname2i = {}
	affiliationnameset = set()
	affiliationname2i = {}
	authorinfo = []
	fr = open('rawdata2.txt','rb')
	line = 'NA'
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		authorname = line
		authornameset.add(authorname)
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		for segment in line.split(';'):
			arr = segment.split(',')
			affiliationname,location,status = arr[0],arr[1],arr[2]
			affiliationname = affiliationname+','+location
			affiliationnameset.add(affiliationname)
			authorinfo.append([authorname,affiliationname,status])
	fr.close()
	authornamelist = sorted(authornameset)
	l = len(authornamelist)
	for i in range(0,l):
		authorname = authornamelist[i]
		authorname2i[authorname] = i
	affiliationnamelist = sorted(affiliationnameset)
	l = len(affiliationnamelist)
	for i in range(0,l):
		affiliationname = affiliationnamelist[i]
		affiliationname2i[affiliationname] = i
	authorinfoi = []
	for authorname,affiliationname,status in authorinfo:
		authorinfoi.append([authorname2i[authorname],affiliationname2i[affiliationname],status])
	fw = open('node-author.txt','w')
	fw.write('ID,NAME\n')
	for authorname,i in sorted(authorname2i.items(),key=lambda x:x[1]):
		fw.write(str(i)+','+authorname+'\n')
	fw.close()
	fw = open('node-affiliation.txt','w')
	fw.write('ID,NAME,LOCATION\n')
	for affiliationname,i in sorted(affiliationname2i.items(),key=lambda x:x[1]):
		fw.write(str(i)+','+affiliationname+'\n')
	fw.close()
	fw = open('edge-author-affiliation.txt','w')
	fw.write('ID_AUTHOR,ID_AFFILIATION,STATUS\n')
	for authornamei,affiliationnamei,status in sorted(authorinfoi,key=lambda x:x[0]):
		fw.write(str(authornamei)+','+str(affiliationnamei)+','+status+'\n')
	fw.close()

def abstractword():
	word2i = {}
	fr = open('word2freq2.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		word = arr[0]
		if not word in word2i:
			word2i[word] = len(word2i)
	fr.close()
	fw = open('node-word.txt','w')
	fw.write('ID,WORD\n')
	for word,i in sorted(word2i.items(),key=lambda x:x[1]):
		fw.write(str(i)+','+word+'\n')
	fw.close()
	fw1 = open('node-paper.txt','w')
	fw2 = open('edge-paper-word.txt','w')
	fw1.write('ID,NAME,TITLE\n')
	fw2.write('ID_PAPER,ID_WORD,FREQUENCY\n')
	fr = open('abstractword.txt','rb')
	line = 'NA'
	i = 0
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		title = line
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		name = line
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		fw1.write(str(i)+','+name+','+title+'\n')
		for segment in line.split(';'):
			arr = segment.split(',')
			word,freq = arr[0],int(arr[1])
			fw2.write(str(i)+','+str(word2i[word])+','+str(freq)+'\n')
		i += 1
	fr.close()
	fw2.close()
	fw1.close()

def rawdata4():
	papername2i = {}
	fr = open('node-paper.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		i,papername = int(arr[0]),arr[1]
		papername2i[papername] = i
	fr.close()
	paperi2j = {}
	fr = open('rawdata4.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split(',')
		papername = arr[0]
		i = papername2i[papername]
		papername = arr[1]
		j = papername2i[papername]
		if not i in paperi2j:
			paperi2j[i] = set()
		paperi2j[i].add(j)
	fr.close()
	fw = open('edge-paper-paper.txt','w')
	fw.write('ID_FROM,ID_TO\n')
	for i,jset in sorted(paperi2j.items(),key=lambda x:x[0]):
		for j in sorted(jset):
			fw.write(str(i)+','+str(j)+'\n')
	fw.close()

def rawdata1():
	authorname2i = {}
	fr = open('node-author.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		i,authorname = int(arr[0]),arr[1]
		authorname2i[authorname] = i
	fr.close()
	papertitle2i = {}
	fr = open('node-paper.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		i,papertitle = int(arr[0]),arr[2]
		papertitle2i[papertitle] = i
	fr.close()
	venueset = set()
	venue2i = {}
	submissioninfo = []
	i2j = {}
	fr = open('rawdata1.txt','rb')
	line = 'NA'
	while line:
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		authorilist = []
		arr = line.split(',')
		for authorname in arr:
			authorilist.append(authorname2i[authorname])
		numauthor = len(authorilist)
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		papertitle = line
		paperi = papertitle2i[papertitle]
		i2j[paperi] = []
		for orderi in range(0,numauthor):
			authori = authorilist[orderi]
			i2j[paperi].append([authori,orderi+1,numauthor])
		line = fr.readline().strip('\r\n')
		if len(line) == 0: break
		arr = line.split(',')
		venue = arr[0]+','+arr[1]
		venueset.add(venue)
		year,award = int(arr[2]),arr[3].lower()
		submissioninfo.append([paperi,venue,year,award])
	fr.close()
	venue2i = {}
	venuelist = sorted(venueset)
	l = len(venuelist)
	for i in range(0,l):
		venue = venuelist[i]
		venue2i[venue] = i
	fw = open('node-venue.txt','w')
	fw.write('ID,NAME,ASSOCIATION\n')
	for venue,i in sorted(venue2i.items(),key=lambda x:x[1]):
		fw.write(str(i)+','+venue+'\n')
	fw.close()
	fw = open('edge-paper-author.txt','w')
	fw.write('ID_PAPER,ID_AUTHOR,ORDER,NUM_AUTHOR\n')
	for [paperi,item] in sorted(i2j.items(),key=lambda x:x[0]):
		for [authori,orderi,numauthor] in sorted(item,key=lambda x:x[1]):
			fw.write(str(paperi)+','+str(authori)+','+str(orderi)+','+str(numauthor)+'\n')
	fw.close()
	fw = open('edge-paper-venue.txt','w')
	fw.write('ID_PAPER,ID_VENUE,YEAR,AWARD\n')
	for paperi,venue,year,award in sorted(submissioninfo,key=lambda x:x[0]):
		venuei = venue2i[venue]
		fw.write(str(paperi)+','+str(venuei)+','+str(year)+','+award+'\n')
	fw.close()
	
if __name__ == '__main__':
	rawdata2()
	abstractword()
	rawdata4()
	rawdata1()

