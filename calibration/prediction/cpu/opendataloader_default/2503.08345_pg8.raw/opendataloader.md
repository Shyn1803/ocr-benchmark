4.3 Spectral analysis

We can now derive specific spectral properties of the Koopman operator that we will leverage for state estimation. Those properties require the following additional assumptions on the nonlinear system (6).

- Assumption 3 (stable hyperbolic equilibrium). The dynamics admits a stable equilibrium at the origin, whose basin of attraction contains the polydisc Dn. Moreover, the eigenvalues λj of the Jacobian matrix JF(0) are simple and satisfy Re(λj) < 0 for all j = 1,...,n.

- Assumption 4 (non-resonant eigenvalues). The eigenvalues λj of the Jacobian matrix JF(0) are non-

resonant, i.e. for all (m1,...,mn) ∈ Nn satisfying n l=1 ml ⩾ 2,

λj ̸=

n

l=1

mlλl, ∀j = 1,...,n.

- Assumption 5 (output map). The components of the output map h belong to H2(Dn).


Remark 14 Nonresonant eigenvalues are required to rely on the Poincare´-Dulac linearization theorem. However, other linearization theorems exist, with different assumptions, see e.g. the Siegle-Bruno theorem in [Bernard, 2023]. In [Krener and MingQing, 2001], similar assumptions were considered to obtain a necessary and sufficient condition for the existence of a change of variable that linearizes the dynamics up to a nonlinear injection term.

The first remarkable property resulting from those assumptions is the fact that the operators AF and A∗F admit a series expansion that allows to represent both operators as infinite matrices.

Lemma 15 For all f ∈ D(AF),

 

 eα

AFf =

AFα,βfβ

α∈Nn

β∈Nn

where fβ = ⟨f,eβ⟩ and AFα,β = ⟨AFeβ,eα⟩.

PROOF. Since {eα}α∈Nn is an orthonormal basis of H2(Dn), any f ∈ D(AF) can be expanded as f = β∈Nn fβeβ. Hence, we can prove that

 

  =

fβeβ

fβAFeβ. (15)

AF

β∈Nn

β∈Nn

Indeed, in [Mugisho and Mauroy, 2024], it is shown that the right-hand side is given by

fβAFeβ

β∈Nn

n

=

Fl

β∈Nn

l=1

(βl + 1)f(β

1,...,βl−1,βl+1,βl+1,...,βn)eβ.

(16)

It remains to show that the left-hand side of (15) is also equal to the right-hand side of (16). To do so, consider the operators A1 and A2 given by

A1f = ∇f and A2ω = F · ω,

for all f ∈ D(AF) and ω ∈ (Hol(Dn))n, respectively. Observe that AF = A2A1 on D(AF). Moreover, for all f ∈ D(AF) and for all l = 1,...,n,

(A1f)l =

(βl + 1)f(β

1,...,βl−1,βl+1,βl+1,...,βn)eβ.

β∈Nn

Hence, for all f ∈ D(AF), AFf = A2A1f

n

=

Fl

(βl + 1)f(β

1,...,βl−1,βl+1,βl+1,...,βn)eβ.

β∈Nn

l=1

In view of (16), it follows that identity (15) holds, which implies that

⟨AFf,eα⟩eα

AFf =

α∈Nn

 

 ,eα eα

=

AF

fβeβ

α∈Nn

β∈Nn

⟨AFeβ,eα⟩fβ eα.

=

α∈Nn β∈Nn

■

It is proved in [Mugisho and Mauroy, 2024] that the infinite matrix representation AF of the operator AF is lower block triangular of the form

AFf =







[0] ··· [0] [A11] [0] ··· [0] [A21] [A22] [0] ···

 

 

 

...

. . . .



- [f0]
- [f1]
- [f2]


, (17)

 

.

8

