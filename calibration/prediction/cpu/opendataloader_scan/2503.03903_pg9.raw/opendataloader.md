![](<2503.03903_pg9_images/imageFile1.png>)

Figure 5. Above is the bottom pipe dream for 1427356 (cross signs denote crossings, and empty boxes denote non-crossings). If we draw a diagonal line out from the first crossing in row 3, then this diagonal line never intersects or is directly to the right of another crossing. However, the diagonal line emitting from the first box in row 5 enters the square directly to the right of the last crossing of row 3. Indeed, the subsequence 473 is a 231 pattern.

a square containing a crossing in P , nor does any square immediately to the left of this line contain a crossing in P .

See Figure 3.2 for an example.

Proof. For contradiction, let i the largest row index such that the line emanating from the leftmost crossing of row i intersects or is directly to the right of a crossing in row j . Since L ( i ) > 0 and i was the largest such row, we must have L ( i + 1) = 0, and thus, since L ( i ) > L ( i + 1), we have w ( i ) > w ( i + 1). But then, we claim that w ( j ) > w ( i + 1). Either w ( j ) > w ( i ), in which this follows by transitivity, or w ( j ) < w ( i + 1), in which case, L ( i + 1) ≥ L ( j ) + ( i − j ) + 1 > 0. Either way, we have either a 231 or a 321 pattern in w given by the indices j,i,i + 1. So, we have proved the claim. □

Lemma 3.6 allows us to prove that 321 and 231-avoidance are sufficient:

Lemma 3.7. If w avoids 231 and 321, then S w is a single CHM. In particular, S w = h L ( w ) .

Proof. We use again the fact that all pipe dreams are obtained from the bottom pipe dream by ladder moves. Here, again all of the ladder moves we can perform are simple ladder moves that just move crossings along their diagonals. Two crossings in the same row of the bottom pipe dream can never slide past each other, and any two rows can slide independently by Lemma 3.6. Thus, row i contributes a factor h i L ( i ) , and multiplying these factors gives us S w =   i h i L ( i ) . □

Notice that, unlike the case of SEMs and analogously to the case for usual monomials, the maximal monomial in the CHM expansion of S w is always h L ( w ) . Finally, we prove that 321 and 231 avoidance are necessary conditions in order for S w to

Finally; we prove that 321 and 231 avoidance are necessary conditions in order for 6w to be a CHM.

Lemma 3.8. If w contains a 321 pattern, then S w is not a CHM.

Proof. We induct on the length of w . First, suppose that w contains a 321 pattern and S w is a single CHM. Let i < j < k be indices such that w i > w j > w k . First, we show how to reduce to the case where i,j,k = i,i + 1 ,i + 2.

