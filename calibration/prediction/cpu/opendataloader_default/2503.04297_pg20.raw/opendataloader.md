20 COLINE EMPRIN AND ALEX TAKEDA

so [φ] is a class in FkH−1(griL h). We now consider the maps

h Li+1h + Fk+1h

h Li+1h

←− f FkH−1

→ FkH−1

FkH−1 griL h → FkH−1

![](<2503.04297_pg20_images/imageFile1.png>)

![](<2503.04297_pg20_images/imageFile2.png>)

h Li+1Fkh + Fk+1h

![](<2503.04297_pg20_images/imageFile3.png>)

The last group is where the k-th intermediate gauge triviality class ϑik lives. But the image of this class in FkH−1(h/Li+1h + Fk+1h) is equal to the image of [φ] ∈ FkH−1(griL h), which vanishes by assumption. Therefore, to show that all classes ϑik vanish, it is suﬃcient to show that the map f is injective. Suppose we have [α] ∈ ker(f). Then we can ﬁnd λ such that

dψλ ≡ α (mod Li+1h + Fk+1h). Let us set λ′ = λ(k−1) + λ(k) + ··· Since dψ is homogeneous of weight one, we must have dψ λ′ ≡ α (mod Li+1h + Fk+1h), since α is in Fkh. Thus λ′ is a primitive of α in h/Li+1Fkh + Fk+1h.

2.3. Application to formality of properadic algebras. The aim of the present article is to study the (intrinsic) coformality properties of Deﬁnition 1.33. To do so, we will use the obstruction theories developed in Section 2.1. Beforehand, let us recall the approach of formality as a deformation problem. In all this section, the ring R is a Q-algebra. Let C be a reduced weight-graded dg coproperad, e.g. C = Y(n)¡. Given any chain complex (A,dA), we have a convolution dg Lie admissible algebra

![](<2503.04297_pg20_images/imageFile4.png>)

gA = HomS C,EndA ,∂,⋆ , whose Maurer–Cartan elements are in bijection with ΩC-structures on A. Recall that an ∞-morphism between two ΩC-algebra structures is an ∞-isotopy if its ﬁrst component is the identity. We denote by ΓA the set of all ∞-isotopies. The existence of gauge equivalences between Maurer–Cartan elements in gA corresponds to existence of ∞-isotopies between the corresponding ΩC-structures thanks to the following theorem.

Theorem 2.14 ([3, Theorem 2.16]). If R is a Q-algebra, the set of all the ∞-isotopies between ΩC-algebra structures forms a group which is isomorphic though the graph exponential/logarithm maps to the gauge group of gA

exp : ((gA)0,BCH,0) ∼= (ΓA,⊚,1) : log . Suppose that C is a reduced weight-graded coproperad (with no diﬀerential) and let H be a graded R-module. The associated convolution dg Lie admissible algebra gH is weight-graded Lie algebra in the sense of Assumptions 1, with the weight grading coming from that of C. It also has an extra ﬁltration where LigA is all the operations with (i+1) or more inputs. More precisely, the (Sop × S)-module C has a direct sum decomposition under a second grading

C = I ⊕ C(1) ⊕ C(2) ⊕ C(3) ⊕ ... where C(i) is spanned by the operations with i outputs. This gives a weight decomposition

gA = (gA)(1) × (gA)(2) × (gA)(3) × ... and we can then deﬁne the extra ﬁltration by

LigA =

(gA)(j).

j i+1

Assuming L is relatively bounded, that is bounded with respect to F, we can apply all the methods of Section 2.1, giving the following applications of Theorem 2.10 and Theorem 2.13.

