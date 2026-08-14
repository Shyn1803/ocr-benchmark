introduction applications, and highlights their relevance to the study of TDI systems and to a long standing conjecture of Paul Seymour on ideal clutters.

# 1.1 Totally dual in L systems

Consider a prime p. A rational number is p-adic if it is of the form rs where r,s ∈ Z and s is an integer power of p [2]. A number is dyadic if it is 2-adic. Let S be a (possibly infinite) set of primes. We

denote by L(S) the set of all rationals of the form rs where r,s ∈ Z and s is a product of integer powers of primes in S. Observe that L({p}) denotes the p-adic rationals. To keep the notation light, we write

Lp for L({p}). For any set of primes S, L(S) is a heavy set (this follows from [3, Lemma 2.1]).

For a system Mx ≤ b to be TD in L we consider the dual (D:M,b,w) for all choices of w ∈ Ln. However, for the aforementioned heavy sets, it suffices to consider the choices w ∈ Zn. Namely, Remark 1.1. Let L := L(S) where S is a set of primes. Then Mx ≤ b is TD in L if and only if for every admissible w ∈ Zn, (D:M,b,w) has an optimal solution in Lm.

Proof. Necessity is clear, let us prove sufficiency. Consider an admissible w ∈ Ln. For some µ that is a product of integer powers of primes in S we have µw ∈ Zn. There exists an optimal solution y¯ ∈ Ln for (D:M,b,µw). However, then µ1y¯ is a solution for (D:M,b,w) that is in Ln.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


For any prime p, we can find a system Mx ≤ b that is TD in Lp but not TD in Lq for any prime q ̸= p. Namely, one can pick Mx ≤ b to consist of a unique constraint, px ≤ 1. However, if we require a system to be TD in Lp and TD in Lp′ for distinct primes p and p′, then it is totally dual in Lq for every prime q [2, Theorem 1.4]. The following stronger statement (the aforementioned case corresponds to S1 = {p},S2 = {p′} and k = 2) holds in the full dimensional case,

Theorem 1.2. Let Mx ≤ b be a system where {x : Mx ≤ b} is a full-dimensional polyhedron. For i = 1,...,k, let Si be a set of primes and suppose that Mx ≤ b is TD in L(Si). If ∩i∈[k]Si = ∅ then Mx ≤ b is TD in Lq for every prime q.

This will be an immediate consequence of Theorem 2.2.

Consider an integral matrix M and an integral vector b. A necessary condition for Mx ≤ b to be TDI is that the polyhedron Q = {x ∈ Rn : Mx ≤ b} be integral, i.e., that every minimal proper face of Q contains an integral vector [10], see also [20, Corollary 22.1a]. However, this is not a sufficient condition [20, Equation (3) in Chapter 22]. Let us define a stronger necessary condition for a system to be TDI. We say that Mx ≤ b is near-TDI if for every prime p, Mx ≤ b is TD in Lp. Since Z ⊂ Lp for every prime p, it then follows from Remark 1.1 that if a system is TDI, it is near-TDI.

Furthermore, we have the following result [3, Theorem 1.5],

2

