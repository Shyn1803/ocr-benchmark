# Note on Clifford Stabilizer Codes for Ising Anyons

Sanchayan Dutta

University of California;  Davis

We provide a streamlined elaboration on existing ideas that link Ising anyon (or equivalently, Majorana) stabilizer codes to certain classes of binary classical codes. The groundwork for such Majorana-based quantum codes can be found in earlier works (including, for example, Bravyi [ BTL10 ] and Vijay et al. [ VF17 ]), where it was observed that commuting families of fermionic (Clifford) operators can often be systematically lifted from weakly self-dual or self-orthogonal binary codes. Here, we recast and unify these ideas into a classiﬁcation theorem that explicitly shows how q-isotropic subspaces in F 2 n 2 yield commuting Clifford operators relevant to Ising anyons, and how these subspaces naturally correspond to punctured self-orthogonal codes in F 2 n + 1 2 .

# 1. INTRODUCTION

# 2. QUANTUM METRICS AND CLIFFORD CODES

Ising anyons are non-Abelian excitations in certain twodimensional topological phases of matter. They can encode and process quantum information by virtue of their fusion and braiding properties. A particularly relevant physical instantiation comes from Majorana zero modes at the boundaries of topological superconductors [ Kit01 , Iva01 ].

Adapting quantum error-correcting strategies to the Isinganyon (or Majorana) context entails generalizing the familiar notion of Pauli stabilizer codes to accommodate fermionic degrees of freedom and parity constraints. Early progress in this direction was made by Bravyi, who introduced Majorana fermion codes [ BTL10 ]. Building on this, Vijay et al. [ VF17 ] highlighted how these fermionic stabilizers map naturally onto weakly self-dual or self-orthogonal binary codes. Related developments have investigated the broader class of Clifford stabilizer codes [ Oka23 ], emphasizing that commuting, even-parity operators underlie valid stabilizer constraints.

In this note, we revisit and unify these ideas by focusing on the concept of q-isotropic subspaces of F n 2 [ Oka23 ]. We show how such subspaces serve as the building blocks for deﬁning Clifford stabilizer codes in Ising-anyonsystems. Furthermore, by enlarging the ambient space to F n + 1 2 via a convenient mapping, these q-isotropic subspaces turn out to correspond exactly to punctured images of classical self-orthogonal codes, providing a direct route to analyzing quantum code properties (such as distance) in purely classical terms.

One advantage of this viewpoint is that it allows us to utilize standard techniques from classical coding theory: in particular, distance bounds such as the Varshamov bound imply that one can construct families of codes with growing length, good distance, and nonvanishing rate, guaranteeing robust error protection in a broad sense. While these results have appeared in various forms in the literature, here we aim to offer a transparent exposition of why these classical arguments continue to apply in the Majorana (or Ising-anyon) context.

∗ dutta@ucdavis.edu

Here we give a concise overview of the foundational concepts from Chapter 2 of [ Oka23 ], focusing on quantum metrics as a unifying framework for assigning distances to quantum errors. This is analogous to the Hamming distance for classical coding but is adapted to genuinely quantum settings. In ﬁnite dimensions, one can specify a generating set of errors, from which all higher-distance errors are built. We also introduce the Kuperberg-Weaver notion of a quantum metric [ KW12 ], specialized here to ﬁnite dimensions, which assigns distances to operators by specifying how they are generated at each level of the metric. Examples include classical and quantum Hamming spaces, as well as spinorial, semispinorial, and full Clifford metrics.

# 2.1. Kuperberg–Weaver Metrics in Finite Dimension

We work in a ﬁnite-dimensional Hilbert space H with associated operator space B ( H ) . A Kuperberg–Weaver quantum metric on B ( H ) is a nested family of subspaces

$$

$$

≥ satisfying the following axioms:

E 0 = C I H . Only scalar multiples of the identity have distance zero.

E ∗ t = E t for each t . Each level is closed under adjoints, so these subspaces consistently contain all relevant “errors” of a given size.

3. E s E t ⊆ E s + t . This is a “triangle inequality” condition on errors, ensuring that composing an error of degree s with another of degree t yields an error of degree at most s + t .

Graph Metrics. A convenient way to build such a quantum metric in ﬁnite dimensions is to specify a generating subspace

$$
€
$$

containing the identity I H and closed under adjoints. We interpret E as the space of “lowest-degree” or single-step nontrivial errors [ Oka23 ]. Deﬁne

