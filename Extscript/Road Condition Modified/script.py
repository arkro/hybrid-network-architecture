##This script takes an External Movement File and generates mule information from it
##mule info: muleID, trajectory, time taken to move from one cluster to another, waiting time
## at each cluster.

##change the multiplying factor to change the hopTime
## accordingly change the hopTime in the ExternalMovement/externalScript.py file.
## Suppose, initially the hoptime is 4 minutes, after road condition changes the hoptime changes as well.
## So, if the final hoptime is 6 minutes, the multiplyingFactor is 6/4
## if the final hoptime is 3 minutes, the multiplyingFactor is 3/4 and so on.............
## change the multiplying factor accordingly on line 128


idb=[
	(240,830),
	(160,680),
	(150,820),
	(70,660),
	(220,550),
	(310,730),
	(110,550),
	(135,430),
	(200,220),
	(245,370),
	(320,470),
	(360,260),
	(280,155),
	(330,610),
	(555,500),
	(480,615),
	(510,730),
	(25,790),
	(515,850)
]

idb_dict= {}
cluster=19
for i in idb:
	idb_dict[i]=cluster
	cluster+=1

#write idb-location to a file
idb_location= open("idb-location.txt","w")
idb_location.write(str(len(idb))+"\n")
for i in idb:
	s= str(i[0])+" "+str(i[1])
	idb_location.write(s+"\n")
idb_location.close()

f= open("ExternalMovement200AT_v2.txt","r").readlines()
muleCount=38
count=0
while count<9:
	muleID= str(muleCount+count)
	outfile= open("Temp/"+muleID,"w")
	#reduce clutter. simplify. and then write to a file where the only stoppages are idb location
	for i in f:
		search= " "+muleID+" "
		if search in i:
			line= i.split()
			tp= (int(line[-2]),int(line[-1]))
			if tp in idb:
				outfile.write(i)
	#close the file. or you risk reading the file once again in the same script.
	outfile.close()
	#get the unique stoppages
	st= []
	fn= open("Temp/"+muleID,"r").readlines()
	for i in fn:
		line= i.split()
		tp= (int(line[-2]),int(line[-1]))
		st.append(tp)
	#print "li",st
	st= set(st)
	#print "sr",st
	newst=[]
	#correct the order in which it appears
	tmpcount=1
	for i in fn:
		if tmpcount>len(st):
			break
		line= i.split()
		tp= (int(line[-2]),int(line[-1]))
		#print tp,
		if(tp in st and not tp in newst):
			#print "  appended",tp
			newst.append(tp)
			tmpcount+=1
	#print newst
	st= newst
	#print st
	#We have the unique stoppages now. What do we do now?
	#read until the last unique stoppage and then read until the GC.
	readNext= False
	oneMore= False
	oneTrip=[]
	for i in fn:
		#print i
		oneTrip.append(i)		
		line= i.split()
		tp= (int(line[-2]),int(line[-1]))
		if tp==st[-1]:
			readNext= True
		
		if oneMore and tp==st[0]:
			break
		
		if readNext and tp==st[0]:
			oneMore= True

	#print oneTrip
	#store oneTrip in a better format
	oneTripFormatted=[]
	for i in oneTrip:
		line= i.split()
		line=[int(i) for i in line]
		oneTripFormatted.append([line[0],line[1],(line[2],line[3])])
	#print oneTripFormatted
	#now, Just create two lists and store distances ( in seconds ) and wait time
	distances=[]
	waitTime=[]
	k=0
	while k<len(oneTripFormatted):
		if k>0:
			time= oneTripFormatted[k][0] - oneTripFormatted[k-1][0]
			if oneTripFormatted[k][-1] == oneTripFormatted[k-1][-1]:
				waitTime.append(time)
			else:
				distances.append((time*45)/40)
		k+=1
	muleName="ExternalMovement/Mules/Mule"+muleID
	finalFile= open(muleName,"w")
	#print distances
	#print waitTime
	finalFile.write(muleID+"\n")
	tmp=1
	trajectory=[]
	#print idb_dict[oneTripFormatted[0][-1]],
	trajectory.append(idb_dict[oneTripFormatted[0][-1]])
	for i in oneTripFormatted[1:]:
		if not oneTripFormatted[tmp][-1]==oneTripFormatted[tmp-1][-1]:
			#print idb_dict[i[-1]],
			trajectory.append(idb_dict[i[-1]])
		tmp+=1
	traj=""
	for i in trajectory:
		traj+=str(i)+" "
	#print traj
	finalFile.write(traj)
	finalFile.write("\n")
	dist=""
	for i in distances:
		finalFile.write(str(i)+" ")
	finalFile.write("\n")
	for i in waitTime:
		finalFile.write(str(i)+" ")
	count+=1
