Proof. One has to impose d1,1 = 0 and dp,j = 0 in eq. (5.7). Then, coefficients ωi,j vanish, because all the successive commutators [K(h),...,[K(h), K(h)]...] appearing in the BCH formula applied to eK(h) e K(h) contain only pure imaginary terms up to order O(h2p+1) .

<table>
  <tr>
    <td> </td>
  </tr>
</table>


In consequence, if the problem (5.1) is defined in a Lie group G , then the scheme Sh of order p is conjugate to a method that preserves the Lie group structure up to order 2p+1 .This is so up to order 2p+2 if Ψh is symmetric-conjugate and the order p is even, due to the particular structure of Kh in that case [5]. On the other hand, if Ψh is symmetric-conjugate and its order p is odd, then the resulting AC method is time-symmetric and of order p + 1 .

# 5.2 New alternating-conjugate methods

The analysis of the previous subsection shows that, in addition to concatenating a given method Ψh of order p (say palindromic or symmetric-conjugate) with the same scheme with complex conjugate coefficients, one

can also get an alternating-conjugate method of order p ≥ 2 by considering Ψh as in Proposition 5.1, namely by requiring the following order conditions:

- 1

- 2


ℜ(k1,1) =

, ℜ(kp,j) = 0; j = 1,...,c(p) kℓ,j = 0, ℓ = 2,...,p − 1; j = 1,...,c(ℓ).

(5.12)

The simplest AC method of order p = 2 corresponds of course to the composition Sh = Φαh Φαh with

Φαh = eK(h) and K(h) = αhM + α2h2Y2 + α3h3Y3 + ··· . By imposing ℜ(α) = 21,ℜ(α2) = 0 we get α = 12(1 ± i) , i.e., we recover method (5.2).

Analogously, for an AC method of order 3 within this family one has to take Ψh = Φα1h Φα2h Φα3h to satisfy the 5 required conditions (5.12). Although there are solutions with α3 ∈ R , it is more efficient to consider Φh in the composition (5.4) as a 2nd-order time-symmetric method, namely

Ψh = Ψ[2]α

1h Ψ[2]α

2h ··· Ψ[2]α

rh. (5.13)

Now the number of order conditions (5.12) to achieve a method of order 3, 4, 5, 6 is, respectively, 2, 4, 7 and 11. This is the strategy we follow next to construct higher order schemes with the minimum number of basic methods (or stages). We denote, for brevity, the whole AC method by its sequence of coefficients:

## Sh = (α1,α2,...,αr,α1,α2,...,αr).

Order 3. The two order conditions, ℜ(k1,1) = 12,ℜ(k3,1) = 0 can be satisfied with just one basic scheme, Ψ[2]α

1h , if

- 1

- 2 ± i


- 1

- 2√3


α1 =

.

In this way we recover the scheme (2.5), which is both symmetric-conjugate and AC. Notice that if Ψ[2]h is taken as the Strang splitting (2.3) for two operators, then the number of exponentials is 5 instead of 12 with

a composition of the Lie–Trotter scheme.

23

