The load size of each packet is 64 bytes. The experiment lasts for 600 seconds using CluFlow and each benchmark approach. We count the number of cluster border nodes and the

communication cost, i.e., the number of sent and forwarded IP packets in the border nodes. The results are shown in Fig. 11. Compared with the benchmark approaches, CluFlow utilizes the smallest number of border nodes and communication cost.

# V. R ELATED W ORK

Most existing WSN structures utilize a distributed control system. They are facing the same difﬁculties as traditional wired networks. Existing WSN management does not provide high-level abstraction. Dynamically changing control policy in WSN becomes increasingly difﬁcult as the scale of WSN increases [6]. The research in [15] provides a solution to utilize OpenFlow in wireless networks. It uses the OpenFlow centralized controller for routing data trafﬁc. SDN-WISE [16] designs and implements a complete SDN system in a real multi-hop wireless network. Its SDN components consist of SDN controller, topology manager, protocol stacks, and wireless motes. It provides a stateful solution and reduces the amount of communication between nodes and SDN controllers. The research in [17] creates an SDN framework for IoT systems based on SDN-WISE and Open Network Operating System (ONOS) [18]. To connect IoT and SDN, it extends the functionality of ONOS as the controller in WSN, while the communication protocol relies on SDN-WISE. In these frameworks, the SDN controller must rely on distributed routing to setup control ﬂow in the nodes that are several hops away. To update ﬂow table entries, the nodes and the SDN controller have to exchange request and reply messages over multiple hops periodically. This process causes much communication delay and overhead in wireless networks. Some researches focus on increasing the performance of

WSN, such as energy efﬁciency, task scheduling, routing, etc., using SDN structure. SDN-ECCKN [19] proposes an SDN-based energy management system for WSN. The system reduces the total transmission time to increase the network lifetime. [20] minimizes energy comsumption on sensors with guaranteed quality-of-sensing in multi-task software deﬁned WSN. It utilizes a centralized SDN to formulate the minimumenergy sensor activation by jointly considering sensor activation and task mapping. The work in [21] presents an energyefﬁcient routing algorithm based on the framework of software deﬁned WSN. To minimize the transmission distance and the energy consumption of sensor nodes, the algorithm partitions WSN into clusters and dynamically assigns tasks to the intracluster nodes by a cluster control node.

# VI. C ONCLUSION

We have presented a cluster-based SDN architecture CluFlow to manage communication ﬂow in WSN, by controlling and monitoring the incoming and outgoing ﬂow of cluster border nodes. CluFlow minimizes the number of border nodes and the communication overhead used for SDN control. Based on the simulations and the experiments in a real network, we have demonstrated that CluFlow signiﬁcantly decreases the

# R EFERENCES

[1] B. A. A. Nunes, M. Mendonca, X.-N. Nguyen, K. Obraczka, and T. Turletti, “A survey of software-deﬁned networking: Past, present, and future of programmable networks,” IEEE Communications Surveys & Tutorials , vol. 16, no. 3, pp. 1617–1634, 2014. [2] I. T. Haque and N. Abu-Ghazaleh, “Wireless software deﬁned net-

T. Haque and N. Abu-Ghazaleh, ~Wireless software defined networking: survey and taxonomy; IEEE Communications Surveys no. pp. 2713-2737, 2016.

H. Mostafaei and M. Menth, ~Software-defined wireless works: A survey; Journal of Network and Computer Applications, vol. 119, pp: 42-56, 2018

N. McKeown; I. Anderson; G. Parulkar; L. Peterson; J. Rexford, S. Shenker; and Turner; Openflow: enabling innovation in campus networks, ACM SIGCOMM vol. 38, no. 2, pp. 69-74 2008

Hu, Q. Hao, and K Bao, "A survey on   software-defined  network and openflow: From concept to implementation;" IEEE Communications Surveys & Tutorials; vol. 16, no. 4, pp. 2181-2206, 2014.

Luo, H.-P Tan, and Q. Quek, ~"Sensor   openflow:   Enabling software-defined wireless sensor networks; IEEE Communications letters, vol. 16, no. 11, pp. 1896-1899, 2012

R Rahmani_ H. Rahman, and T. Kanter; "On performance of logical clustering of flow-sensors; International Journal of Computer Science Issues, vol. 10, no. 5, pp. 1-13, 2013.

Y. Breitbart, C.-Y. Chan; M. Garofalakis; R. Rastogi, and A Silber schatz, "Efficiently monitoring bandwidth and latency in ip networks in INFOCOM vol. IEEE, 2001, pp: 933-942

M. R. Garey and D. S. Johnson; Computers and Intractability; A Guide to the Theory of NP-CompletenessNew York, NY, USA: W. H. Freeman & Co., 1990.

lutionary k-way node separators,” in Proceedings of the Genetic and Evolutionary Computation Conference . ACM, 2017, pp. 345–352. [11] Y. Boykov and V. Kolmogorov, “An experimental comparison of min-

Y. Boykov and V. Kolmogorov; "An experimental comparison of mincutmax-flow   algorithms for energy minimization in vision; IEEE transactions on pattern analysis and machine intelligence, vol. 26, no. 9 pp. 124-1137, 2004

G Karakostas "A better   approximation ratio for the vertex cover problem; in International Colloquium On Automata;   Languages; and Programming .

F. Aurenhammer; Voronoi diagramsa survey of a fundamental geometACM Computing Surveys (CSUR), vol. 23, no. 3, pp 345-405, 1991.

T. Winter; P. Thubert, A Brandt; T. Clausen; J. Hui, R. Kelsey, P. Levis, low power and networks_ ROLL Working Group; 2011. lossy

Detti C. Pisa; S. Salsano; and N Blefari-Melazzi, Wireless mesh software defined networks (wmsdn) in WiMob. IEEE, 2013, pp. 89 95

Galluccio; S. Milardo; G. Morabito; and $ Palazzo;   ~Sdn-wise: Design; prototyping and experimentation of stateful  sdn solution for wireless sensor networks; in INFOCOM. IEEE, 2015, pp. 513-521.

A.-C. Anadiotis; Galluccio, Milardo, G. Morabito, and S. Palazzo, Towards a software-defined network operating system for the iot; in Internet of WF-IoT) 2015 IEEE 2nd World Forum IEEE, 2015, pp. 579-584. Things

P- Berde, M Gerola, Hart, Y Higuchi, M Kobayashi_ T. Koide, B. Lantz; B. ~Onos: towards an open; distributed sdn OS in Proceedings of the third workshop Hot topics in software defined networking ACM, 2014, pp_ 1-6.

Y H. Chen; X. Wu; and L. Shu; "An energy-efficient sdn based scheduling algorithm for wsns; Journal of Network and Computer Wang; sleep

[20] D. Zeng, P. Li, S. Guo, T. Miyazaki, J. Hu, and Y. Xiang, “Energy minimization in multi-task software-deﬁned sensor networks,” IEEE transactions on computers , vol. 64, no. 11, pp. 3128–3139, 2015. [21] W. Xiang, N. Wang, and Y. Zhou, “An energy-efﬁcient routing algorithm

for software-deﬁned wireless sensor networks,” IEEE Sensors Journal , vol. 16, no. 20, pp. 7393–7400, 2016.

