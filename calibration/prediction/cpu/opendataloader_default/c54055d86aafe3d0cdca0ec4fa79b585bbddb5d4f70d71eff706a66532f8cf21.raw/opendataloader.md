8 KABALAN GASPARD

The equation can be solved using cyclotomy and quadratic residues. A partial solution was found by Dirichlet using this method, building upon the work of Gauss [3]. In this section, we build upon Dirichlet’s work, explicitly writing the solution and using the modern machinery of Galois Theory to streamline the approach. Again, we let p be an odd prime, and deﬁne p∗ = (−1)

2 p, i = √

p−1

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile1.png>)

−1, and start by introducing an important lemma.

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile2.png>)





Lemma 3.



als in Z[x].

q1(x) = 2

1≤k<p

(

k p

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile3.png>)

q−1(x) = 2

(

k p

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile4.png>)

(x − ζk) = f(x) + √p∗g(x)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile5.png>)

)=1

√p∗g(x)

(x − ζk) = f(x) −

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile6.png>)

1≤k<p

)=−1

where f(x), g(x) are polynomi-

(x− ζk) = 4mp(x) ∈ Z[x]. It is therefore ﬁxed by any Galois automorphism in Gal(K : Q). Now taking θ = ζ

Proof. Note that the product of the 2 above polynomials (on the left-hand side) is 4

1≤k<p

p−1 2

p2−1 8

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile7.png>)

p2−1

(1 − ζk)2, we see that θ2 = p∗ since (−1)

8 ≡ p 2 (mod 2), and trivially θ ∈ OK. So √p∗ ∈ OK, Now an automorphism σ in the Galois group ﬁxes p∗ if and only if σ is a square. But this is if and only if σ ﬁxes all (and only) the ζk such that k is a quadratic residue modulo p. So

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile8.png>)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile9.png>)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile10.png>)

k=1

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile11.png>)

(x − ζk) ∈ L[x] where L = Q(√p∗). All the

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile12.png>)

1≤k<p

(

)=1

k p

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile13.png>)

coeﬃcients in L[x] are of the form a + b√p∗ where a and b are both rational, and 12· an algebraic integer (allowing for the fact that p∗ ≡ 1 (4)). The coeﬃcients of 2

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile14.png>)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile15.png>)

(x − ζk)

1≤k<p

(

)=1

k p

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile16.png>)

are therefore rational algebraic integers and thus in Z. We can now expand q1(x) and rewrite it as q1(x) = f(x) + √p∗g(x) where f(x), g(x) are polynomials in Z[x].

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile17.png>)

A similar argument shows that q−1(x) ∈ L[x]. Now let τ be the Galois automorphism in Gal(K : Q) deﬁned by τ(√p∗) = −

√p∗ (noting that K : L : Q is a tower of ﬁelds). Then by

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile18.png>)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile19.png>)

the above, and since τ2 must ﬁx q1(x), we must have that τ(ζk) = ζl where kp p l = −1. So since τ is a Galois automorphism over K, we must have τ(q1(x)) = q−1(x). This yields that q−1(x) = f(x) −

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile20.png>)

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile21.png>)

√p∗g(x).

![](<c54055d86aafe3d0cdca0ec4fa79b585bbddb5d4f70d71eff706a66532f8cf21_images/imageFile22.png>)

We will primarily consider the case where d is an odd prime. Pell’s Equation then becomes

(3.1) x2 − py2 = 1

