import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter

def cascade(G,threshold,num_init_adopters,random_seed):
    q = Queue(maxsize = 0) 
    init_adopters = []
    count_nodes = 0
    for i in G.Nodes():
        count_nodes+=1
    node_is_B = [False] * count_nodes
    #get random nodes
    Rnd = snap.TRnd(random_seed)
    #we want to use same set of init adopters, we dont need  Rnd.Randomize()
    for i in range(0,num_init_adopters):
        nodeId = G.GetRndNId(Rnd)
        init_adopters.append(nodeId)
        node_is_B[nodeId] = True
    for NId in init_adopters:
        node = G.GetNI(NId)
        for node_fd_Id in node.GetOutEdges():
            if not node_is_B[node_fd_Id]:
                q.put((node_fd_Id,1))
    process_num=0
    while q.empty() is False:
        NId, num_ita = q.get()
        if node_is_B[NId]:
            continue
        node = G.GetNI(NId)
        neigh_total=0
        neigh_B=0
        for node_fd_Id in node.GetOutEdges():
            if node_fd_Id == NId:
                continue
            neigh_total+=1
            if node_is_B[node_fd_Id]:
                neigh_B+=1
        if neigh_B/neigh_total >= threshold:
            node_is_B[NId] = True
            for node_fd_Id in node.GetOutEdges():
                if not node_is_B[node_fd_Id]:
                    q.put((node_fd_Id,num_ita+1))
        #process_num+=1
        #if process_num%5000 ==0:
            #print("process "+str(process_num))
    count_B = 0
    for is_B in node_is_B:
        if is_B:
            count_B+=1
    #if (count_B-num_init_adopters) != 0 :
        #print((threshold,count_B,num_init_adopters))
    return (count_B-num_init_adopters)*100/(count_nodes-num_init_adopters)

def cascade_with_init_adopters(G,threshold,init_adopters):
    q = Queue(maxsize = 0) 
    count_nodes = 0
    for i in G.Nodes():
        count_nodes+=1
    node_is_B = [False] * count_nodes
    for NId in init_adopters:
        node_is_B[NId] = True
        node = G.GetNI(NId)
        for node_fd_Id in node.GetOutEdges():
            if not node_is_B[node_fd_Id]:
                q.put((node_fd_Id,1))
    while q.empty() is False:
        NId, num_ita = q.get()
        if node_is_B[NId]:
            continue
        node = G.GetNI(NId)
        neigh_total=0
        neigh_B=0
        for node_fd_Id in node.GetOutEdges():
            if node_fd_Id == NId:
                continue
            neigh_total+=1
            if node_is_B[node_fd_Id]:
                neigh_B+=1
        if neigh_B/neigh_total >= threshold:
            node_is_B[NId] = True
            for node_fd_Id in node.GetOutEdges():
                if not node_is_B[node_fd_Id]:
                    q.put((node_fd_Id,num_ita+1))
    count_B = 0
    for is_B in node_is_B:
        if is_B:
            count_B+=1
    #if (count_B-num_init_adopters) != 0 :
        #print((threshold,count_B,num_init_adopters))
    return (count_B-len(init_adopters))*100/(count_nodes-len(init_adopters))

num_run = 10
num_init_adopters_arr=[1,10,20]
LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "Slashdot0902.txt", 0, 1, '\t')
snap.DelSelfEdges(LoadedGraph)

plt.title("threshold vs cascade percentage")
plt.ylabel('cascade percentage')
plt.xlabel('threshold')
random.seed(datetime.now())
PRankH = snap.TIntFltH()
snap.GetPageRank(LoadedGraph,PRankH)
PRankH_arr=[]
for item in PRankH:
    PRankH_arr.append((item,PRankH[item]))
PRankH_arr.sort(key=itemgetter(1), reverse=True)
try:
    f=open("p3_result.txt","w+")
except:
    print("Some error occurs about open file")

for num_init_adopters in num_init_adopters_arr:
    print("type of initial adopters: key nodes(randomly choose from the 100 largest PRank nodes)")
    print("number of initial adopters: "+str(num_init_adopters))
    print("For each threshold value, create "+str(num_run)+" sets of initial adopters")
    key_nodes_Id=[]
    for i in range(num_run):
        key_nodes_Id.append([])
        for j in range(num_init_adopters):
            random_number = random.randint(0,100)
            while PRankH_arr[random_number][0] in key_nodes_Id[i]:
                random_number = random.randint(0,100)
            key_nodes_Id[i].append(PRankH_arr[random_number][0])
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for num_run_index in range(num_run):
            cascade_percent+=cascade_with_init_adopters(LoadedGraph,threshold,key_nodes_Id[num_run_index])
        cascade_percent = cascade_percent/num_run
        if cascade_percent != 0:
            cascade_percent_arr.append(cascade_percent)
            threshold_arr.append(threshold)
            print("threshold: "+str(threshold)+" cascade percentage(%): "+str(cascade_percent))
            if cascade_percent==100:
                break
    try:
        f.write("type of initial adopters: key nodes(randomly choose from the 100 largest PRank nodes)\n")
        f.write("number of initial adopters: "+str(num_init_adopters)+"\n")
        f.write("For each threshold value, create "+str(num_run)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("threshold: "+str(threshold_arr[i])+" cascade percentage(%): "+str(cascade_percent_arr[i])+"\n")
    except:
        print("Some error occurs about open file")
    plt.plot(threshold_arr,cascade_percent_arr,label="key nodes, num_init="+str(num_init_adopters))

seed_arr = []
for i in range(num_run):
    seed_arr.append(int(100000*random.random()))
for num_init_adopters in num_init_adopters_arr:
    print("type of initial adopters: normal nodes(randomly choose from all nodes)")
    print("number of initial adopters: "+str(num_init_adopters))
    print("For each threshold value, create "+str(num_run)+" sets of initial adopters")
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for num_run_index in range(num_run):
            cascade_percent+=cascade(LoadedGraph,threshold,num_init_adopters,seed_arr[num_run_index])
        cascade_percent = cascade_percent/num_run
        cascade_percent_arr.append(cascade_percent)
        threshold_arr.append(threshold)
        print("threshold: "+str(threshold)+" cascade percentage(%): "+str(cascade_percent))
        if cascade_percent==100:
            break
    try:
        f.write("type of initial adopters: normal nodes(randomly choose from all nodes)\n")
        f.write("number of initial adopters: "+str(num_init_adopters)+"\n")
        f.write("For each threshold value, create "+str(num_run)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("threshold: "+str(threshold_arr[i])+" cascade percentage(%): "+str(cascade_percent_arr[i])+"\n")
    except:
        print("Some error occurs about open file")
    plt.plot(threshold_arr,cascade_percent_arr,label="normal nodes, num_init="+str(num_init_adopters))
plt.legend(title="Number of initial adopters")
try:
    plt.savefig('p3_result.png')
except:
    print("Some error occurs about save image")
plt.show()
#for i in range(len(threshold_arr)):
    #print("threshold: "+str(threshold_arr[i])+" cascade percentage(%): "+str(cascade_percent_arr[i]))