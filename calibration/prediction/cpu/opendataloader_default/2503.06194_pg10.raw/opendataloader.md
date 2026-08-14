- 4.1. The formula of the first homology groups. We recall the construction of abelian branched coverings of (M,L). Let G be a finite abelian group and π :

π1(M −L) → G be a surjective homomorphism. Let Mπ → M denote the branched cover corresponding to π, that is, the Fox completion of the unbranched covering corresponding to kerπ. Then the transformation group of Mπ → M is G. Note that any finite abelian cover of M branched along L is obtained in this way.

We also recall the formula for the size of the first homology groups of abelian branched coverings given by Mayberry–Murasugi and Porti. Let Gˆ denote the set of homomorphisms from G to C∗. We choose meridians m1,...,md ∈ π1(M − L;Z). For ξ ∈ Gˆ, we define a sublink Lξ of L as

Lξ = ∪ξ(π(mi))̸=1li. We write Lξ = li

1 ∪ ···li

k

. For the trivial homomorphism 1 ∈ Gˆ, we define L1 = ∅ and ∆L

1

= 1. We also set Gˆ(1) = {ξ ∈ Gˆ | Lξ has a single component}.

We write i(ξ) for the index of the meridian corresponding to ξ ∈ Gˆ(1). For a group H, let |H| be the size of H if H is finite and 0 if H is infinite. Then Mayberry–Murasugi and Porti gave the following theorem.

Theorem 4.1 ([8, Theorem 10.1], [4, Theorem 1.1]).

|H1(Mπ;Z)| = |G| ξ∈Gˆ(1) |1 − ξ(π(mi(ξ)))|

ξ∈Gˆ

|∆L

ξ

(ξ(π(mi

1

)),...,ξ(π(mi

k

)))|. (4.1)

- 4.2. Zdp-coverings. Let π : π1(M −L) → Zdp be the composition map of the abelianization π1(M − L) → π1(M − L)ab (∼= Zd) and the inclusion Zd → Zdp. For a finite index subgroup Γ ⊂ Zdp let πΓ : π1(M − L) → Zdp/Γ denote the composition of π and the canonical surjective map Zdp → Zdp/Γ. Let MΓ → M denote the branched covering of (M,L) corresponding to πΓ.


Definition 4.2. A branched Zdp-covering of (M,L) is the inverse system of branched coverings MΓ → M where Γ runs finite index open subgroups in Zpd.

We obtain the p-adic convergence of the non-p-parts of the sizes of the first ho-

mology groups in branched Zdp-covering of (M,L). For a Zp-module A let rankA = dimF

A ⊗ Fp.

p

Lemma 4.3. Let Γ1 ⊃ Γ2 ⊃ ··· be a descending sequence of finite open subgroups such that ∩nΓn = {0} in Zpd. Then we have

- (1) for all sufficiently large n, rankZpd/Γn = d.
- (2) for each meridian m of L, limn→∞ ord(πΓ


(m)) = ∞. Proof. We put Gn = Zpd/Γn.

n

←−n Gn ∼= Zpd by the assumption ∩nΓn = {0}. Since the canonical homomorphisms Fn : Zpd → Gn and fn/n−1 : Gn → Gn−1 are surjective the induced homomorphisms F˜n : Zpd⊗Fp → Gn⊗Fp and f˜n/n−1 : Gn⊗Fp → Gn−1⊗Fp are also surjective. Thus we have that the sequence (rankGn) is monotonically increasing. We suppose that rankGn < d for all n > 0. Then we have that dimF

(1) We note that lim

kerF˜n ≥ 1 for all n. Since kerF˜n ⊂ kerF˜n−1 for all n > 1, we see that dimF

p

n ∩n kerF˜n ≥ 1. Thus

10

