We also denote the induced pairing by  · , ·  A , which satisﬁes

$$
(2.24) (m, %)A = m = € Ao( X,e) € (X), i=1 1=1 Lipb (
$$

understanding that φ ( e ) = 0 .

Proposition 2.11. Let X ⊂ R n be a closed set and e / ∈ X . Then,

A ( X,e ) ∼ = Æ ( X ) via m  → m X for m ∈ A 0 ( X,e ) , extending by density, ≃ Æ ∗ via  →  →     .

(b)

, Thm.3.3, Cor.3.4], the pairing ( 2.24 ) extends to an isometric isomorLip b ( X ) . In particular this implies that for m ∈ Æ 0 ( X,e ) ,

$$
Ilm
$$

Hence it follows that A ( X,e ) ∼ = Æ ( X ) by sending each m ∈ A 0 ( X,e ) to m X ∈ Æ 0 ( X ) and extending by density, thereby proving (a) . Since we also have   m,φ   A =   m X,φ   Æ for all m ∈ A 0 ( X,e ) and φ ∈ Lip b ( X ) , it follows that Æ ( X ) ∗ ∼ = Lip b ( X ) via the pairing  · , ·  , establishing (b) .  

Example 2.12. If X ⊂ R n is closed, we have M ( X ) ⊂ Æ ( X ) , by noting for that each µ ∈ M ( X ) , the mapping φ  →   X φ d µ is well-deﬁned and weakly ∗ -continuous on Lip b ( X ) . However this space is strictly larger in general; if a ∈ X is an accumulation point of X , then we can ﬁnd a sequence ( a k ) k ⊂ X converging to a such that a k   = a for all k . By passing to a subsequence if necessary, assume that   k | a k − a | < ∞ . Then m =   ∞ k =1 ( δ a k − δ a ) ∈ Æ ( X ) by noting the series converges absolutely in Lip b ( X ) ∗ .

Lemma 2.13. Let X ⊂ R n be any set, and φ k ,φ ∈ Lip b ( X ) . Then, as k → ∞ ,

$$
@k = uniformly on bounded subsets of X, 2.26) @k in (X) (X) 00 Lipb (
$$

Proof. Using the identiﬁcation Lip b ( X ) ∼ = Lip b ( X ) , we can assume without loss of generality that X is closed. If φ k ∗ ⇀ φ weakly ∗ in Lip b ( X ) , by the Banach-Steinhaus theorem, we have   φ k   Lip b ( X ) is uniformly bounded in k . Then by applying the Arzelà-Ascoli theorem, there is a subsequence φ k j which converges uniformly to φ on X ∩ B M (0) for each M ∈ N , and hence φ k j → φ uniformly on bounded subsets of X . Since the limit is unique, this convergence also holds for the entire sequence φ .

k Conversely since Lip b ( X ) is the dual of a separable space, the weak ∗ -topology is compact and metrisable on norm-bounded subsets (see e.g. [ Bre11 , Thm.3.16, 3.28]). Therefore φ k admits a weakly ∗ -convergent subsequence, but since this limit is uniquely determined as φ using the uniform convergence, the entire sequence φ k converges weakly ∗ to φ .  

We will often use Lemma 2.13 with X = [0 , 1] , noting that Lip b ([0 , 1]) = W 1 , ∞ ((0 , 1)) . For general open sets U however, we have a slightly diﬀerent characterisation for weak ∗ convergence in W 1 , ∞ ( U ) .

Lemma 2.14. Let U ⊂ R n be an open set. Then if φ k ,φ ∈ W 1 , ∞ ( U ) , as

$$
@k pointwise; (2.27) in Wl,* (U)
$$

In addition, the space C 1 b ( U ) is sequentially weakly ∗ dense in W 1 , ∞ ( U ) .

We note that C 1 b ( U )  ⊂ Lip b ( U ) in general, so we do not get an analogous density statement there. Also the below proof shows in fact that φ k → φ locally uniformly in U in ( 2.27 ), however pointwise convergence will suﬃce for our purposes.

