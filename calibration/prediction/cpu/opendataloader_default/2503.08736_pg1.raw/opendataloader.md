arXiv:2503.08736v1 [quant-ph] 11 Mar 2025

A Note on Clifford Stabilizer Codes for Ising Anyons

Sanchayan Dutta∗

University of California, Davis

We provide a streamlined elaboration on existing ideas that link Ising anyon (or equivalently, Majorana) stabilizer codes to certain classes of binary classical codes. The groundwork for such Majorana-based quantum codes can be found in earlier works (including, for example, Bravyi [BTL10] and Vijay et al. [VF17]), where it was observed that commuting families of fermionic (Clifford) operators can often be systematically lifted from weakly self-dual or self-orthogonal binary codes. Here, we recast and unify these ideas into a classiﬁcation theorem that explicitly shows how q-isotropic subspaces in F22n yield commuting Clifford operators relevant to Ising anyons, and how these subspaces naturally correspond to punctured self-orthogonal codes in F22n+1.

1. INTRODUCTION

Ising anyons are non-Abelian excitations in certain twodimensional topological phases of matter. They can encode and process quantum information by virtue of their fusion and braiding properties. A particularly relevant physical instantiation comes from Majorana zero modes at the boundaries of topological superconductors [Kit01, Iva01].

Adapting quantum error-correcting strategies to the Isinganyon (or Majorana) context entails generalizing the familiar notion of Pauli stabilizer codes to accommodate fermionic degrees of freedom and parity constraints. Early progress in this direction was made by Bravyi, who introduced Majorana fermion codes [BTL10]. Building on this, Vijay et al. [VF17] highlighted how these fermionic stabilizers map naturally onto weakly self-dual or self-orthogonal binary codes. Related developments have investigated the broader class of Clifford stabilizer codes [Oka23], emphasizing that commuting, even-parity operators underlie valid stabilizer constraints.

In this note, we revisit and unify these ideas by focusing on

the concept of q-isotropic subspaces of Fn2 [Oka23]. We show how such subspaces serve as the building blocks for deﬁning

Clifford stabilizer codes in Ising-anyonsystems. Furthermore, by enlarging the ambient space to Fn2+1 via a convenient mapping, these q-isotropic subspaces turn out to correspond exactly to punctured images of classical self-orthogonal codes, providing a direct route to analyzing quantum code properties (such as distance) in purely classical terms.

One advantage of this viewpoint is that it allows us to utilize standard techniques from classical coding theory: in particular, distance bounds such as the Varshamov bound imply that one can construct families of codes with growing length, good distance, and nonvanishing rate, guaranteeing robust error protection in a broad sense. While these results have appeared in various forms in the literature, here we aim to offer a transparent exposition of why these classical arguments continue to apply in the Majorana (or Ising-anyon) context.

![](<2503.08736_pg1_images/imageFile1.png>)

∗ dutta@ucdavis.edu

2. QUANTUM METRICS AND CLIFFORD CODES

Here we give a concise overview of the foundational concepts from Chapter 2 of [Oka23], focusing on quantum metrics as a unifying framework for assigning distances to quantum errors. This is analogous to the Hamming distance for classical coding but is adapted to genuinely quantum settings. In ﬁnite dimensions, one can specify a generating set of errors, from which all higher-distance errors are built. We also introduce the Kuperberg-Weaver notion of a quantum metric [KW12], specialized here to ﬁnite dimensions, which assigns distances to operators by specifying how they are generated at each level of the metric. Examples include classical and quantum Hamming spaces, as well as spinorial, semispinorial, and full Clifford metrics.

2.1. Kuperberg–Weaver Metrics in Finite Dimension

We work in a ﬁnite-dimensional Hilbert space H with associated operator space B(H). A Kuperberg–Weaver quantum metric on B(H) is a nested family of subspaces

{Et}t≥0 ⊆ B(H), satisfying the following axioms:

- 1. E0 = CIH. Only scalar multiples of the identity have distance zero.
- 2. Et∗ = Et for each t. Each level is closed under adjoints, so these subspaces consistently contain all relevant “errors” of a given size.
- 3. EsEt ⊆ Es+t. This is a “triangle inequality” condition on errors, ensuring that composing an error of degree s with another of degree t yields an error of degree at most s+t.


Graph Metrics. A convenient way to build such a quantum metric in ﬁnite dimensions is to specify a generating subspace

E ⊆ B(H),

containing the identity IH and closed under adjoints. We interpret E as the space of “lowest-degree” or single-step nontrivial errors [Oka23]. Deﬁne

E0 = CIH, and for each integer t ≥ 1,

