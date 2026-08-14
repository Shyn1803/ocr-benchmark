NORMAL TRACE SPACE OF DM-FIELDS 7

We also denote the induced pairing by  ·,· A, which satisﬁes

- (2.24) m,φ A =

k

i=1

ai(φ(qi) − φ(pi)), m =

k

i=1

ai(δq

i

− δp

i

) ∈ A0(X,e), φ ∈ Lipb(X),

understanding that φ(e) = 0. Proposition 2.11. Let X ⊂ Rn be a closed set and e ∈/ X. Then,

- (a) A(X,e) ∼= Æ(X) via m  → m X for m ∈ A0(X,e), extending by density,

![](<2503.09536_pg7_images/imageFile1.png>)

![](<2503.09536_pg7_images/imageFile2.png>)

- (b) Lipb(X) ≃ Æ(X)∗ via φ  → (m  → m,φ Æ).


Proof. By [Wea18, Thm.3.3, Cor.3.4], the pairing (2.24) extends to an isometric isomorphism A(X,e)∗ ∼= Lipb(X). In particular this implies that for m ∈ Æ0(X,e),

- (2.25) m X Lip

![](<2503.09536_pg7_images/imageFile3.png>)

![](<2503.09536_pg7_images/imageFile4.png>)

b(X)∗ = sup{| m,φ A| : φ Lip

b(X) ≤ 1} = m A.

Hence it follows that A(X,e) ∼= Æ(X) by sending each m ∈ A0(X,e) to m X ∈ Æ0(X) and extending by density, thereby proving (a). Since we also have m,φ A = m X,φ Æ for all m ∈ A0(X,e) and φ ∈ Lipb(X), it follows that Æ(X)∗ ∼= Lipb(X) via the pairing  ·,· Æ, establishing (b).

![](<2503.09536_pg7_images/imageFile5.png>)

![](<2503.09536_pg7_images/imageFile6.png>)

![](<2503.09536_pg7_images/imageFile7.png>)

![](<2503.09536_pg7_images/imageFile8.png>)

Example 2.12. If X ⊂ Rn is closed, we have M(X) ⊂ Æ(X), by noting for that each µ ∈ M(X), the mapping φ  → X φdµ is well-deﬁned and weakly∗-continuous on Lipb(X). However this space is strictly larger in general; if a ∈ X is an accumulation point of X, then we can ﬁnd a sequence (ak)k ⊂ X converging to a such that ak = a for all k. By passing to a subsequence if necessary, assume that k|ak − a| < ∞. Then m = ∞k=1(δa

k

−δa) ∈ Æ(X) by noting the series converges absolutely in Lipb(X)∗.

- Lemma 2.13. Let X ⊂ Rn be any set, and φk,φ ∈ Lipb(X). Then, as k → ∞,

(2.26) φk ⇀∗ φ in Lipb(X) ⇐⇒

φk → φ uniformly on bounded subsets of X, supk φk Lip

b(X) < ∞.

Proof. Using the identiﬁcation Lipb(X) ∼= Lipb(X), we can assume without loss of generality that X is closed. If φk ⇀∗ φ weakly∗ in Lipb(X), by the Banach-Steinhaus theorem, we have

![](<2503.09536_pg7_images/imageFile9.png>)

φk Lip

b(X) is uniformly bounded in k. Then by applying the Arzelà-Ascoli theorem, there is a subsequence φk

j

which converges uniformly to φ on X ∩BM(0) for each M ∈ N, and hence φk

j

→ φ uniformly on bounded subsets of X. Since the limit is unique, this convergence also holds for the entire sequence φk.

Conversely since Lipb(X) is the dual of a separable space, the weak∗-topology is compact and metrisable on norm-bounded subsets (see e.g.[Bre11, Thm.3.16, 3.28]). Therefore φk admits a weakly∗-convergent subsequence, but since this limit is uniquely determined as φ using the uniform convergence, the entire sequence φk converges weakly∗ to φ.

We will often use Lemma 2.13 with X = [0,1], noting that Lipb([0,1]) = W1,∞((0,1)). For general open sets U however, we have a slightly diﬀerent characterisation for weak∗ convergence in W1,∞(U).

- Lemma 2.14. Let U ⊂ Rn be an open set. Then if φk,φ ∈ W1,∞(U), as k → ∞,


- (2.27) φk ⇀∗ φ in W1,∞(U) ⇐⇒


φk → φ pointwise, supk φk W1,∞(U) < ∞.

In addition, the space C1b(U) is sequentially weakly∗ dense in W1,∞(U).

We note that C1b(U)  ⊂ Lipb(U) in general, so we do not get an analogous density statement there. Also the below proof shows in fact that φk → φ locally uniformly in U in (2.27), however pointwise convergence will suﬃce for our purposes.

