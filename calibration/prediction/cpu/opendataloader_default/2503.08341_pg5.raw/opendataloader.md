Proposition 2.2. There exists an involution i : H(W) → H(W), defined as i(Tω) = Tω−1, which is an anti-homomorphism, i.e.

i(TrTr−1 ...T2T1) = i(T1)i(T2)...i(Tr−1)i(Tr). In particular, if all the Ti are indexed by the generators of the Hecke algebra, we have i(Ts

...Ts

) = Ts

...Ts

.

r

1

1

r

Many particle systems can be characterized using the Hecke Algebra or random walk on the Hecke Algebra, see [8] for more examples. In this paper, we focus on the oriented swap process. Let W = Sn be the permutation group, S the set of n − 1 nearest neighbor transpositions as the generators, and l the length function, defined as the inversion number of a permutation. We set as = 1 and bs = 0 and define a map P : Sn → H(Sn) such that a permutation ω is mapped to an element P(ω) = Tω in the basis of the Hecke algebra.

When a swap attempt occurs at position i, ω transitions to τiω if and only if ω(i) < ω(i + 1). On the other hand, Tτ

Tω = Tτ

iω if and only if ω(i) < ω(i + 1). Now, consider a continuous-time

i

random walk on Hecke algebra, i.e. Wt = ri=1 Ti, where each Ti is chosen uniformly from all the nearest neighbor transposition, and r = Poi(t). Writing this random walk as a linear combination

of the Hecke algebra basis defines a random measure on the basis. The probability that a finite swap process is in configuration ω at time t corresponds to the expectation of coefficient of Tω in the decomposition of Wt.

# Corollary 2.3. [8, Cor. 2.2]

- 1. For a finite oriented swap process at a fixed time t, πtn and (πtn)−1 have the same law, the inverse is in the sense of the inversion of a permutation.
- 2. For a infinite swap process at a fixed time t, and its first k particles,

(πt(1),πt(2),...πt(k)) (=d) (πt−1(1),πt−1(2),...πt−1(k)).

Remark 2.4. The symmetry property for the finite case is a direct corollary of the property of the involution. For the infinite case, we need again the Harris’ construction and apply the symmetry property to each segment, see also the proof of [2, Thm 1.4].

- 2.3 Properties of TASEP and the oriented swap process


Our analysis of the oriented swap process relies on its connection with TASEP. In this section, we present some propositions about TASEP and how they relate to the oriented swap process. Firstly, we define certain operations on configurations of TASEP or the oriented swap process. A configuration ρ ∈ ZI specifies the type of particle at each position and the set of all such configurations is denoted as S.

Definition 2.5. For any k ∈ Z, and any configuration ρ, where I is a finite or infinite interval, we define the projection operator Tk : S → S as

(Tkρ)(x) = 1{ρ(x)≤k}.

The operator projects a configuration of multi species particle system(e.g. the infinite oriented process) to a TASEP configuration on the same segment with only particles and holes.

5

