Antenna array

array

![](<2503.07090_pg2_images/imageFile1.png>)

BS

The massive MIMO system.

systems [24], which can also be viewed as a kind of symplectic optimization, to solve the constrained optimization problem and provide an algorithm. The proposed algorithm achieves a faster rate than gradient descent. Simulation results indicate that the proposed precoder achieves a satisfying WSR performance while maintaining the smoothness of the effective channel. Meanwhile, the proposed precoder design exhibits lower computational complexity in comparison with traditional precoder designs. The rest of this paper is orgnized as follows: Section

II presents the problem formulation of CSPD. Section III proposes the precoder design with symplectic optimization. Section IV presents simulation results illustrating the benefits of the CSPD. The paper concludes in Section V. Notations : The conjugate, transpose and hermitian of matrix

A are denoted as A ∗ , A T and A H , respectively. The trace of A is represented as the operator tr( A ) . The identity matrix of size M × M is denoted as I M . The operation diag( a ) constructs a square diagonal matrix with the elements of vector a on its main diagonal. Additionally, A = Bdiag { A 1 , ··· , A N } creates a block diagonal matrix with blocks A 1 , ··· , A N along its main diagonal.

# P ROBLEM F ORMULATION

In this section, we formulate the CSPD as an optimization problem which balances the WSR performance and the smoothness of the effective channels.

# A. System Model

We consider a single-cell massive multiple-input multipleoutput (MIMO) system consists of a BS equipped with a uniform planar array (UPA) comprising M = M z M x antennas, where M x and M z denote the number of horizontal and vertical antennas, respectively. The BS serves K singleantenna users. Orthogonal frequency division multiplexing (OFDM) modulation is employed. The number of subcarriers is N c , and N v subcarriers are allocated for data transmission. Each time slot contains N b OFDM symbols, and the channel parameters remain constant within each OFDM symbol but vary across different symbols. The diagram of the massive MIMO system is depicted in Fig.1

# B. Per-subcarrier Precoder Design

Let p c k ∈ C M × 1 and x k,c denote the precoding vector and the transmitted signal of the k -th user at the c -th subcarrier, respectively. The transmitted signal after precoding can be presented as

$$
K k=l Xk.c
$$

The channel vector from the BS to user k at the c -th subcarrier is defined as h k,c . The received signal y k,c of user k at the c -th subcarrier can be presented as

$$
Uk,c hk,cXk,c + K Zk,c
$$

where the noise z k,c is distributed as CN (0 ,σ 2 z ) . We treat the aggregate interference-plus-noise z ′ k,c = h k,c K   l ̸ = k p c l x l,c + z k,c as Gaussian noise. Let Γ k,c be denoted as the variance of z ′ k,c , we have

we have

$$
K =02 + (3) lk Tkc
$$

Assuming that user k can obtain Γ k,c . The rate of user k at the c -th subcarrier can be computed as

$$
=1 H Rk c
$$

To maximize the WSR for each subcarrier, the problem formulation of the conventional per-subcarrier precoder design with total power constraint is given as

$$
K PK = arg max Wk k=l K s.t.
$$

where w k is used to ensure the fairness of different users and P c is the power budget at c -th subcarrier. Since the precoders in (5) are designed independently for each subcarrier, the smoothness of the resulting frequency domain effective channels is not satisfied. This implies a weak correlation among effective channels, thereby complicating effective channel estimation and signal detection at the receiver.

# C. CSPD with Channel Smoothing

To significantly improve the performance of the channel estimation and signal detection, we optimize precoders across subcarriers, and the smoothness of the frequency domain effective channel is considered as a objective function in the optimization problem. The delay spread can be adjusted by setting related parameters. Let p be a vector stacked by p c as p =

Let pk be vector stacked by as pk € and Hk be block diagonal  matrix   defined as Hk Bdiag {hk,1 , hk,Nv} € CMNv

