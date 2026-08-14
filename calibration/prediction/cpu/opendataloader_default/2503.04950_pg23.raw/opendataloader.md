![](<2503.04950_pg23_images/imageFile1.png>)

![](<2503.04950_pg23_images/imageFile2.png>)

![](<2503.04950_pg23_images/imageFile3.png>)

![](<2503.04950_pg23_images/imageFile4.png>)

![](<2503.04950_pg23_images/imageFile5.png>)

![](<2503.04950_pg23_images/imageFile6.png>)

![](<2503.04950_pg23_images/imageFile7.png>)

![](<2503.04950_pg23_images/imageFile8.png>)

![](<2503.04950_pg23_images/imageFile9.png>)

1 4 3

![](<2503.04950_pg23_images/imageFile10.png>)

![](<2503.04950_pg23_images/imageFile11.png>)

![](<2503.04950_pg23_images/imageFile12.png>)

- 0 2 1

![](<2503.04950_pg23_images/imageFile13.png>)

![](<2503.04950_pg23_images/imageFile14.png>)

![](<2503.04950_pg23_images/imageFile15.png>)

![](<2503.04950_pg23_images/imageFile16.png>)

![](<2503.04950_pg23_images/imageFile17.png>)

![](<2503.04950_pg23_images/imageFile18.png>)

![](<2503.04950_pg23_images/imageFile19.png>)

![](<2503.04950_pg23_images/imageFile20.png>)

![](<2503.04950_pg23_images/imageFile21.png>)

![](<2503.04950_pg23_images/imageFile22.png>)

![](<2503.04950_pg23_images/imageFile23.png>)

![](<2503.04950_pg23_images/imageFile24.png>)

- 0 3 0 1


![](<2503.04950_pg23_images/imageFile25.png>)

![](<2503.04950_pg23_images/imageFile26.png>)

![](<2503.04950_pg23_images/imageFile27.png>)

![](<2503.04950_pg23_images/imageFile28.png>)

![](<2503.04950_pg23_images/imageFile29.png>)

![](<2503.04950_pg23_images/imageFile30.png>)

![](<2503.04950_pg23_images/imageFile31.png>)

![](<2503.04950_pg23_images/imageFile32.png>)

![](<2503.04950_pg23_images/imageFile33.png>)

![](<2503.04950_pg23_images/imageFile34.png>)

![](<2503.04950_pg23_images/imageFile35.png>)

![](<2503.04950_pg23_images/imageFile36.png>)

![](<2503.04950_pg23_images/imageFile37.png>)

![](<2503.04950_pg23_images/imageFile38.png>)

![](<2503.04950_pg23_images/imageFile39.png>)

![](<2503.04950_pg23_images/imageFile40.png>)

Figure 6: An N-labeling of ν = (4,3,3). The descents occur at cells (2,3),(3,1),(3,2),(3,3) yielding maj(σ) = 2 + 1 + 1 + 1 = 5. The inversion triples are formed by ((3,2),(3,1),(3,3)), ((1,2),(1,3)), and ((1,2),(1,4)) yielding inv(σ) = 3.

The reading order of a diagram ν is the order on cells that goes left-to-right along rows starting from the top row and working down. The standardization of a labeling σ : ν → N with content α = (α0,α1,···), denoted by st(σ), is an injective labeling σ : ν → {1,··· ,|ν|} that labels the 0’s appearing in ν 1,2,··· ,α0 in the order that they appear in the reading order. The 1’s appearing in ν are labeled α0 + 1,··· ,α0 + α1 in reading order and so on. A triple consists of cells with row-column coordinates of the form u = (r,c), v = (r − 1,c) and w = (r,c + k) for r,c,k ≥ 1, where u,w must be cells of ν, but v is allowed to be a cell immediately below ν. Extend st(σ) to cells immediately below ν by labeling them −∞. A triple is an inversion triple of σ if the labels st(σ)(u),st(σ)(w),st(σ)(v) are decreasing clockwise. The statistic inv(σ) counts the number of inversion triples of σ.

A descent of σ is a cell u = (r + 1,c) in ν, such that v = (r,c) is also in ν and σ(u) > σ(v). Letting Des(σ) denote that set of descents we deﬁne the major index statistic

(leg(u) + 1),

maj(σ) :=

u∈Des(σ)

where leg(u) is the number of cells of ν in the same column as u and above u. See Fig 6 for an example. Lemma 5.2.1. The monomial coeﬃcient [qitj]H˜µ[n],hη[n] stabilizes once n ≥ max(|µ|+µ1+|η|+i, |η|+η1). Proof. Fix partitions µ,ν and i,j and let M(n) denote the set of being enumerated in (26). Then

[qitj]H˜µ[n],hη[n] = |M(n)| and we wish to show |M(n)| stabilizes.

Suppose n ≥ |µ| + µ1 + |η| + i and n ≥ |η| + η1 so that µ[n] and η[n] are well-deﬁned. Deﬁne the map γn : M(n) → M(n+1) as follows. For σ ∈ M(n), shift the bottom row of the corresponding diagram to the right by one cell and insert a new cell labelled 0 in the bottom left corner. So for instance:

![](<2503.04950_pg23_images/imageFile41.png>)

![](<2503.04950_pg23_images/imageFile42.png>)

![](<2503.04950_pg23_images/imageFile43.png>)

![](<2503.04950_pg23_images/imageFile44.png>)

![](<2503.04950_pg23_images/imageFile45.png>)

![](<2503.04950_pg23_images/imageFile46.png>)

![](<2503.04950_pg23_images/imageFile47.png>)

![](<2503.04950_pg23_images/imageFile48.png>)

![](<2503.04950_pg23_images/imageFile49.png>)

1 0 2 0 0 4 3 1 0

γn :

![](<2503.04950_pg23_images/imageFile50.png>)

![](<2503.04950_pg23_images/imageFile51.png>)

![](<2503.04950_pg23_images/imageFile52.png>)

![](<2503.04950_pg23_images/imageFile53.png>)

![](<2503.04950_pg23_images/imageFile54.png>)

![](<2503.04950_pg23_images/imageFile55.png>)

![](<2503.04950_pg23_images/imageFile56.png>)

![](<2503.04950_pg23_images/imageFile57.png>)

![](<2503.04950_pg23_images/imageFile58.png>)

![](<2503.04950_pg23_images/imageFile59.png>)

![](<2503.04950_pg23_images/imageFile60.png>)

![](<2503.04950_pg23_images/imageFile61.png>)

![](<2503.04950_pg23_images/imageFile62.png>)

![](<2503.04950_pg23_images/imageFile63.png>)

![](<2503.04950_pg23_images/imageFile64.png>)

![](<2503.04950_pg23_images/imageFile65.png>)

![](<2503.04950_pg23_images/imageFile66.png>)

![](<2503.04950_pg23_images/imageFile67.png>)

![](<2503.04950_pg23_images/imageFile68.png>)

![](<2503.04950_pg23_images/imageFile69.png>)

![](<2503.04950_pg23_images/imageFile70.png>)

![](<2503.04950_pg23_images/imageFile71.png>)

![](<2503.04950_pg23_images/imageFile72.png>)

![](<2503.04950_pg23_images/imageFile73.png>)

![](<2503.04950_pg23_images/imageFile74.png>)

![](<2503.04950_pg23_images/imageFile75.png>)

![](<2503.04950_pg23_images/imageFile76.png>)

![](<2503.04950_pg23_images/imageFile77.png>)

![](<2503.04950_pg23_images/imageFile78.png>)

![](<2503.04950_pg23_images/imageFile79.png>)

![](<2503.04950_pg23_images/imageFile80.png>)

![](<2503.04950_pg23_images/imageFile81.png>)

![](<2503.04950_pg23_images/imageFile82.png>)

![](<2503.04950_pg23_images/imageFile83.png>)

![](<2503.04950_pg23_images/imageFile84.png>)

 → 1 0 2 0 0 0 4 3 1 0

![](<2503.04950_pg23_images/imageFile85.png>)

![](<2503.04950_pg23_images/imageFile86.png>)

![](<2503.04950_pg23_images/imageFile87.png>)

![](<2503.04950_pg23_images/imageFile88.png>)

![](<2503.04950_pg23_images/imageFile89.png>)

![](<2503.04950_pg23_images/imageFile90.png>)

![](<2503.04950_pg23_images/imageFile91.png>)

![](<2503.04950_pg23_images/imageFile92.png>)

![](<2503.04950_pg23_images/imageFile93.png>)

![](<2503.04950_pg23_images/imageFile94.png>)

![](<2503.04950_pg23_images/imageFile95.png>)

![](<2503.04950_pg23_images/imageFile96.png>)

![](<2503.04950_pg23_images/imageFile97.png>)

![](<2503.04950_pg23_images/imageFile98.png>)

![](<2503.04950_pg23_images/imageFile99.png>)

![](<2503.04950_pg23_images/imageFile100.png>)

![](<2503.04950_pg23_images/imageFile101.png>)

![](<2503.04950_pg23_images/imageFile102.png>)

![](<2503.04950_pg23_images/imageFile103.png>)

![](<2503.04950_pg23_images/imageFile104.png>)

![](<2503.04950_pg23_images/imageFile105.png>)

![](<2503.04950_pg23_images/imageFile106.png>)

![](<2503.04950_pg23_images/imageFile107.png>)

![](<2503.04950_pg23_images/imageFile108.png>)

![](<2503.04950_pg23_images/imageFile109.png>)

![](<2503.04950_pg23_images/imageFile110.png>)

![](<2503.04950_pg23_images/imageFile111.png>)

![](<2503.04950_pg23_images/imageFile112.png>)

![](<2503.04950_pg23_images/imageFile113.png>)

![](<2503.04950_pg23_images/imageFile114.png>)

![](<2503.04950_pg23_images/imageFile115.png>)

![](<2503.04950_pg23_images/imageFile116.png>)

We have to check that the map is well-deﬁned and surjective. We claim that the ﬁrst µ1 +1 entries of the bottom row of any σ′ ∈ M(n+1) are 0. Suppose for contradiction that there was a non-zero value a among these ﬁrst µ1+1 cells. Then there are at least n+1−|µ|−(µ1 +1) = n−|µ|−µ1 entries right of a. Of these, at most |η| − 1 are allowed to be non-zero (since a is one of the |η| non-zero values in the labeling). Hence a would contribute at least n − |µ| − µ1 − (|η| − 1) > i inversion triples formed by taking a, the phantom cell below it, and a 0 entry to the right of it. This contradicts that inv(σ′) = i for σ′ ∈ M(n+1).

This implies that if we let σ be obtained from a σ′ ∈ M(n+1) by deleting the bottom left cell and shifting the bottom row to the left by one, then σ ∈ M(n) and γn(σ) = σ′, which implies that γn is well-deﬁned and bijective. Indeed, the ﬁrst µ1 cells of the bottom row of σ will be labeled 0 and so the status of descents and inversion triples doesn’t change when going from σ′ to σ. Thus, σ′ and σ have the same inv and maj values.

![](<2503.04950_pg23_images/imageFile117.png>)

![](<2503.04950_pg23_images/imageFile118.png>)

![](<2503.04950_pg23_images/imageFile119.png>)

![](<2503.04950_pg23_images/imageFile120.png>)

23

