4 STABILITY ESTIMATES FOR THE VLASOV–POISSON SYSTEM WITH YUDOVICH DENSITY

- Assumption 1.5. The growth functions Θ is such that the associated generalized modulus of continuity φΘ : [0,+∞) → [0,+∞) is continuous, where

φΘ(s) :=

 



0 if s = 0, s|log s|Θ(|log s|) if 0 < s < e−d−1, e−d−1(d + 1)Θ(d + 1) if s ≥ e−d−1.

Indeed, φΘ is the modulus of continuity of the force field given that the macroscopic density is Yudovich, which is enforced by Assumption 1.4 (see Crippa, Inversi, Saffirio and Stefani [4, Lemma 1.1 and Assumption 1.3]); as explained in [4], the value e−d−1 in the definition of φΘ is essentially irrelevant and included solely to make φΘ more appealing. Under Assumption 1.4 and Assumption 1.5, one can define weak solutions f to (VP) through

T

0 X×Rd

[(∂tϕ + v · ∇xϕ − ∇Uf · ∇vϕ)f](t;x,v) dxdv dt = −

X×Rd

ϕ(0,x)f(0;x,v) dxdv

for all test functions ϕ ∈ Cc∞([0,T) × (X × Rd)), since then the product of the solution with the force field is integrable; i.e., ∥f(t)∇Uf(t)∥L1(X×Rd) ∈ L1([0,T]).

While [4, Theorem 1.6] assumed φΘ to be nondecreasing concave in some regime for the 1-Wasserstein stability of (VP), in the p-Wasserstein setting, we instead assume a p-modified version of φΘ to be nondecreasing concave in some regime as follows:

- Assumption 1.6. The growth function Θ is such that φp,Θ : [0,+∞) → [0,+∞) is nondecreasing concave on [0,cp,Θ;d) for some positive constant cp,Θ;d < 1/e that depends only on p, Θ, and d, where φp;Θ is given by


 

0 if s = 0, s|log s|pΘp (|log s|) if 0 < s ≤ cp,Θ;d, φp,Θ(cp,Θ;d) if s ≥ cp,Θ;d.

φp,Θ(s) :=



This encompasses for instance the bounded case with Θ(r) = 1 (cp,Θ;d = e−max{p,d+1}), the exponential Orlicz space with Θ(r) = r1/α and 1 ≤ α < +∞ (cp,Θ;d = e−max{pβ,d+1}, β := 1 + 1/α), and also a countable family of iterated logarithms due to Yudovich [18, Section 3] for two-dimensional Euler’s equations in vorticity form; Θn : [0,+∞) → [0,+∞) (cp,Θ;d = min{expn−+12p(1),e−d−1}) given by

 

r|log1(r)|2|log2(r)|2 ···|logn(r)|2 if r ≥ expn(1), Θn(expn(1)) else,

Θn(r) :=



where exp0(1) := 1, expn+1(1) := eexpn(1), and

 

r if n = 0, log ◦log ◦··· ◦ log

logn(r) :=

◦|log r| otherwise.



(n−1)times

Moreover, each of these cases satisfies the following two assumptions:

