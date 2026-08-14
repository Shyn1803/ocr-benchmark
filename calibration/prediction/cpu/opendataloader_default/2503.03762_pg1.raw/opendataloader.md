![](<2503.03762_pg1_images/imageFile1.png>)

DISPROVING SOME THEOREMS IN SHARMA AND CHAUHAN et al. (2018, 2021)∗

![](<2503.03762_pg1_images/imageFile2.png>)

arXiv:2503.03762v1 [cs.IT] 24 Feb 2025

Ramy Takieldin Faculty of Engineering, Ain Shams University, Cairo, Egypt Egypt University of Informatics, New Capital, Cairo, Egypt ramy.farouk@eng.asu.edu.eg

Patrick Solé I2M (CNRS, University of Aix-Marseille), 13009 Marseilles, France patrick.sole@telecom-paris.fr

ABSTRACT

The main objective of this work is to show, through counterexamples, that some of the theorems presented in the papers of Sharma et al. (2018) and Chauhan et al. ( 2021) are incorrect. Although they used these theorems to establish a sufﬁcient condition for a multi-twisted (MT) code to be linear complementary dual (LCD), we show that this condition itself remains valid. We further improve this condition by removing the restrictions on the shift constants and relaxing the required coprimality condition. We show that compared to the previous condition, the modiﬁed condition is able to identify more LCD MT codes. Furthermore, without the need for a normalized set of generators, we develop a formula to determine the dimension of any ρ-generator MT code.

Keywords Multi-twisted code · linear complementary dual · Determinantal divisors · Algebraic coding MSC: 94B05, 94B60, 11T71

1 Introduction

Multi-twisted (MT) codes over a ﬁnite ﬁeld Fq constitute a signiﬁcant and comprehensive class of linear codes. This class contains several well-known subclasses, including cyclic, constacyclic, quasi-cyclic, quasi-twisted, and general-

ized quasi-cyclic codes. For some integer ℓ ≥ 1, let 0 = λi ∈ Fq and mi ≥ 1 for 1 ≤ i ≤ ℓ. If Λ = (λ1,λ2,...,λℓ), then a Λ-MT code C with block lengths (m1,m2,...,mℓ) is deﬁned in [1, Deﬁnition 3.1] as a linear code of length n = m1 + m2 + ··· + mℓ that remains invariant under the Λ-MT linear transformation

TΛ :(c1,0,c1,1,...,c1,m

ℓ−1)  → (λ1c1,m

1−1;c2,0,c2,1,...,c2,m

2−1;...;cℓ,0,cℓ,1,...,cℓ,m

1−2;λ2c2,m

2−2;...;λℓcℓ,m

ℓ−2).

1−1,c1,0,...,c1,m

2−1,c2,0,...,c2,m

ℓ−1,cℓ,0,...,cℓ,m

Throughout this paper, we adopt the same notations as in [1, 2]. Thus, C denotes a Λ-MT code over Fq with block lengths (m1,m2,...,mℓ). The Euclidean dual C⊥ of C is a λ−1 1,λ−2 1,...,λ−ℓ 1 -MT code with the same block lengths. By using polynomial representation for blocks, C can be regarded as an Fq[x]-submodule of the Λ-MT module

ℓ

Fq[x] xmi − λi

Fq[x] xm1 − λ1

Fq[x] xm2 − λ2

Fq[x] xmℓ − λℓ

V =

=

⊕

⊕ ··· ⊕

.

![](<2503.03762_pg1_images/imageFile3.png>)

![](<2503.03762_pg1_images/imageFile4.png>)

![](<2503.03762_pg1_images/imageFile5.png>)

![](<2503.03762_pg1_images/imageFile6.png>)

i=1

![](<2503.03762_pg1_images/imageFile7.png>)

∗This research was conducted at Université d’Artois, La Faculté Jean Perrin in Lens, and was funded by the Science, Technology & Innovation Funding Authority (STDF); International Cooperation Grants, project number 49294. Ramy Takieldin would like to express his deepest gratitude to Professor André Leroy for his invaluable guidance throughout this project.

