# Learning Spatially Adaptive ℓ1-Norms Weights for Convolutional Synthesis Regularization

## arXiv:2503.09483v1 [cs.LG] 12 Mar 2025

Andreas Kofler

Physikalisch-Technische Bundesanstalt (PTB)

Braunschweig and Berlin, Germany andreas.kofler@ptb.de

Christoph Kolbitsch

Physikalisch-Technische Bundesanstalt (PTB)

Braunschweig and Berlin, Germany christoph.kolbitsch@ptb.de

Luca Calatroni

MaLGa Center, DIBRIS, Universit`a di Genova, MMS, Istituto Italiano di Tecnologia, Genoa, Italy luca.calatroni@unige.it

Kostas Papafitsoros

School of Mathematical Sciences Queen Mary University of London London, UK k.papafitsoros@qmul.ac.uk

Abstract—We propose an unrolled algorithm approach for learning spatially adaptive parameter maps in the framework of convolutional synthesis-based ℓ1 regularization. More precisely, we consider a family of pre-trained convolutional filters and estimate deeply parametrized spatially varying parameters applied to the sparse feature maps by means of unrolling a FISTA algorithm to solve the underlying sparse estimation problem. The proposed approach is evaluated for image reconstruction of lowfield MRI and compared to spatially adaptive and non-adaptive analysis-type procedures relying on Total Variation regularization and to a well-established model-based deep learning approach. We show that the proposed approach produces visually and quantitatively comparable results with the latter approaches and at the same time remains highly interpretable. In particular, the inferred parameter maps quantify the local contribution of each filter in the reconstruction, which provides valuable insight into the algorithm mechanism and could potentially be used to discard unsuited filters.

Index Terms—Neural Networks, Convolutional Dictionary Learning, Sparsity, Adaptive Regularization, Low-Field MRI

I. INTRODUCTION

Convolutional Sparse Coding (CSC) and Convolutional Dictionary Learning (CDL) approaches [1] rely on the assumption that the signal/image of interest x ∈ RN (or CN) is wellapproximated by a linear combination of convolutions of normalized filters dk ∈ Rk

f×kf with sparse feature maps sk ∈ RN (or CN) for k = 1,...,K, that is

K

dk ∗ sk, where ∀k sk is sparse. (1)

x ≈

k=1

The project (22HLT02 A4IM) has received funding from the European Partnership on Metrology, co-financed from the European Union’s Horizon Europe Research and Innovation Programme and by the Participating States. LC acknowledges the financial support of the European Research Council (grant MALIN, 101117133).

By enforcing sparsity by means of ℓ1-regularization, given a set of signals {xl}Ll=1 and some λ > 0, the CDL problem can be thus typically formulated as:

L

K

L

K

- 1

- 2


dk ∗ sk,l∥22 + λ

∥sk,l∥1 such that ∥dk∥2 = 1, ∀k = 1,...,K.

∥xl −

min

(2)

{dk},{sk}

l=1

k=1

l=1

k=1

In the context of image reconstruction, given possibly incomplete observed data y ∈ V modeled as the noisy output of a linear forward operator A : V → W, CDL and CSC are employed as variational regularization methods, see e.g. [2]:

- 1

- 2∥Ax − y∥22+


min

x,{dk},{sk}

K

K

(3)

α 2

∥x − dk ∗ sk∥22 + λ

∥sk∥1 such that ∥dk∥2 = 1, ∀k = 1,...,K,

k=1

k=1

where α > 0 enforces the synthesis constraint. Note that in (3) it is implicitly assumed that the underlying sparsifying model is unknown so that the elements x,{dk},{sk}, k = 1...,K are reconstructed jointly, typically by alternating the minimization between solving (2) and computing the current update of desired image depending on the estimated dictionary. These methods are thus often referred to as blind Compressed Sensing approaches, see, e.g. [3] for MRI applications.

Problem (3) is a non-convex optimization problem whose solution is, typically, computationally demanding, and further requires careful tuning of the regularization parameters λ, α, initializations x0,{d0k},{s0k} and, depending on the algorithms considered, possibly also of other parameters coupling the image update and the CSC and CDL, see, e.g. [4] for ADMM schemes. Furthermore, the regularization parameter λ dictates the strength of the imposed regularization in terms of the sparsity of the feature maps only globally and independently

