ns = []
fr = open('cikm12-gscholar','rb')
x = False
for line in fr:
	if x:
		n = int(line.strip('\r\n'))
		ns.append(n)
	x = not x
fr.close()
y = len(ns)
ns = sorted(ns,key=lambda x:-x)
print y
print ns[0:10]
print 1.0*sum(ns)/y
print ns[y/2]

# 3rd, 9th

