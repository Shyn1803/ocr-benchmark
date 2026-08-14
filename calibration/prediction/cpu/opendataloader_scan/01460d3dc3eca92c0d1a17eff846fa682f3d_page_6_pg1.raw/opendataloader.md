![](<01460d3dc3eca92c0d1a17eff846fa682f3d_page_6_pg1_images/imageFile1.png>)

C 1

C 2

C 3

Cz

C 10

C 6

C 9

C 11

C 12

![](<01460d3dc3eca92c0d1a17eff846fa682f3d_page_6_pg1_images/imageFile2.png>)

C 10

Fig. 5. The network nodes are partitioned into cluster c 1 , c 2 and c 3 . (a) The nodes { v 2 , v 3 , v 4 , v 5 } are the border nodes of cluster c 1 after Step II of Section III-B3b. (b) Node v 1 replaces v 2 and v 3 as the border node.

Fig. 6. (a) The network nodes are partitioned into clusters with different colors. (b) The clusters are abstracted into a cluster-level topology. The nodes in solid blue are vertex cover clusters.

# Algorithm 2: Reduce Redundant Border Nodes

for Each cluster c i do

Calculate MVC on cluster-level topology.

if Border node in non-VC cluster then

Change to the cluster-ID of neighbor VC cluster.

C2 are C1 and C3 are area between with border nodes can replace v2 and 03 as the border node of c1 as shown in Fig. 5(b) to further decrease the total number of border nodes We formalize the approach to reduce redundant border nodes as follows. The main operation flow is shown in 2

(i) We reset the cluster-ID of all the border nodes selected in Section III-B3b to a minimum number of clusters. We convert it to the Minimum Vertex Cover (MVC) problem [12] as follows. In the ﬁrst place, we abstract the clusters into a cluster-level topology as shown in Fig. 6, where each clusterlevel node represents a cluster. If there exists edges between two clusters as in Fig. 6.(a), we connect the two cluster-level nodes. Next, we set the weight of each node in the cluster-level topology. The border nodes in cluster c i are b i after Alg. 1, and we call all the other border nodes that have edge connections with cluster c i as β i . The nodes set b i ∪ β i represents the maximum set of border nodes in c i if re-categorizing the cluster-ID of β i . To concentrate more border nodes in fewer clusters using MVC, we set weight value to each cluster. If the number of all the possible border nodes | b i ∪ β i | is high, we set a low weight value to the cluster c i . In the implementation, we set the weight of cluster c i to 1 / ( | b i ∪ β i | ) . After that, we run the MVC algorithm on the cluster-level topology. If a border node belongs to a non-VC cluster, it changes its cluster-ID to the neighbor VC cluster. To differentiate with the notations before this step, c i changes to c m i after re-categorizing the border nodes, and b changes to b m .

# C. Protocol for Cluster based SD-WSN

CluFlow makes the SDN controller estimate ﬂow among clusters by monitoring the ﬂow at border nodes. The SDN controller controls trafﬁc ﬂow by injecting cluster-level routing rules to the border nodes. The management procedure of the SDN controller and nodes in WSN is shown in Alg. 3. There are at least two beneﬁts of utilizing SDN control in

cluster-level routing. Firstly, compared with SDN management for every node in WSN, CluFlow trades granularity of SDN control for less communication load. Only cluster border nodes communicate with the SDN controller. The number of nodes that communicate with the SDN controller decreases. Secondly, cluster-level routing and local routing are decoupled. The nodes inside the clusters use only distributed local routing and do not need to request ﬂow table entries from the SDN controller. The communication delay caused by requesting ﬂow table entries therefore decreases.

# IV. E XPERIMENTAL S ETUP AND R ESULTS

In this section, we test and evaluate CluFlow in simulation and a real deployed WSN.

# A. Benchmark Approaches

To evaluate the performance of CluFlow, three benchmark approaches are implemented to calculate the communication ﬂow among clusters.

