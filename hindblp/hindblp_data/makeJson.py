from copy import *
from math import *

class Node:
	tabs = '\t\t\t\t'
	def __init__(self,idx,category,name,rate=0.0,tp='normal'):
		self.idx = idx
		self.category = category
		self.name = name
		self.rate = rate
		self.tp = tp
	def display(self,comma=1):
		s = self.tabs+'{\n'
		s += self.tabs+'\t"category": "'+self.category+'",\n'
		if not self.rate == 0.0:
			s += self.tabs+'\t"rate": '+str(self.rate)+',\n'
		s += self.tabs+'\t"type": "'+self.tp+'",\n'
		s += self.tabs+'\t"name": "'+self.name+'"\n'
		s += self.tabs+'}'
		if comma == 1: s += ','
		s += '\n'
		return s

class Link:
	tabs = '\t\t\t\t'
	def __init__(self,idx,srcNode,tgtNode,rate=0.0,tp='metalink'):
		self.idx = idx
		self.src = srcNode.idx
		self.tgt = tgtNode.idx
		self.rate = rate
		self.tp = tp
	def display(self,comma=1):
		s = self.tabs+'{\n'
		s += self.tabs+'\t"source": '+str(self.src)+',\n'
		s += self.tabs+'\t"target": '+str(self.tgt)+',\n'
		if not self.rate == 0.0:
			s += self.tabs+'\t"rate": '+str(self.rate)+',\n'
		s += self.tabs+'\t"type": "'+str(self.tp)+'"\n'
		s += self.tabs+'}'
		if comma == 1: s += ','
		s += '\n'
		return s

def display_year(year,nodelist,linklist,comma=1):
	tabs = '\t\t'
	s = tabs+'"'+year+'": {\n'
	s += tabs+'\t"nodes": [\n'
	numNode = len(nodelist)
	for i in range(0,numNode-1):
		s += nodelist[i].display()
	s += nodelist[numNode-1].display(0)
	s += tabs+'\t],\n'
	s += tabs+'\t"links": [\n'
	numLink = len(linklist)
	for i in range(0,numLink-1):
		s += linklist[i].display()
	s += linklist[numLink-1].display(0)
	s += tabs+'\t]\n'
	s += tabs+'}'
	if comma == 1: s += ','
	s += '\n'
	return s

if __name__ == '__main__':
	DIR = 'graphdata/'
	MAX_NUM_WORD = 29
	CATEGORY_AFFILIATION = "affiliation"
	CATEGORY_AUTHOR = "author"
	CATEGORY_PAPER = "paper"
	CATEGORY_VENUE = "venue"
	CATEGORY_WORD = "word"
	DEFAULT_WEIGHT_NODE = 0.2
	DEFAULT_WEIGHT_EDGE = 10.0
	DEFAULT_WEIGHT_META_EDGE = 600.0

	nodelist = []
	linklist = []
	year2IDsets = {} # affiliation, author, paper, venue, word, linkidx

	### NODE ###

	node = Node(0,CATEGORY_AFFILIATION,'__'+CATEGORY_AFFILIATION+'__',0.0,'meta')
	nodelist.append(node)
	node = Node(1,CATEGORY_AUTHOR,'__'+CATEGORY_AUTHOR+'__',0.0,'meta')
	nodelist.append(node)
	node = Node(2,CATEGORY_PAPER,'__'+CATEGORY_PAPER+'__',0.0,'meta')
	nodelist.append(node)
	node = Node(3,CATEGORY_VENUE,'__'+CATEGORY_VENUE+'__',0.0,'meta')
	nodelist.append(node)
	node = Node(4,CATEGORY_WORD,'__'+CATEGORY_WORD+'__',0.0,'meta')
	nodelist.append(node)

	affiliationID2node = {}
	category = CATEGORY_AFFILIATION
	fr = open(DIR+'node-affiliation.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		affiliationID = int(arr[0])
		name = arr[1]
		idx = len(nodelist)
		rate = DEFAULT_WEIGHT_NODE
		node = Node(idx,category,name,rate)
		nodelist.append(node)
		affiliationID2node[affiliationID] = node
		idx = len(linklist)
		link = Link(idx,nodelist[0],node,DEFAULT_WEIGHT_META_EDGE)
		linklist.append(link)
	fr.close()

	authorID2node = {}
	category = CATEGORY_AUTHOR
	fr = open(DIR+'node-author.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		authorID = int(arr[0])
		name = arr[1]
		idx = len(nodelist)
		rate = DEFAULT_WEIGHT_NODE
		node = Node(idx,category,name,rate)
		nodelist.append(node)
		authorID2node[authorID] = node
		idx = len(linklist)
		link = Link(idx,nodelist[1],node,DEFAULT_WEIGHT_META_EDGE)
		linklist.append(link)
	fr.close()

	paperID2node = {}
	category = CATEGORY_PAPER
	fr = open(DIR+'node-paper.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		paperID = int(arr[0])
		name = arr[1]
		idx = len(nodelist)
		rate = DEFAULT_WEIGHT_NODE
		node = Node(idx,category,name,rate)
		nodelist.append(node)
		paperID2node[paperID] = node
		idx = len(linklist)
		link = Link(idx,nodelist[2],node,DEFAULT_WEIGHT_META_EDGE)
		linklist.append(link)
	fr.close()

	venueID2node = {}
	category = CATEGORY_VENUE
	fr = open(DIR+'node-venue.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		venueID = int(arr[0])
		name = arr[1]
		idx = len(nodelist)
		rate = DEFAULT_WEIGHT_NODE
		node = Node(idx,category,name,rate)
		nodelist.append(node)
		venueID2node[venueID] = node
		idx = len(linklist)
		link = Link(idx,nodelist[3],node,DEFAULT_WEIGHT_META_EDGE)
		linklist.append(link)
	fr.close()

	wordID2node = {}
	category = CATEGORY_WORD
	fr = open(DIR+'node-word.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		idx = len(nodelist)
		wordID = int(arr[0])
		name = arr[1]
		rate = DEFAULT_WEIGHT_NODE*2.0*(MAX_NUM_WORD-wordID+2)/MAX_NUM_WORD
		node = Node(idx,category,name,rate)
		nodelist.append(node)
		wordID2node[wordID] = node
		idx = len(linklist)
		link = Link(idx,nodelist[4],node,DEFAULT_WEIGHT_META_EDGE)
		linklist.append(link)
		if wordID > MAX_NUM_WORD: # default
			break
	fr.close()

	### EDGE ###

	paperID2year = {}
	paperID2wordID = {}
	paperID2authorID = {}
	authorID2year = {}

	fr = open(DIR+'edge-paper-venue.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		paperID = int(arr[0])
		venueID = int(arr[1])
		year = int(arr[2])
		if not paperID in paperID2node:
			continue
		paperNode = paperID2node[paperID]
		if not venueID in venueID2node:
			continue
		venueNode = venueID2node[venueID]
		rate = 0.0
		award = arr[3]
		if award == 'short': rate = DEFAULT_WEIGHT_EDGE*0.25
		if award == 'full': rate = DEFAULT_WEIGHT_EDGE*0.5
		if award == 'best': rate = DEFAULT_WEIGHT_EDGE
		idx = len(linklist)
		link = Link(idx,paperNode,venueNode,rate,'outer')
		linklist.append(link)
		# year
		if not year in year2IDsets:
			year2IDsets[year] = [set(),set(),set(),set(),set(),set()]
		year2IDsets[year][2].add(paperID)
		year2IDsets[year][3].add(venueID)
		year2IDsets[year][5].add(idx)
		paperID2year[paperID] = year
	fr.close()

	fr = open(DIR+'edge-paper-word.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		paperID = int(arr[0])
		wordID = int(arr[1])
		if not paperID in paperID2node:
			continue
		paperNode = paperID2node[paperID]
		if not wordID in wordID2node:
			continue
		wordNode = wordID2node[wordID]
		rate = DEFAULT_WEIGHT_EDGE*0.001+log(1.0*int(arr[2]))
		idx = len(linklist)
		link = Link(idx,paperNode,wordNode,rate,'inner')
		linklist.append(link)
		# year
		year = paperID2year[paperID]
		year2IDsets[year][4].add(wordID)
		year2IDsets[year][5].add(idx)
	fr.close()

	fr = open(DIR+'edge-paper-author.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		paperID = int(arr[0])
		authorID = int(arr[1])
		if not paperID in paperID2node:
			continue
		paperNode = paperID2node[paperID]
		if not authorID in authorID2node:
			continue
		authorNode = authorID2node[authorID]
		rate = DEFAULT_WEIGHT_EDGE*(0.5+int(arr[2])/int(arr[3]))
		idx = len(linklist)
		link = Link(idx,paperNode,authorNode,rate,'inner')
		linklist.append(link)
		# year
		year = paperID2year[paperID]
		year2IDsets[year][1].add(authorID)
		year_old = 9999
		if authorID in authorID2year:
			year_old = authorID2year[authorID]
		year_old = min(year_old,year)
		authorID2year[authorID] = year_old
		year2IDsets[year][5].add(idx)
	fr.close()

	fr = open(DIR+'edge-author-affiliation.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		authorID = int(arr[0])
		affiliationID = int(arr[1])
		authorNode = authorID2node[authorID]
		affiliationNode = affiliationID2node[affiliationID]
		rate = 0.0
		status = arr[2]
		if status == 'student':
			rate = DEFAULT_WEIGHT_EDGE*0.25
			authorNode.rate = DEFAULT_WEIGHT_NODE
		if status == 'advisor':
			rate = DEFAULT_WEIGHT_EDGE*0.5
			authorNode.rate = DEFAULT_WEIGHT_NODE*1.5
		if status == 'employee':
			rate = DEFAULT_WEIGHT_EDGE*0.5
			authorNode.rate = DEFAULT_WEIGHT_NODE*1.25
		if not authorID in authorID2node:
			continue
		idx = len(linklist)
		link = Link(idx,authorNode,affiliationNode,rate,'outer')
		linklist.append(link)
		# year
		year = authorID2year[authorID]
		year2IDsets[year][0].add(affiliationID)
		year2IDsets[year][5].add(idx)
	fr.close()

	fr = open(DIR+'edge-paper-paper.txt','rb')
	fr.readline()
	for line in fr:
		arr = line.strip('\r\n').split(',')
		paperIDFROM = int(arr[0])
		paperIDTO = int(arr[1])
		if not paperIDFROM in paperID2node:
			continue
		paperNodeFROM = paperID2node[paperIDFROM]
		if not paperIDTO in paperID2node:
			continue
		paperNodeTO = paperID2node[paperIDTO]
		rate = DEFAULT_WEIGHT_EDGE
		idx = len(linklist)
		link = Link(idx,paperNodeFROM,paperNodeTO,rate,'outer')
		linklist.append(link)
		# year
		year = paperID2year[paperIDFROM]
		year2IDsets[year][5].add(idx)
	fr.close()

	fw = open("graph.json",'w')
	s = '{\n'
	s += '\t"data": {\n'
	fw.write(s)
	
	sort_year2IDsets = sorted(year2IDsets.items(),key=lambda x:x[0])
	numYear = len(sort_year2IDsets)
	for i in range(1,numYear):
		for j in range(0,6):
			sort_year2IDsets[i][1][j] = sort_year2IDsets[i][1][j] | sort_year2IDsets[i-1][1][j]
	yearlist = []
	for i in range(0,numYear):
		year = sort_year2IDsets[i][0]
		yearlist.append(str(year))
		mynodelist = deepcopy(nodelist)
		mylinklist = deepcopy(linklist)
		for affiliationID in affiliationID2node:
			if affiliationID in sort_year2IDsets[i][1][0]:
				continue
			node = affiliationID2node[affiliationID]
			mynodelist[node.idx].name = ''
			mynodelist[node.idx].rate = 0.0
		for authorID in authorID2node:
			if authorID in sort_year2IDsets[i][1][1]:
				continue
			node = authorID2node[authorID]
			mynodelist[node.idx].name = ''
			mynodelist[node.idx].rate = 0.0
		for paperID in paperID2node:
			if paperID in sort_year2IDsets[i][1][2]:
				continue
			node = paperID2node[paperID]
			mynodelist[node.idx].name = ''
			mynodelist[node.idx].rate = 0.0
		for venueID in venueID2node:
			if venueID in sort_year2IDsets[i][1][3]:
				continue
			node = venueID2node[venueID]
			mynodelist[node.idx].name = ''
			mynodelist[node.idx].rate = 0.0
		for wordID in wordID2node:
			if wordID in sort_year2IDsets[i][1][4]:
				continue
			node = wordID2node[wordID]
			mynodelist[node.idx].name = ''
			mynodelist[node.idx].rate = 0.0
		for link in mylinklist:
			if link.idx in sort_year2IDsets[i][1][5]:
				continue
			mylinklist[link.idx].tp = 'metalink'
		if i == numYear-1:
			fw.write(display_year(yearlist[i],mynodelist,mylinklist,0))
		else:
			fw.write(display_year(yearlist[i],mynodelist,mylinklist))
	
	s = '\t},\n'
	s += '\t"year_description": [\n'
	for i in range(0,numYear-1):
		s += '\t\t"'+yearlist[i]+'",\n'
	s += '\t\t"'+yearlist[numYear-1]+'"\n'
	s += '\t]\n'
	s += '}\n\n'
	fw.write(s)
	fw.close()

