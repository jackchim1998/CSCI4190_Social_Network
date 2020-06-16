import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt

num_test_per_threshold = 10
num_init_adopters_arr = [1,10,30,60,100]

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


LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "Slashdot0902.txt", 0, 1, '\t')
snap.DelSelfEdges(LoadedGraph)
#make array of random seed to make sure different threshold use same num_test_per_threshold sets of init adopters
seed_arr = []
random.seed(datetime.now())
for i in range(num_test_per_threshold):
    seed_arr.append(int(100000*random.random()))
#for each pair of threshold and number of initial adopters, average the cascading percentage of num_test_per_threshold sets
plt.title("threshold vs cascade percentage")
plt.ylabel('cascade percentage')
plt.xlabel('threshold')
try:
    f=open("p1_result.txt","w+")
except:
    print("Some error occurs about open file")
for num_init_adopters in num_init_adopters_arr:
    print("number of initial adopters: "+str(num_init_adopters))
    print("For each threshold value, create "+str(num_test_per_threshold)+" sets of initial adopters")
    cascade_percent_arr = []
    threshold_arr = []
    for threshold in reversed(range(99)):
        if threshold > 20 and ((threshold+1)%5)!=0:
            continue
        threshold = (threshold+1)/100
        cascade_percent = 0
        for seed_index in range(len(seed_arr)):
            cascade_percent += cascade(LoadedGraph,threshold,num_init_adopters,seed_arr[seed_index])
        cascade_percent = cascade_percent/len(seed_arr)
        cascade_percent_arr.append(cascade_percent)
        threshold_arr.append(threshold)
        print("threshold: "+str(threshold)+" cascade percentage(%): "+str(cascade_percent))
        if cascade_percent==100:
            break
    plt.plot(threshold_arr, cascade_percent_arr, label = str(num_init_adopters))
    try:
        f.write("number of initial adopters: "+str(num_init_adopters)+"\n")
        f.write("For each threshold value, create "+str(num_test_per_threshold)+" sets of initial adopters\n")
        for i in range(len(threshold_arr)):
            f.write("threshold: "+str(threshold_arr[i])+" cascade percentage(%): "+str(cascade_percent_arr[i])+"\n")
    except:
        print("Some error occurs about open file")
plt.legend(title="Number of initial adopters")
try:
    plt.savefig('p1_result.png')
except:
    print("Some error occurs about save image")
plt.show()