0

0

4

3

![](<2503.04950_pg23_images/imageFile1.png>)

2

1

3

0

Figure 6: An N -labeling of ν = (4 , 3 , 3) . The descents occur at cells (2 , 3) , (3 , 1) , (3 , 2) , (3 , 3) yielding maj ( σ ) = 2 + 1 + 1 + 1 = 5 . The inversion triples are formed by ((3 , 2) , (3 , 1) , (3 , 3)) , ((1 , 2) , (1 , 3)) , and ((1 , 2) , (1 , 4)) yielding inv ( σ ) = 3 .

The reading order of a diagram ν is the order on cells that goes left-to-right along rows starting from the top row and working down. The standardization of a labeling σ : ν → N with content α = ( α 0 ,α 1 , ··· ) , denoted by st ( σ ) , is an injective labeling σ : ν → { 1 , ··· , | ν |} that labels the 0’s appearing in ν 1 , 2 , ··· ,α 0 in the order that they appear in the reading order. The 1’s appearing in ν are labeled α 0 + 1 , ··· ,α 0 + α 1 in reading order and so on. A triple consists of cells with row-column coordinates of the form u = ( r,c ) , v = ( r − 1 ,c ) and w = ( r,c + k ) for r,c,k ≥ 1 , where u,w must be cells of ν , but v is allowed to be a cell immediately below ν . Extend st ( σ ) to cells immediately below ν by labeling them −∞ . A triple is an inversion triple of σ if the labels st ( σ )( u ) , st ( σ )( w ) , st ( σ )( v ) are decreasing clockwise. The statistic inv ( σ ) counts the number of inversion triples of σ .

A descent of σ is a cell u = ( r + 1 ,c ) in ν , such that v = ( r,c ) is Des ( σ ) denote that set of descents we deﬁne the major index statistic

$$
maj(o) := (leg(u) + 1),
$$

where leg ( u ) is the number of cells of ν in the same column as u and above u . See Fig 6 for an example.

Lemma 5.2.1. The monomial coeﬃcient  

M ( n ) denote the set of being enumerated in ( 26 ). Then

$$
IM(n)
$$

and we wish to show | M ( n ) | stabilizes.

Suppose n ≥ | µ | + µ 1 + | η | + i and n ≥ | η | + η 1 so that µ [ n ] and η [ n ] are well-deﬁned. Deﬁne the map γ n : M ( n ) → M ( n +1) as follows. For σ ∈ M ( n ) , shift the bottom row of the corresponding diagram to the right by one cell and insert a new cell labelled 0 in the bottom left corner. So for instance:

2

2

0

Yn

![](<2503.04950_pg23_images/imageFile2.png>)

4

3

1

4

3

1 0

0

0

0

0

0

0

We have to check that the map is well-deﬁned and surjective. We claim that the ﬁrst µ 1 +1 entries of the bottom row of any σ ′ ∈ M ( n +1) are 0. Suppose for contradiction that there was a non-zero value a among these ﬁrst µ 1 +1 cells. Then there are at least n +1 −| µ |− ( µ 1 +1) = n −| µ |− µ 1 entries right of a . Of these, at most | η | − 1 are allowed to be non-zero (since a is one of the | η | non-zero values in the labeling). Hence a would contribute at least n − | µ | − µ 1 − ( | η | − 1) > i inversion triples formed by taking a , the phantom cell below it, and a 0 entry to the right of it. This contradicts that inv ( σ ′ ) = i for σ ′ ∈ M ( n +1) .

This implies that if we let σ be obtained from a σ ′ ∈ M ( n +1) by deleting the bottom left cell and shifting the bottom row to the left by one, then σ ∈ M ( n ) and γ n ( σ ) = σ ′ , which implies that γ n is well-deﬁned and bijective. Indeed, the ﬁrst µ 1 cells of the bottom row of σ will be labeled 0 and so the status of descents and inversion triples doesn’t change when going from σ ′ to σ . Thus, σ ′ and σ have the same inv and maj values.

