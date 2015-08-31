Node:
	author: name
	affiliation: name,location (CMU/Tsinghua)(Pittsburgh/New York/Beijing)
	paper: title,name,abstract
	venue(conference/journal): name,association (KDD/TKDE)(IEEE/ACM)
Edge:
	<author,affiliation>: status (student/advisor/employee)
	<author,paper>: order (1st/2nd)
	<paper,venue>: year,award (2014/2015)(best/full/short/poster)
	<paper,paper>: citation
	
rawdata1
	L1: names {name,order} (author)
	L2: title (paper)
	L3: name,association,year,award (venue)
rawdata2
	L1: name (author)
	L2: name,location,status (affiliation)
rawdata3
	L1: title (paper)
	L2: name (paper)
	L3: abstract (paper)
rawdata4
	L: name1 (paper) - cites - name2 (paper)
	