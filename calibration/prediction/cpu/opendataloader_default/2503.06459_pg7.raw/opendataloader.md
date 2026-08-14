Proof of Proposition 2.3. The coefficients of the variables in the defining constraints (eqs. (2.11) to (2.15)) of pGT(𝜆, 𝜇) do not depend upon 𝜇. It thus follows that in modifying 𝜇 to 𝜇′, each of the defining hyperplanes is translated parallel to itself. Further, hyperplanes corresponding to eqs. (2.12) and (2.13) do not change. The right hand sides of the inequalities in eq. (2.11) change by at most 𝛿√𝑛 − 1, and the Euclidean norm of the coefficient vector for the corresponding hyperplanes is √𝑛 − 2, so that the corresponding hyperplanes translate along their normal by a distance of at most

√√𝑛𝑛−−12𝛿. A similar argument applied to eq. (2.14) and eq. (2.15) gives upper bounds of 𝛿/

√2𝑖 − 1 (for 1 ≤ 𝑖 ≤ 𝑛 − 2) and 𝛿 respectively on the magnitude of the translation, so that the largest possible magnitude of the translation over all the defining hyperplanes is

√√𝑛𝑛−−12𝛿. □ The volume of GT(𝜆, 𝜇) according to the (𝑛−1)(𝑛−2)

2 -dimensional Hausdorff measure in R𝑛(𝑛−1)/2 is denoted by 𝑉𝜆,𝜇, while that of pGT(𝜆, 𝜇) with respect to the Lebesgue measure on R(𝑛−1)(𝑛−2)/2 is denoted by 𝑉˜𝜆,𝜇. It is then a simple consequence of the area formula [Fed96, Theorem 3.2.3] that

- (2.16) √︁(𝑛 − 1)! ·𝑉˜𝜆,𝜇 = 𝑉𝜆,𝜇.

(See Appendix A.1 for details). Note that for these volumes to be non-zero, it is necessary that (1) |𝜆| = |𝜇|, and (2) the entries of 𝜆 must be distinct.

When both 𝜆 and 𝜇 have only non-negative integer entries, integer points in GT(𝜆, 𝜇) are in one-to-one correspondence with semi-standard Young tableaux with shape 𝜆 and content 𝜇. (This correspondence is obtained by interpreting the 𝑖th row of a pattern with integral entries as the shape of the sub-tableaux consisting only of entries in {1, 2, . . .,𝑖}.) In particular, the number of integral points in GT(𝜆, 𝜇) is then equal to the Kostka number 𝐾𝜆,𝜇. We thus refer to the polytope GT(𝜆, 𝜇) as a Kostka polytope.

Definition 2.5 (The Schur-Horn polytope). Let𝜆 be a partition with𝑛 parts. For𝜎 a permutation of {1, . . .,𝑛}, we denote its action on 𝜆 by

- (2.17) 𝜎(𝜆1, . . .,𝜆𝑛) := (𝜆𝜎(1), . . .,𝜆𝜎(𝑛)).

We refer to the convex hull of all vectors 𝜎(𝜆) (as 𝜎 ranges over all 𝑛-permutations) as the SchurHorn polytope SH(𝜆). SH(𝜆) is also referred to as the permutohedron of 𝜆 [Pos09]. It is well known that SH(𝜆) has the following equivalent representation [Mar64, Theorem 1.1 and Remark 1.1].

- (2.18) SH(𝜆) = 𝜇 ∈ R𝑛≥0 : 𝜆 ⪰ 𝜇 , where 𝜆 ⪰ 𝜇 means that 𝜆 majorizes 𝜇 in the sense that for every permutation2 𝜏 of {1, 2, . . .,𝑛},
- (2.19)


# ∑︁𝑖

(𝜆𝑗 − 𝜇𝜏(𝑗)) ≥ 0 for 1 ≤ 𝑖 ≤ 𝑛 − 1, and ∑︁𝑛

𝑗=1

(𝜆𝑗 − 𝜇𝑗) = 0.

𝑗=1

2It is enough to restrict to the permutation that puts the entries of 𝜇 in non-increasing order.

7

