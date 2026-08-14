arXiv:2503.07573v1 [math.DG] 10 Mar 2025

RECONSTRUCTING CURRENTS FROM THEIR PROJECTIONS

AIDAN BACKUS

Abstract. We prove an inversion formula for the exterior k-plane transform. As a consequence, we show that if m < k then an m-current in Rn can be reconstructed from its projections onto Rk, which proves a conjecture of Solomon.

A basic problem in analysis and geometry is to reconstruct an object in euclidean space from its orthogonal projections. Here we are interested in reconstructing an oriented submanifold, or more generally a current, from its projections. The geometry needed to prove our main theorem was worked out by Solomon [Sol11], who conjectured that the analysis would work out as well. In this brief note, we prove that conjecture.

Throughout, ﬁx integers 0 ≤ m < k < n. A compactly supported m-current is a continuous linear functional on the space of smooth m-forms [Sim84, §6.2]. If T is a compactly supported m-current and α is a smooth m-form, we write T α for T(α). Thus every compact, oriented, C1 submanifold of Rn is a compactly supported m-current.

Let G be the Grassmannian variety of k-dimensional linear subspaces of Rn. There is a natural O(n)-action on G, which induces a unique O(n)-invariant Borel probability measure on G. For any P ∈ G, we have two operations:

- (1) Given an m-form α on P, the pullback P∗α is the m-form on Rn which is the pullback of α by the orthogonal projection, Rn → P.
- (2) Given a compactly supported m-current T on Rn, the pushforward P∗T is the compactly supported m-current on P such that for every m-form α on P,


α =

P∗T

P∗α.

T

It is very important to work in the category of compactly supported currents for the pushforward by an orthogonal projection to make sense. Indeed, one can only push forward a noncompactly supported current by a proper map, which orthogonal projections are not; moreover, it does not really make sense to make sense to push forward a submanifold of Rn.

![](<2503.07573_pg1_images/imageFile1.png>)

We take the convention 0 ∈ N. Let x := 1 + |x|2 be the Japanese bracket. By A k B we mean that there exists C > 0 (which depends on k) for every A,B, A ≤ CB. The Schwartz space is the Fre´chet space S of m-forms α such that for every N ∈ N, |α(x)| N x −N [H¨or15, §7.1]. A density argument shows that a compactly supported m-current is determined by its action on S .

Our main theorem establishes [Sol11, Conjectures 6.5 and 6.8]:

Theorem 1. For every α ∈ S and P ∈ G, there exists a smooth m-form αP on P such that for every x ∈ Rn,

α(x) =

P∗(αP)(x)dP, (1)

G

![](<2503.07573_pg1_images/imageFile2.png>)

Date: March 11, 2025. 2020 Mathematics Subject Classiﬁcation. 44A12. This research was supported by the National Science Foundation’s Graduate Research Fellowship Program under

Grant No. DGE-2040433.

1

