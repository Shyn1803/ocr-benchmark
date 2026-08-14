14 BERNARDO CARVALHO, PIOTR OPROCHA, AND ELIAS REGO

Proof of Theorem 3.7. First, note that fA has a unique measure of maximal entropy η and its push forward measure µ = π∗η is a measure of maximal entropy of gA, because π is bounded to one which guarantees hµ(gA) = hη(fA) (e.g. see [39]) and, hence, h(gA) = h(fA) = hη(fA) = hµ(gA) (see [25] for the definition of metric entropy).

Next let us prove the uniqueness of the measure of maximal entropy of gA. To do so, let us fix any measure of maximal entropy µˆ for gA. Theorem 2.12 implies that gA has the periodic specification property, which ensures the existence of a sequence µˆn of measures supported on periodic points pn such that µˆ is the weak* limit of µˆn (see [25, Proposition 21.8]). Let qn be any periodic point qn ∈ π−1(pn) and let ηˆn be the measure supported on qn. Then µˆn = π∗(ˆηn). Without loss of generality we may assume that (ˆηn)n∈N converge in the weak* topology to a measure ηˆ. But then, by continuity of the push-forward operator π∗ we have π∗ηˆ = µˆ and as a consequence

h(gA) = hµˆ(gA) ≤ hηˆ(fA) ≤ h(fA) = h(gA). This proves that ηˆ = η and consequently that µˆ = µ, that is, µ is the unique measure of maximal entropy of gA.

It remains to prove that µ is the weak* limit of µn. A difficulty that arise is how to lift precisely the sequence (µn)n∈N to the Torus since the sequence (ηn)n∈N defined by

1 Pern(fA)

δp,

ηn =

p∈Pn(fA)

which converge to η by Bowen’s proof, does not project to (µn)n∈N. Indeed, the antipodal periodic points are also in the pre-image of periodic points of gA. An attempt would be to include the antipodal periodic points in the definition of these measures and consider the sequence (ˆηn)n∈N defined by

1 Pern(fA) + Per−n (fA)

ηˆn =

δp.

p∈Pn(fA)∪Pn−(fA)

But ηˆn still does not project to µn and the problem relies on the existence of the spines (points with a single pre-image). Thus, we rule out these points as follows: for each n ∈ N, let

Pn∗(gA) = {p ∈ Pn(gA) : #π−1(p) = 2}, Per∗n(gA) = #Pn∗(gA), and µˆn =

1 Per∗n(gA)

δp.

p∈Pn∗(gA)

Since there are only four points with a single pre-image, we have |Pern(gA) − Per∗n(gA)| ≤ 4.

Thus, (µn)n∈N and (ˆµn)n∈N converge weakly* to exactly the same measure, provided the limit exists. For each n ∈ N, let

Pn∗(fA) = π−1(Pn∗(gA)) and Per∗n(fA) = #Pn∗(fA) = 2Per∗n(gA), and note that for n sufficiently large we have

Pern(fA) 2 ≤ Per∗n(fA) ≤ 3Pern(fA).

