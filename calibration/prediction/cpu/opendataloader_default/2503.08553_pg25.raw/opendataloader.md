As the proof will show, the value r0 decreases as the value of L increases.

Proof. Let L, r, and p0 be as in the statement of the lemma. We may assume that p0 = p− is the south pole. Let ψ be the stereographic projection based at the north pole p+ and let ϱ be its inverse. Set r1 arccot(L) and let κ denote the biLipschitz constant of the restriction of ψ to S2 \ B(p+,r1). Finally, set r0 2−1 · min{r1, L−1,κ−2}.

Let δr : C → C be the scaling map given by δr(z) = r·z and denote by η: S2 → S2 the conformal diffeomorphism agreeing with ϱ ◦ δr ◦ ψ on S2 \ {p+}. It follows from (2.1) and (2.2) that

η(B(p+,2r1)) = S2 \ B(p−,h(Lr)) ⊂ S2 \ B(p−, Lr) since h(Lr) ≥ Lr.

Now, let p ∈ S2. We distinguish two cases. If B(p,r0) intersects B(p+,r1) nontrivially then B(p,r0) is contained in B(p+,2r1) and hence, by the above, we have η(B(p,r0)) ⊂ S2 \ B(p−, Lr). If B(p,r0) does not intersect B(p+,r1) then we have

η(B(p,r0)) ⊂ B(η(p),rκ2r0) ⊂ B(η(p),r) since the restriction of ψ to S2 \ B(p+,r1) is κ-biLipschitz. □ Proof of Proposition 9.2. Let 0 < ε < εI and let φ: S2 → X be an ε-indecomposable map. Define, as in the proof of Proposition 9.1,

δ min  

  

l02 2π

ε 10CI

and L 2eδ−1kI(eI(φ)+10−1ε),

,

where l0 > 0 is the scale up to which the isoperimetric inequality holds in X, CI is as in (9.1), and kI is as in (3.1). Let 0 < r0 < L−1 be as in Lemma 9.3.

Let u ∈ Λ(φ) be as in the statement of the proposition. For each p ∈ S2 set r(p) inf r > 0 : EI(u|B(p,r)) ≥ 5−1εI and let r¯ > 0 be the infimum of the r(p) over all p ∈ S2. We clearly have EI(u|B(p,r¯)) ≤

εI 5

for every p ∈ S2 and there exists p¯ ∈ S2 such that equality holds for p = p¯. If r¯ ≥ r0 then the proposition holds with η being the identity mapping, so we may assume that r¯ < r0. We claim that

εI 5

(9.2) EI(u|B( ¯p,Lr¯)) > EI(u) −

# .

The proposition easily follows from this together with Lemma 9.3. Indeed, let η: S2 → S2 be as in the lemma applied with p0 = p¯ and r = r¯. Then for every p ∈ S2 we have

η(B(p,r0)) ⊂ B(η(p),r¯) or η(B(p,r0)) ∩ B( ¯p, Lr¯) = ∅. In the first case we obtain

εI 5

EI(u ◦ η|B(p,r0)) ≤ EI(u|B(η(p),r¯)) ≤

and in the second case

εI 5

EI(u ◦ η|B(p,r0)) ≤ EI(u|S2\B( ¯p,Lr¯)) ≤

. This establishes the proposition assuming (9.2).

25

