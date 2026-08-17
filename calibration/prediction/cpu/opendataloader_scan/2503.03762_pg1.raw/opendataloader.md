# D ISPROVING SOME THEOREMS IN S HARMA AND C HAUHAN et al. (2018, 2021) ∗

# Ramy Takieldin Shams

Faculty of Engineering, Ain University, Cairo, Egypt Egypt University of Informatics, New Capital, Cairo, Egypt ramy.farouk@eng.asu.edu.eg

# Patrick Solé

I2M (CNRS, University of Aix-Marseille), 13009 Marseilles, France patrick.sole@telecom-paris.fr

# A BSTRACT

The main objective of this work is to show, through counterexamples, that some of the theorems presented in the papers of Sharma et al. (2018) and Chauhan et al. ( 2021) are incorrect. Although they used these theorems to establish a sufﬁcient condition for a multi-twisted (MT) code to be linear complementary dual (LCD), we show that this condition itself remains valid. We further improve this condition by removing the restrictions on the shift constants and relaxing the required coprimality condition. We show that compared to the previous condition, the modiﬁed condition is able to identify more LCD MT codes. Furthermore, without the need for a normalized set of generators, we develop a formula to determine the dimension of any ρ -generator MT code.

K eywords Multi-twisted code · linear complementary dual · Determinantal divisors · Algebraic coding MSC: 94B05, 94B60, 11T71

# Introduction

Multi-twisted (MT) codes over a ﬁnite ﬁeld F q constitute a signiﬁcant and comprehensive class of linear codes. This class contains several well-known subclasses, including cyclic, constacyclic, quasi-cyclic, quasi-twisted, and generalized quasi-cyclic codes. For some integer ℓ ≥ 1 , let 0   = λ i ∈ F q and m i ≥ 1 for 1 ≤ i ≤ ℓ . If Λ = ( λ 1 ,λ 2 ,...,λ ℓ ) , then a Λ -MT code C with block lengths ( m 1 ,m 2 ,...,m ℓ ) is deﬁned in [1, Deﬁnition 3.1] as a linear code of length n = m 1 + m 2 + ··· + m ℓ that remains invariant under the Λ -MT linear transformation

$$
=1; C2,0, 1 , Ce,me-1) + (X1cl,m1-1, ~2; =1, Ce,me-2 C1,1 , Cl,m17 C2,m2 C1,0 , C1,m17 C2.0 , C2,m27
$$

Throughout this paper, we adopt the same notations as in [1, 2]. Thus, denotes a -MT code over q with block lengths ( m 1 ,m 2 ,...,m ℓ ) . The Euclidean dual C ⊥ of C is a   λ − 1 1 ,λ − 1 2 ,...,λ − 1 ℓ   -MT code with the same block lengths. By using polynomial representation for blocks, C can be regarded as an F q [ x ] -submodule of the Λ -MT module

$$
V = (xm1 X1 , (xm2 (xme i=1
$$

∗ This research was conducted at Université d’Artois, La Faculté Jean Perrin in Lens, and was funded by the Science, Technology & Innovation Funding Authority (STDF); International Cooperation Grants, project number 49294. Ramy Takieldin would like to express his deepest gratitude to Professor André Leroy for his invaluable guidance throughout this project.

