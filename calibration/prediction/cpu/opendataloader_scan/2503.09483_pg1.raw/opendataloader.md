# Learning Spatially Adaptive ℓ 1 -Norms Weights for Convolutional Synthesis Regularization

Andreas Kofler

Physikalisch-Technische Bundesanstalt (PTB) Braunschweig and Berlin, Germany andreas.kofler@ptb.de

Christoph Kolbitsch Physikalisch-Technische Bundesanstalt (PTB) Braunschweig and Berlin, Germany christoph.kolbitsch@ptb.de

christoph kolbitsch @ptb.de

Abstract —We propose an unrolled algorithm approach for learning spatially adaptive parameter maps in the framework of convolutional synthesis-based ℓ 1 regularization. More precisely, we consider a family of pre-trained convolutional filters and estimate deeply parametrized spatially varying parameters applied to the sparse feature maps by means of unrolling a FISTA algorithm to solve the underlying sparse estimation problem. The proposed approach is evaluated for image reconstruction of lowfield MRI and compared to spatially adaptive and non-adaptive analysis-type procedures relying on Total Variation regularization and to a well-established model-based deep learning approach. We show that the proposed approach produces visually and quantitatively comparable results with the latter approaches and at the same time remains highly interpretable. In particular, the inferred parameter maps quantify the local contribution of each filter in the reconstruction, which provides valuable insight into the algorithm mechanism and could potentially be used to discard unsuited filters.

Index Terms —Neural Networks, Convolutional Dictionary Learning, Sparsity, Adaptive Regularization, Low-Field MRI

# I. I NTRODUCTION

Convolutional Sparse Coding (CSC) and Convolutional Dictionary Learning (CDL) approaches [1] rely on the assumption that the signal/image of interest x ∈ R N (or C N ) is wellapproximated by a linear combination of convolutions of normalized filters d k ∈ R k f × k f with sparse feature maps s k ∈ R N (or C N ) for k = 1 ,...,K , that is

$$
K X ~ dk * Sk, where Vk Sk is sparse. k=l
$$

The project (22HLTO2 A4IM) has   received funding from the   European Partnership on Metrology; co-financed Europe Research and Innovation Programme and by the Participating States (grant MALIN, 101117133). from Luca Calatroni MaLGa Center; DIBRIS , Università di Genova; MMS, Istituto Italiano di Tecnologia, Genoa, Italy luca.calatroni @unige.it Kostas Papafitsoros School of Mathematical Sciences Queen Mary University of London London, UK k-papafitsoros = qmul.ac.uk By enforcing sparsity by means of 41-regularization; given a be thus typically formulated as:

$$
K K min dk * {dk} {sk 2 l=l k=l l=l k=l (2) such that Vk = 1 K.
$$

In the context of image reconstruction, given possibly incomplete observed data y ∈ V modeled as the noisy output of a linear forward operator A : V → W , CDL and CSC are employed as variational regularization methods, see e.g. [2]:

$$
min x,{dk } {sk} 2lAx_ yll2+ K K Q (3) Ilx = dk * 2 k=l k=l such that Vk = 1, K,
$$

where α > 0 enforces the synthesis constraint. Note that in (3) it is implicitly assumed that the underlying sparsifying model is unknown so that the elements x , { d k } , { s k } , k = 1 ...,K are reconstructed jointly, typically by alternating the minimization between solving (2) and computing the current update of desired image depending on the estimated dictionary. These methods are thus often referred to as blind Compressed Sensing approaches, see, e.g. [3] for MRI applications. Problem (3) is a non-convex optimization problem whose

solution is, typically, computationally demanding, and further requires careful tuning of the regularization parameters λ , α , initializations x 0 , { d 0 k } , { s 0 k } and, depending on the algorithms considered, possibly also of other parameters coupling the image update and the CSC and CDL, see, e.g. [4] for ADMM schemes. Furthermore, the regularization parameter λ dictates the strength of the imposed regularization in terms of the sparsity of the feature maps only globally and independently

