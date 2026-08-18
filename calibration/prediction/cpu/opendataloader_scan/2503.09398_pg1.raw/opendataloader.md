# Precoder Learning by Leveraging Unitary Equivariance Property

Yilun Ge, Shuyao Liao, Shengqian Han, Chenyang Yang

School of 100191, China Email: { yilunge, shuyaoliao, sqhan, cyyang } @buaa.edu.cn

Abstract —Incorporating mathematical properties of a wireless policy to be learned into the design of deep neural networks (DNNs) is effective for enhancing learning efficiency. Multi-user precoding policy in multi-antenna system, which is the mapping from channel matrix to precoding matrix, possesses a permutation equivariance property, which has been harnessed to design the parameter sharing structure of the weight matrix of DNNs. In this paper, we study a stronger property than permutation equivariance, namely unitary equivariance, for precoder learning. We first show that a DNN with unitary equivariance designed by further introducing parameter sharing into a permutation equivariant DNN is unable to learn the optimal precoder. We proceed to develop a novel non-linear weighting process satisfying unitary equivariance and then construct a joint unitary and permutation equivariant DNN. Simulation results demonstrate that the proposed DNN not only outperforms existing learning methods in learning performance and generalizability but also reduces training complexity. Index Terms —Precoding, deep learning, unitary equivariant,

permutation equivariant

# I. I NTRODUCTION

The optimization of multi-user multi-input multi-output (MU-MIMO) precoder is a challenging problem. Various numerical algorithms have been developed, e.g., the weighted minimum mean square error (WMMSE) algorithm [1], which, however, are with high computational complexity. Deep learning offers a promising solution for optimization

due to its low inference complexity. In [2], a fully-connected deep neural network (DNN) was trained to approximate the performance of WMMSE with significantly reduced inference complexity. However, such DNNs often involve a large number of learnable parameters, requiring extensive training time and massive training samples. Incorporating inductive biases into DNNs architecture with mathematical properties of the policies being learned is crucial for enhancing learning efficiency [3,4]. A well-known example is convolutional neural network (CNN), which leverages the property of translational invariance and has significantly promoted the field of image recognition [5]. Recent studies have demonstrated the importance of inte-

grating permutation equivariance properties to enhance learning efficiency for wireless communications [6–12]. In [8], the mismatch between the inductive bias of CNNs and the permutation equivariance property of the precoding policy was identified, and an edge-updated graph neural network (GNN) was proposed to leverage the permutation equivariance

In this paper, we study the learning of MU-MIMO precoder by investigating a stronger property than permutation equivariance, known as unitary equivariance. This property means that if the channel matrix is multiplied by a unitary matrix, then the optimal precoder will be multiplied by the same unitary matrix. The only instance of a unitary equivariant DNN design was introduced in [13]. However, it lacked a systematic analysis of how the unitary equivariance property impacts DNN design, and its performance in precoder learning is unsatisfactory, as to be demonstrated later. In this paper, we first show that a DNN with a parameter sharing structure derived from the unitary and permutation equivariance property is unable to learn the optimal precoder. To solve the problem, we then develop a non-linear weighting process that satisfies the unitary equivariance, and finally construct a joint unitary and permutation equivariant neural network (UPNN) for precoder learning. Simulation results demonstrate the advantages of the proposed UPNN in performance improvement and training complexity reduction.

# II. E QUIVARIANCE P ROPERTY OF A P RECODING P OLICY

Consider a downlink MU-MIMO system where a base station (BS) equipped with N antennas serves K single-antenna users. The channel matrix is denoted as H = [ h 1 ,..., h K ] ∈ C N × K , where h k ∈ C N × 1 is the channel vector of user k . The precoding matrix is denoted as V = [ v 1 ,..., v K ] ∈ C N × K , where v k ∈ C N × 1 is the precoding vector of user k . The precoder optimization problem that maximizes the sum rate subject to the total power constraint is

$$
max Rk la) k=l
$$

$$
S.t Tr (VHv) Ib) Pmax
$$

where Rk 1 + is the data rate of log2 Em#k

