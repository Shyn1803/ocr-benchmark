# 15. A NALYSING THE FLOW

In section 13, we constructed a continuous vector ﬁeld X on the closed surface S . Since in this setting F cs is in ideal position, its vertical sublamination Λ cs Λ

Together, X and Λ have the following properties:

- (1) the vector ﬁeld X is tangent to the geodesic lamination Λ ; − 1
- (2) the vector ﬁeld is zero at a point p if and only if π ( p ) is a center circle and we refer to these as the critical points ;
- (3) each critical point lies on an isolated geodesic in Λ and we call these geodesics the critical geodesics ;
- (4) each critical geodesic contains exactly one critical point;
- (5) at each critical point, the index of X at p is in { − 1,0, + 1}; moreover, if we consider a small disk D centered at p and split D along the critical geodesic to produce two half-disks, then the index of X at p is in { − 1 2 ,0, + 1 2 } on each of the half-disks.


Item (3) is given by lemma 9.1 and item (5) by lemma 13.1.

The plan now is to ﬁrst excise the non-isolated leaves of Λ from S , producing a surface with boundary S 0 ⊂ S where Λ ∩ S 0 consists only of isolated geodesic arcs, each of which is compact. We then split S 0 into a number of “regions” R i by cutting along the “critical arcs.” By applying the Poincaré–Hopf theorem to the vector ﬁeld X restricted to a region R i , we show that at least one of these regions has positive Euler characteristic and therefore must be a topological disk. Its pre-image π − 1 ( R i ) must contain half of a vertical leaf of F cu , and this causes a contradiction, completing the overall proof.

For simplicity, we assume that the continuous vector ﬁeld X integrates to a ﬂow φ on S and we explain in the following remark how to adapt the proof when this is not the case.

Remark . The deﬁnition of a dumbbell and the proof of proposition 14.1 do not actually rely on X integrating to a ﬂow φ on all of S . We can instead deﬁne an outﬂow edge σ as having a small neighborhood U such that any integral curve starting at a point x ∈ U and tangent to X must remain in U until it hits σ . The proof of proposition 14.1 only considers the ﬂow φ on the lamination Γ . In our setting, Γ will be a geodesic lamination and so the ﬂow is well deﬁned. After applying the proposition and restricting to a subset S 0 ⊂ S , we may replace X by a smooth approximation such that X is unchanged on the ﬁnitely many arcs of Λ ∩ S 0 which contain critical points. Thus, we may freely assume that X inte-

Let Γ be the sublamination of Λ consisting of all of the non-isolated leaves in Λ . Apply proposition 14.1 to Γ and let S 0 denote the subset S \int( K ) given by the proposition. Each boundary component of S 0 is therefore a dumbbell.

