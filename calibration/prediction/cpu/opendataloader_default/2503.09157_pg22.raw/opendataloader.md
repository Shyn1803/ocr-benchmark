So

∥∂IΦ(n,I) · h∥∞ ≥ ∥h∥∞. (43) Therefore, ∂IΦ(n,I) is a global diffeomorphism on C0([0,T],R) and according to (43)

∂IΦ(n,I) −1 ≤ 1.

<table>
  <tr>
    <td>ineq:diffÃľo</td>
  </tr>
</table>


Hence, according to the implicit function Theorem, we can find a function F ∈ C1 X,C0([0,T],R+) such that

∀n ∈ X, Φ(n,F(n)) = 0. i.e.

∞ 0

r(F(n)(t),x)n(t,x)dx. (44) Finally

∀t ∈ [0,T],F(n)(t) =

<table>
  <tr>
    <td>eq:fonction_implicite</td>
  </tr>
</table>


∥∂nF(n)∥ ≤ ∂IΦ(n,I) −1 ∂nΦ(n,I) ≤ 1 × rM. Hence, F is rM-lipschitzian on X.

Now, if µ1,µ2 are two solutions of (26), associated to the activity function I1,I2 ∈ C0([0,T],R) with µ1(0) = µ2(0) = nini, then, according to Lemma 6.2,

t 0

∀t ∈ [0,T], ∥µ1(t) − µ2(t)∥1 ≤ ∥µ1(0) − µ2(0)∥1 + 2∥∂Ir∥∞

∥I1(τ) − I2(τ)∥∞dτ

Then, since µ1(0) = µ2(0) = nini, we obtain

∀t ∈ [0,T], ∥µ1(t) − µ2(t)∥1 ≤ 2T∥∂Ir∥∞∥I1 − I2∥∞. And so

∥µ1 − µ2∥X ≤ 2T∥∂Ir∥∞∥I1 − I2∥∞.

Finally, if n1,n2 ∈ X, and µ(n1),µ(n2) ∈ X are the two solutions associated to the activity functions I1 = F(n1) and I2 = F(n2) and with µ1(0) = µ2(0) = nini, then,

∥µ(n1) − µ(n2)∥X ≤ 2T∥∂Ir∥∞∥I1 − I2∥∞. ≤ 2T∥∂Ir∥∞rM∥n1 − n2∥X

Now, if we take T > 0 such that 2T∥∂Ir∥∞rM < 1, then the function n  → µ(n) is a contraction on X and therefore, according to Picard Fixed point Theorem, there exist a unique function on X such that µ(n) = n. This function is the solution of (1) on [0,T].

<table>
  <tr>
    <td>lem: Estimation n par rapport a r</td>
  </tr>
</table>


Finally, we use the same argument on every interval [kT,(k + 1)T], with k ∈ N to prove that the solution n is uniquely and well-defined on R+. Lemma 6.2. Let µ1 and µ2 be the solution of (26) with respectively r1(t,x) := r(x,I1(t)) and r2(t,x) = r(x,I2(t)), µ1(0) = µ01 and µ2(0) = µ02. Then,

<table>
  <tr>
    <td> </td>
  </tr>
</table>


∀t ≥ 0,∥µ1(t) − µ2(t)∥1 ≤ ∥µ01 − µ02∥1 + 2∥∂Ir∥∞

t 0

∥I1(τ) − I2(τ)∥∞dτ.

22

