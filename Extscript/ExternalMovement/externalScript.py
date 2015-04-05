##This script generates the external movement file from the information of the mules in "Mules/" directory.
##Uncomment the hoptime or change it accordingly.

import os,random

outfile= open("externalMovement.txt","w")

#compare function to sort according to the time stamps
def compare(a,b):
    return a[0]-b[0]

#read the co-ordinates of the IDB's
idb={}
f= open("idb-location.txt","r").read().splitlines()
numIDB= int(f[0])
f.remove(f[0])
i=1

for point in f :
    line= [ int(k) for k in point.split()]
    print line
    if(len(line)>0):
    	x,y= line[0],line[1]
    	idb[i]=(x,y)
    i+=1

#Read the number of dataMules, HopTime and Simulation Time
#Read the number of mules by reading the number of files in the Mules directory
os.chdir('Mules')
mules= len(os.listdir(os.getcwd()))
#mules= 9
#print mules, "[mules]"
os.chdir('..')
id_info= open("id_info","r").readlines()
muleStart= int(id_info[0])

##print the wifi info to the file
wifi_nodes= [int(i)-20 for i in id_info[1].split()]

print wifi_nodes

wifi_id= numIDB*2
for i in wifi_nodes:
    outfile.write("0  "+str(wifi_id)+"  "+str(idb[i][0])+"  "+str(idb[i][1])+"\n")
    wifi_id+=1


fileStart=muleStart
#hopTime=420
hopTime = 1680
#original hop-time= 240
#hopTime=120
#hopTime=150
#hopTime=180
#hopTime=210
#hopTime=240
#hopTime=270
#hopTime=300
#hopTime=330
#hopTime=360
#hopTime=60
simulationTime= 80000
#Generate External Movement file
#Approach: Generate movement data for individual data mule and store them
#Sort these data according to the time Stamp and write them to the output file
count=0
moveMent=[]
while count<(mules):
    filename="Mules/Mule"+str(count+ fileStart)
    muleInfo= open(filename,"r").read().splitlines()
    muleInfo=[i.split('[')[0].strip() for i in muleInfo]
    muleID= int(muleInfo[0])
    trajectory= [int(i)-20 for i in muleInfo[1].split()]
    distance=[ int(i) for i in muleInfo[2].split()]
    serviceTime= [int(i) for i in muleInfo[3].split()]
    totalTime= simulationTime
    time= 0
    moveMent.append([time,muleID,idb[trajectory[0]]])
    if(len(trajectory)<2):
        break
    k=0
    prev=0
    while time<=totalTime:
        #take the difference between current time and previous time
        #previous time= time when a data mule starts moving from an IDB towards the next IDB
        diff= time-prev
        if (diff==(distance[k])):
            parts= diff/hopTime
            initial_x,initial_y= idb[trajectory[k]][0], idb[trajectory[k]][1]
            final_x,final_y= idb[trajectory[k+1]][0], idb[trajectory[k+1]][1]
            for midi in xrange(1,parts):
                m=midi
                n= parts-midi
                path_x = (m*final_x+ n*initial_x)/(m+n)
                path_y = (m*final_y+ n*initial_y)/(m+n)
                moveMent.append([prev+midi*hopTime,muleID, (path_x, path_y)])
            moveMent.append([time,muleID, idb[trajectory[k+1]]])
            time+=serviceTime[k]
            moveMent.append([ time,muleID, idb[trajectory[k+1]]])
            prev=time
            k+=1
        time+=hopTime
        #re-assign k to 0 when the data mule reaches the group centre
        #because we are generating external movement data for each mule upto simulation time
        #and then we are merging them together
        if(k==len(distance)):
            k=0
    count+=1
#sort the list according to the time-stamps
moveMent= sorted(moveMent,cmp=compare)
#write the data in file
##outfile= open("externalMovement.txt","w")
for i in moveMent:
    output=str(i[0])+" "+str(i[1])+" "+str(i[2][0])+" "+str(i[2][1])
    outfile.write(output)
    outfile.write("\n")
outfile.close()
