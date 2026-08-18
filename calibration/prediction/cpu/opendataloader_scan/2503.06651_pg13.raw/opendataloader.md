![](<2503.06651_pg13_images/imageFile1.png>)

BS sends CSI-RS

BS obtains the full channel

information by SRS and PMI

UE sends SRS

UE feedback PMI and &

BS

BS

BS

H1,s

6

weak ports

strong ports

strong ports

strong ports

weak ports

weak ports

UE

UE

UE

Fig. 12. Illustration of integrated channel estimation method for tri-polarized MIMO.

![](<2503.06651_pg13_images/imageFile2.png>)

Tri-polarized antenna

XX

x

(a)

normalized and then fed back to Tx, given by

$$
H2,D 47) pzejwz
$$

where ρ 2 and ω 2 represents the normalization amplitude and phase, respectively. Similarly, estimated channel for G1 can be normalized with a normalization amplitude and phase of and .

Step 4: Port combining reference value feedback : The estimated channel of antenna ports in G2 by downlink measurement cannot be directly combined with that in G1 due to the unknown combining reference value. Therefore, the Rx needs to feedback the channel combining reference value, denoted by δ , from the full channel information H D , and is given by

$$
(48) eju1
$$

Fig. 13. Illustration of the antenna radiation patterns at UEs. (a) Test scenario. (b) The first two polarizations. (c) The third polarization.

antenna in GI, H1,U, is first normalized as and for channel combining as H1,U ports

estimation accuracy for some antenna ports deteriorates due to variations in antenna gain among different polarizations. To mitigate this issue, a joint uplink-downlink channel estimation method is proposed. As shown in Fig. 12, the main idea of the proposed method involves measuring the channel for port groups with high antenna gain using the uplink channel estimation method, while measuring the channel for port groups with low antenna gain through downlink channel estimation. The specific steps are as follows, illustrated with single-user MIMO system as an example. Step 1: Port grouping : Based on the receive power on Rx’s

each antenna port, the antenna ports are categorized into two distinct groups: one for ports with high antenna gain (marked as G1), and another for those with low antenna gain (marked as G2).

- Step 2: Uplink channel estimation for G1 : The Rx sends pilots through the ports in G1, such that Tx can estimate the channel for corresponding ports, denoted by H 1 , U , by leveraging the channel reciprocity.
- Step 3: Downlink channel measurement for G2 : The Tx sends pilots and then the Rx measures the full-dimension channel H D , which consists of two components corresponding G1 and G2, respectively, denoted by H 1 , D and H 2 , D with H D = [ H 1 , D , H 2 , D ] . Next, the estimated channel for G2 is


$$
= (49 H1,u
$$

As such, the channel for all antenna ports can be obtained as

$$
H= [H1,U, H2,D] 50)
$$

3) Performance Evaluation : We conduct system-level simulation to evaluate the efficiency of our proposed joint uplinkdownlink channel estimation method by taking into account real-world scenarios with tri-polarized MIMO. It is assumed that 50 UEs are randomly distributed in a standard cell with three sectors. The BS and each UE is equipped with 256 and 12 antenna ports respectively. The directional radiation patterns of the tri-polarized antennas used are illustrated in Fig. 13. Other simulation assumptions are detailed in Table I.

Fig. 14 illustrates the cumulative distribution function (CDF) curves of the capacity, comparing a benchmark utilizing uplink channel estimation with the proposed method. It is observable that the capacity of the proposed method consistently surpasses the benchmark across all intervals. Furthermore, it is demonstrated that the average capacity attained by the proposed method is 29% higher than that of the benchmark. This is expected because our proposed method efficiently compensate for the imbalance in receive power among different antenna ports.

