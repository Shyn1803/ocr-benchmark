where Rε = R2ε +div(R1ε)+R3ε +R4ε and C1 is some positive constant independent of ε. Therefore, lim

G(I + εh) − G(I) ε − (ξ,η)

(ξ,˜ η˜)

= 0. This establishes the Gâteaux differentiability of G at I in the direction h, with G′(I)h = (ξ,η). Now, we establish a result on the differentiability of the cost functional:

= lim

ε→0

ε→0

X

X

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Theorem 4.1 (On the Gâteau-differentiability of the Cost Functional). Let Assumptions (A1)(A10) hold. Then the cost functional J is Gâteaux differentiable at any I ∈ Uad. Furthermore, for any direction h ∈ L∞(0,T), the Gâteaux derivative of J at I in the direction h is given by:

T

ξ(T,x)dx (45)

⟨J′(I),h⟩ =

α

ξ(t,x)dx + 2βI(t)h(t) dt + γ

RN

RN

0

where (ξ,η) is the solution to the linearized system (35). Proof. Let I ∈ Uad and define the functional LI : L∞(0,T) → R by:

T

ξ(T,x)dx (46)

⟨LI,h⟩ =

ξ(t,x)dx + 2βI(t)h(t) dt + γ

α

RN

RN

0

where (ξ,η) solves the linearized system (35) with the direction h. Now let h1,h2 ∈ L∞(0,T) and λ ∈ R, and let us consider h = h1+λh2, with (ξ1,η1) and (ξ2,η2) are the solutions to the linearized system corresponding to directions h1 and h2 respectively. By the linearity of system (35), the solution (ξ,η) corresponding to h satisfies ξ = ξ1 + λξ2 and η = η1 + λη2. Consequently:

T

⟨LI,h1 + λh2⟩ =

(ξ1 + λξ2)(T,x)dx

(ξ1 + λξ2)dx + 2βI(t)(h1(t) + λh2(t)) dt + γ

α

RN

RN

0

= ⟨LI,h1⟩ + λ⟨LI,h2⟩.

Therefore LI is linear. Furthermore, for any h ∈ L∞(0,T), by using the estimates from Lemma 4.1 we obtain:

T

|⟨LI,h⟩| ≤ α

|ξ(t,x)|dxdt + 2β∥I∥L∞∥h∥L∞T + γ

|ξ(T,x)|dx ≤ C1∥h∥L∞(0,T),

0 RN

RN

where C1 is a positive constant depending on α, β, γ, T, and the bounds from Lemma 4.1. Therefore LI is continuous.

To show that LI represents the Gâteaux derivative of J, let h ∈ L∞(0,T), ε > 0, and let define Iε = I + εh and let (pε,dε) = G(Iε) and (p,d) = G(I). Let define ΦI(ε) =

J(Iε) − J(I) ε

, we have:

T

(Iε)2 − I2 ε

pε(T,x) − p(T,x) ε

pε − p ε

dx + β

dt + γ

dx

ΦI(ε) =

α

RN

RN

0

T

ξεdx + β(2Ih + εh2) dt + γ

ξε(T,x)dx

=

α

RN

RN

0

where ξε = (pε − p)/ε. By Lemma 4.1, we have ξε → ξ in X as ε → 0, where ξ is the solution to the linearized system (35). Therefore:

T

ξ(T,x)dx = ⟨LI,h⟩. (47)

lim

ΦI(ε) =

α

ξ(t,x)dx + 2βI(t)h(t) dt + γ

ε→0

RN

RN

0

This establishes that J is Gâteaux differentiable at I with derivative J′(I) = LI, which complete the proof.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


18

