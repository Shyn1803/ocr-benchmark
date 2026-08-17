actions, extending the original framework. Other examples include the work of Gnilke and Zumbr¨agel [ 15 ], who linked Maze et al.’s ideas to recent advances in isogeny-based cryptography. Additionally, [ 16 ] introduced a key-exchange protocol based on twisted group rings, incorporating a group key-exchange agreement. In this research, Grigoriev and Shpilrain proposed the use of tropical semiring

for public key exchange [ 2 ], [ 3 ] and for digital signatures [ 4 ]. Nevertheless, the ﬁrst attempt was analyced by [ 5 ], where it was introduced the so called Kotov-Ushakov attack, an heuristic attack that knowadays has become the standar attack against tropical cryptography. In [ 6 ], the authors propose a new deterministic attack against a public key exchange protocol based on tropical semiring, that improve the KotovUshakov attack in the sense that it can be used in the sames scenarios, but with a deterministic output. In addition, the other two tropical cryptographyc protocols proposed by Grigoriev and Shpilrain has been proven not secure in [ 9 ], [ 7 ] and [ 8 ]. Far from being abandoned, this ideas has been further explored. In [ 17 ], the authors

recently proposed the use of triad matrix semiring. This semiring is a generalization of tropical semiring where elements are a vector of 3 entries, and with a modiﬁed addition and multiplication that endow them with the structure of semiring. Based on them, the authors stablish a public key exchange protocol that use matrix with entries over triad semiring.

# 2 Results

In this paper, we introduce an isomorphism between triad semiring and circuland matrix over tropical semiring. As a result, it is possible to satblish an isomorhism between triad matrix semiring and tropical matrix semiring, and therefore reinterpretate the public key exchange in terms of tropical matrix. This prove that the previous protocol can be seen as the Stickel protocol where instead of taking a polynomial, only a monomial is used. Finally, this protol is suscentible to the attack introduced in [ 18 ] .

# 3 Preliminaries

In this secition we will introduce some basic background on tropical semiring as well as triad semiring.

Deﬁnition 1 A semiring R is a non-empty set together with two operations + and · such that ( S, +) is a commutative monoid, ( S, · ) is a monoid and the following distributive laws hold:

$$
a(b + c) = ab + ac (a + b)c = ac + bc
$$

Deﬁnition 2 Let R be a semiring and ( M, +) be a commutative semigroup with identity 0 M . M is a right semimodule over R if there is an external operation · : M × R → M such that

