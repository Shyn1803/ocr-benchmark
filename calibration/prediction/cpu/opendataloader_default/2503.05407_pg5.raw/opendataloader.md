SPHERICAL REPRESENTATION SPACES OF QUIVERS 5

real root, and there are only ﬁnitely many isomorphism classes of such V . This proves ﬁniteness of the number of G d-orbits in R dﬂag(Q). Corollary 3.4. For d ∈ NQ0, the representation space Rd(Q) is spherical if and only if there is no gentle imaginary root e ≤ d for Qd.

Proof. Sphericity of Rd(Q) is equivalent to Bd acting with ﬁnitely many orbits on Rd by Theorem 2.3. This is equivalent to G d acting with ﬁnitely many orbits on R dﬂag(Qd), and the previous proposition shows the claim.

4. Classification

To approach the classiﬁcation of spherical representation varieties, we ﬁrst show that we can restrict to excluding minimal non-spherical situations.

Lemma 4.1. If d ≤ e are dimension vectors for Q and Rd(Q) is not spherical, then Re(Q) is not spherical. Proof. We have an embedding of quivers

ι : Qd → Qe, (i,k)  → (i,k + ei − di) for i ∈ Q0 and k ≤ di. It induces an embedding of Weyl groups ι : WQ

# → WQ

e

d

and a WQ-equivariant embedding

ι : Z(Qd)0 → Z(Qe)0. It is easily veriﬁed that ι maps FQ

, and thus imaginary roots for Qd to imaginary roots for Qe. Obviously, ι also preserves gentleness. The claim then follows from the previous corollary.

to FQ

e

d

We say that a quiver Q is a connected sum of two full subquivers Q′ and Q′′ along a vertex i ∈ Q0 if

(Q′)0 ∪ (Q′′)0 = Q0 and (Q′)0 ∩ (Q′′)0 = {i}. In this case, we write

Q = Q′#iQ′′. Given a dimension vector d for Q, we write

(Q,d) = (Q′,d|Q′)#i(Q′′,d|Q′′).

We call such a connected sum of quiver settings thin if di = 1. In the following, the symbol ↔ denotes an arrow of either orientation.

Theorem 4.2. For a connected quiver setting (Q,d), the representation space Rd(Q) is a spherical variety under the action of Bd ⊂ Gd if and only if (Q,d) is a thin connect sum of quiver settings with Q of the form 1 ↔ 2 ↔ 3, and d = (m,n,1) or d = (m,2,n).

Proof. First assume Rd(Q) is spherical. We reduce to the claimed situation in several steps, always using the previous lemma.

(1) If Q contains a cycle, then Rd(Q) even admits inﬁnitely many Gd-orbits, since there are already inﬁnitely many isomorphism classes of representations of dimension vector (1,...,1) for any cycle quiver. Thus we can assume Q to be a tree.

