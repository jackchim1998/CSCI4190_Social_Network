import snap
import random
import sys
from datetime import datetime
from queue import Queue 
import matplotlib.pyplot as plt


LoadedGraph = snap.LoadEdgeList(snap.PUNGraph, "Slashdot0902.txt", 0, 1, '\t')
snap.DelSelfEdges(LoadedGraph)
snap.PrintInfo(LoadedGraph,"stats","info.txt",False)

edge_arr=[]
for NI in LoadedGraph.Nodes():
    count=0
    for Id in NI.GetOutEdges():
        count+=1
    edge_arr.append(count)
plt.title("Distribution of Number of edges")
plt.ylabel('Number of edges')
plt.xlabel('node ID')
plt.plot(edge_arr)
try:
    plt.savefig('p0_result.png')
except:
    print("Some error occurs about save image")
plt.show()

edge_arr.sort()
mini = str(edge_arr[0])
max = str(edge_arr[len(edge_arr)-1])
avg = str(sum(edge_arr)/len(edge_arr))
median = str(edge_arr[int(len(edge_arr)/2)])
num_nodes_with_edge_arr = [0] * (int(max)+1)
for i in edge_arr:
    num_nodes_with_edge_arr[i]+=1
plt.title("Number of nodes vs edge")
plt.ylabel('Number of nodes')
plt.xlabel('Edge')
plt.plot(num_nodes_with_edge_arr)
try:
    plt.savefig('p0_result2.png')
except:
    print("Some error occurs about save image")
plt.show()
print("Minimun number of edges: "+mini)
print("Maximun number of edges: "+max)
print("Avergae number of edges: "+avg)
print("Median number of edges: "+median)
try:
    f=open("p0_result.txt","w+")
    f.write("Minimun number of edges: "+mini+"\n")
    f.write("Maximun number of edges: "+max+"\n")
    f.write("Avergae number of edges: "+avg+"\n")
    f.write("Median number of edges: "+median+"\n")
    for i in range(len(num_nodes_with_edge_arr)):
        f.write(str(num_nodes_with_edge_arr[i])+" nodes have "+str(i)+" edges\n")
except:
    print("Some error occurs about open file")
