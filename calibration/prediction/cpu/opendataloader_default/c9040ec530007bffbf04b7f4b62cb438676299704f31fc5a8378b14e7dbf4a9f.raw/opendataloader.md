Next we prove σ1 is a G-extendible set for ρ1. Given ψ1 : σ1 → G we let ψ2 : σ2 → G be the function given by ψ2 = ψ1 ◦ θ∗. There is also a homomorphism Ψ2 : ρ2 → G such that Ψ2|σ2

= ψ2 since σ2 is a G-extendible set for ρ2. There is a homomorphism Ψ1 : ρ1 → G such that for all a,b ∈ X1 such that aρ1b we have

- Ψ1 (a,b) = Ψ2 (θ∗)−1 (a,b) if a = b andΨ1 (a,b) = 1 if a = b. Given a,b ∈ X1 such that (a,b) ∈ σ1 there exist x,y ∈ X1 such that a = θ (x), b = θ (y), and (x,y) ∈ σ2. We have θ∗ (x,y) = (a,b) and Ψ2 (x,y) = Ψ1 (a,b) by construction,
- Ψ2 (x,y) = ψ2 (x,y) since (x,y) ∈ σ2, and ψ2 (x,y) = ψ1 (a,b) since ψ2 = ψ1 ◦ θ∗.


This shows Ψ1|σ1

= ψ1 and σ1 is a G-extendible set for ρ1.

Definition 4.4 Let ρ be a reﬂexive relation on a set X.

- 1. (X,ρ) is stable if ρ is balanced and if the relations aρb, aρc, bρc, bρd, and cρd imply aρd for all distinct a,b,c,d ∈ X.
- 2. An element x ∈ X is a clasp if there exist w,y ∈ X\{x} such that wρx, xρy, and (w,y) ∈/ ρ.
- 3. x ∈ X is a locked clasp if there exist u,v,w,y ∈ X\{x} such that (w,y) ∈/ ρ and (u,x,y),(u,x,v),(w,x,v) ∈ Trans(X) .
- 4. An unlocked clasp is a clasp which is not locked.


It is easy to see a preorder is stable. The balanced relation determined by (d) in Figure 1 is not stable. Neither a balanced relation which is not stable nor a stable relation which contains a locked clasp can be the compression of a preorder by [8, Theorem 2.4 and Lemma 3.4].

14

