The key advance of the MILP model is its global optimality guarantee, since it can explore all possible combinations via branch-and-bound. Furthermore, by employing upper and lower bound pruning strategies, MILP significantly reduces ineffective search efforts, thereby enhancing computational efficiency and guaranteeing the identification of the global optimality. However, despite its global optimality, its computational complexity still grows rapidly as the problem size increases with the time complexity O (2 M · K ) . Empirical results show that when M > 50 and K > 100 , the size of the branch-and-bound search tree leads to memory and time costs that exceed practical limits.

Algorithm 2 GRSIP : Greedy Row Selection with Isolated Preselection.

Preselection. Require: G,Nr, An Ensure: Is 1: Initialize: 1 = 0, 2: 3: = arg max gi , s.t. ieTã) 4: 1 =1+1 5: U {i} 6: end while 7: while / < Nr do 8: = st. hk € 9: 1 =1+1 10: = 1l: end while 12: return Is = Ninit , T()= =T()

Hence, in the following we also propose a greedy algorithm in Algorithm 2 with the time complexity O ( MKN r ) . The algorithm starts by choosing N init positions with the top average channel gains for each subcarrier, maintaining a minimum separation of ∆ n between them, where D 1 ( · , · ) represents the minimal ℓ 1 -norm distance between two point

Remark 2 (Applications to Other Models) . The theoretical analysis and algorithms of the two-step framework for FAS proposed in this work could be extended to other problems besides FAS. First, the proposed two-step framework could be directly extended to the antenna selection problem with discrete positions, regardless of whether the exact antennas deployment [38]–[41]. The group-sparse recovery formulation and D-GRIP analysis can be directly adapted to delay-Doppler domain channel estimation [42], [43], where structures induce similar group-wise sparsity patterns in reconstruction. The DC-GOMP algorithm employs a correlation-aware selection mechanism to dynamically resolve coherence conflicts, offering a systematic and efficient approach to sparse event detection. Then, MILP-based spatial equalization offers new insights for the resourceconstrained optimization in RIS configuration on discrete phase [44]. These potential extensions highlight that our methodology effectively tackles the unified challenge of sparsity-aware optimization under structured constraints, making it applicable to a wide range of domains, including computational sensing, adaptive control, and beyond.

# V. S IMULATION R ESULTS

In this section, we present the performance of the proposed group-sparsity based frequency-space channel estimation algorithm, i.e., DC-GOMP, in comparison to two traditional algorithms (OMP, GOMP), under FAS-assisted wideband SIMO system. The proposed positions optimization methods, i.e., MILP and GRSIP, are also evaluated through the physical layer simulations and in terms of BER.

Space Frequency Grid

Recovered by DC-GOMP

Recovered by OMP

Recovered by GOMP

-100

100

f (MHz)

Original Delay-Wavenumber Grid

0.5

"0.5

0.5

Delay

15

-100

-100

f (MHz)

Recovered by DC-GOMP

![](<2503.02004_pg9_images/imageFile1.png>)

0.5

0.5

1

-0.5

1.5

Delay

"J0

f (MHz)

Recovered by OMP

0.5

Delay

1.5

100

-100

0.5

f (MHIz)

Recovered by GOMP

100

Delay

1.5

Figure 2. (1) The first row has four expressions in frequency-space domain. The first one represents the original SFG and the last three represent the recovered version by three different algorithm (our proposed DC-GOMP, OMP and GOMP). (2) Delay-wavenumber domain expressions corresponding to ones above. Black boxes denote the low power regions and red boxes denote the regions failing to correctly allocate the energy.

