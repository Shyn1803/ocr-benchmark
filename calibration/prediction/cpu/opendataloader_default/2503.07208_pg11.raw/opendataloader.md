# S. Jana, L. Kanesh, M. Kundu, D. Lokshtanov, and S. Saurabh 23:11

of f, denoted by c(f), as any directed S-path from u to v that utilizes only forward arcs from AB(Tσ,Pσ).

- ▶ Definition 13 (certification of an arc set). Consider an ordered partition Pσ = (V1,...,Vℓ) of an ordered tournament Tσ and let F be a set of some backward arcs of Tσ. We say that we can certify F whenever it is possible to find a set F = {c(f) : f ∈ F} of arc-disjoint certificates for the arcs in F.
- ▶ Definition 14 (safe partition). Consider an ordered partition Pσ = (V1,...,Vℓ) of an ordered tournament Tσ. Let BE denote the set of all backward arcs in AB(Tσ,Pσ). For a vertex subset S ⊆ V (T), we say Pσ is a S-safe partition if we can certify BE.


Let Dσ = (Vσ,A) be an ordered directed graph. We use Sfas(Dσ,S) to denote the size of a minimum subset feedback arc set in the directed graph Dσ. Specifically, given a directed graph Dσ, and a vertex subset S ⊆ Vσ, it refers to the cardinality of the smallest set F ⊆ A of arcs whose removal (or reversal) renders Dσ S-acyclic. Given a tournament, for an arc subset A′ ⊆ A[T], the directed graph T[A′] is defined by the subgraph T containing the arc set A′. More specifically, T[A′] = (V (T),A′). For a ease of notation, when the subset is clear to the context, we use Sfas(Dσ) instead of Sfas(Dσ).

▶ Lemma 15. Consider an ordered partition Pσ = (V1,...,Vℓ) of an ordered tournament Tσ and a terminal set S ⊆ V (T). If Pσ is a S-safe partition then,

Sfas(Tσ) = Sfas(Tσ[AI(Tσ,Pσ)]) + Sfas(Tσ[AB(Tσ,Pσ)])

Moreover, there exists a minimum sized S-feedback arc set of Tσ containing BE, where BE denote the set of all backward arcs in AB(Tσ,Pσ).

Proof. Given any bipartition of the arc set A into A1 and A2, we have

Sfas(Tσ) ≥ Sfas(Tσ[A1]) + Sfas(Tσ[A2]). Specifically, for the partition of A into AI(Tσ,Pσ) and AB(Tσ,Pσ), it follows that

Sfas(Tσ) ≥ Sfas Tσ[AI(Tσ,Pσ)] + Sfas Tσ[AB(Tσ,Pσ)] . Next, we need to show that

Sfas(Tσ) ≤ Sfas Tσ[AI(Tσ,Pσ)] + Sfas Tσ[AB(Tσ,Pσ)] .

This assertion holds because, after reversing all arcs in BE, each remaining directed S-cycle is contained within Tσ[Vi] for some i ∈ [ℓ]. In other words, once all arcs in BE are reversed, every S-cycle is entirely contained within Tσ[AI(Tσ,Pσ)]. Observe that as Pσ is S-safe, the set of all backward arcs of AB(Tσ,Pσ), i.e., BE can be certified using only arcs from AB(Tσ,Pσ). This concludes the proof of the first part of the lemma. Essentially, we have shown the existence of a minimum-sized S-feedback arc set for Tσ that includes BE. This completes the proof of the lemma. ◀

Construction of a S-safe partition. Recall that an S-triangle is a directed cycle of length three that includes at least one vertex from S. It is clear that the number of arc-disjoint Striangles provides a lower bound for the size of the smallest S-feedback arc set in a tournament. We illustrate how this set can be utilized to identify a safe partition in polynomial time.

## CVIT 2016

