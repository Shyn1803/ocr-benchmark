8 ELENA CAVIGLIA, AMARTYA GOSWAMI & LUCA MESITI

Notice that ni = n1i ∧n2i . Thus,

(n1i ∧n2i ). Since (a1∧a2)∧ni ≠ 0 for each i, we get

ni =

2

2

i=1

i=1

0 ≠ (a1∧a2)∧ni = (a1∧a2)∧(n1i ∧n2i ) = (a1∧n1i )∧(a2 ∧n2i ). This implies that a1∧n1i ≠ 0 and a2∧n2i ≠ 0. Since a1↝µb↓1 and a2↝µb↓2, we have

n2i   ≠ 0. Thus,

n1i   ≠ 0 and a2∧

2

2

a1∧

i=1

i=1

(n1i ∧n2i )  ≠ 0. Therefore, (a1∧a2)↝µ(b1∧b2)↓.

(a1∧a2)∧ 

ni  = (a1∧a2)∧ 

2

2

i=1

i=1

(3) Let x1 and x2 be nonzero elements in b↓ such that x1∧x2 ≠ 0 and (a∧b)∧xk ≠ 0 for each k. This

implies a∧(b∧xk) ≠ 0 for each k. Also, observe that ⋀2k=1(b∧xk) = b∧(x1 ∧x2) = x1 ∧x2 ≠ 0. Since a is a µ-element in L, this implies that

(a∧b)∧(x1∧x2) = a∧

(b∧xk)  ≠ 0, proving the desired claim.

2

k=1

(4) We can assume a ≠ 0 and a ≠ 1, because otherwise b = 1 or b = 0 respectively, and the thesis holds. We can also assume that c  ⩽ b, because otherwise b∨c = b↝µb↑. Let x1 > b and x2 > b such that (x1∧x2) > b and ((b∨c)∧xk) > b, for each k. The latter condition is equivalent to b∨(c∧xk)> b, which is equivalent to c∧xk ⩽  b. We need to show that

(b∨c)∧x1 ∧x2 > b,

which is equivalent to c∧x1 ∧x2  ⩽ b. Since b is a pseudo-complement of a in L, c∧x1 ∧x2  ⩽ b holds if and only if

a∧c∧x1 ∧x2 ≠ 0.

Now, consider the elements a,x1,x2 ∈ L. a∧x1 ∧x2 ≠ 0 because otherwise we would have x1 ∧x2 ⩽ b, as b is a pseudo-complement of a. Moreover c∧xk ≠ 0 for each k, because otherwise we would have c∧xk ⩽ b. Finally c∧a ≠ 0, because otherwise c ⩽ b, contradicting our assumption. As c is a µ-element in L, we conclude that c∧a∧x1 ∧x2 ≠ 0, which proves the claim.

![](<2503.06739_pg8_images/imageFile1.png>)

![](<2503.06739_pg8_images/imageFile2.png>)

![](<2503.06739_pg8_images/imageFile3.png>)

![](<2503.06739_pg8_images/imageFile4.png>)

Remark 3.16. — An analogue of part (2) of Proposition 3.15 does not hold for upsets. Consider the frame of power set P(X) of the set X = {1,2,3,4,5}. We have {1,2}↝µ{1}↑ and {3,4}↝µ{3}↑, by Remark 3.12. However, it is easy to see that {1,2}∨{3,4} = {1,2,3,4} is not a µ-element in {1,3}↑ = {1}∨{3}↑. Moreover, it is also not a µ-element in P(X).

Proposition 3.17. — Let L be a frame, a ∈ L, and b a pseudo-complement of a in L. If c ∈ L is maximal relative to the properties a ⩽ c and b∧c = 0, then a↝µc↓.

