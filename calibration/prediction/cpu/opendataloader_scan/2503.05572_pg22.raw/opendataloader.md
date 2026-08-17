permutes the Z 7 -component at h by a particular even permutation if and only if hs = hs ′ .

  Once we can check for equality of nodes, the proof is again similar to the proof of Theorem 4.1, but we check for an accepting tree on the tree obtained by contracting paths. We will construct versions of the φ -maps that send information over paths where the tree is not branching, and goodness checks should similarly jump over paths. In the remainder of the proof, we explain how these variants can be constructed. d

Note that the contracted paths are of length n at most. We explain ﬁrst how to deal with a single length ℓ . A minor modiﬁcation of Equation 1 gives an automorphism f that performs π in the Z 7 -component at h if and only if ha ℓ contains s . Namely, we simply replace the conjugating partial shifts of the third track by their ℓ th power. ℓ ′

However, we need to check that the intermediate nodes on the path, i.e. ha for ℓ ′ < ℓ , do not branch, and that ha ℓ does branch. This can be done since as we showed above, we have in our group automorphisms that permute Z 7 in an arbitrary way depending on whether a given relative node is branching. Speciﬁcally, one can use commutator formulas and divide-and-conquer to obtain a polynomial-norm automorphism that cancels the eﬀect of f if the branching is not correct.

The resulting automorphisms can be simply composed for all distinct ℓ to obtain the desired analogs of the φ -maps, as their supports are distinct (the ℓ th map can only act nontrivially when the non-branching preﬁx of the tree starting from h is of length exactly ℓ ). To allow goodness checks to jump over paths, the argument is direct from

Barrington’s theorem (taking the maps that check for branching nodes to be to be among the generators).

# PSPACE-hardness for general groups under the Gap Conjecture

A sequence b k is at most polynomial if b k = O ( k d ) for some d . A function b k is at least stretched exponential if we have b k = Θ( e k β ) for some β > 0, and β is called the degree . We again recall the version of Gap Conjecture relevant to us, so let β ∈ [0 , 1).

Conjecture 7.1 (Conjecture C ∗ ( β ) of Grigorchuk) . A group either has at most polynomial growth, or at least stretched exponential growth with degree β .

We next show that in any group with stretched exponential growth in the above sense, for suﬃciently large k we can ﬁnd a subtree that ﬁts in a ball of radius polynomial in k , has suﬃcient branching, and furthermore we can encode this tree in a ﬁnite-support conﬁguration of a particular SFT X . We are mainly interested in full shifts, so we will work with SFTs that contain

points of ﬁnite support, and our ﬁrst result constructs ﬁnite-support points which we will use as markers. This does not require any assumptions on the group. Similar marker constructions can be performed under other (including some strictly weaker) assumptions. See e.g. [2, 19] for such marker constructions.

