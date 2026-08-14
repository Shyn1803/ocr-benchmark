Therefore, assuming that the first child of the root is j ∈ {1,...,d} (equivalently, that the

minimal label of σ(j)⊔ l̸=j σ(l) belongs to the jth component), and using this counting principle, one get the recursive formula

 

  |σ| − 1

d

d

|σ(j)| |σ| − 1

dk(∅,σ(k)), (4.17)

d(∅,σ) =

w∅,j

|σ(1)|,...,|σ(d)|

j=1

k=1

where dk denotes the combinatorial dimension in which the weights wi,ij are replaced by wki,kij, and k n

1,···,kd denotes the usual multinomial coefficient. Thereafter, the proof of the lemma follows by induction. By using Lemma 4.1, we obtain results similar to those in Theorem 3.1. The proof follows

<table>
  <tr>
    <td> </td>
  </tr>
</table>


from simple calculations and is omitted.

- Corollary 4.3. The normalized extremal NNHFs of this WBD take the form

φ(τ) =

i∈τ

αi

i∈τ◦

αi

d j=1 αijwi,ij

, (4.18)

with α∅ = 1 and αi = αi1 + ... + αid ∈ [0,1] for any i ∈ Sd. Again, the αi represents the asymptotic proportion of descendants of i in a regular path.

Besides, the corresponding saturated ergodic central Markov kernel is then given by

p(τ,τ ⊔ {ij}) =

 



αijwi,ij

d k=1 αikwi,ik

αi, if i ∈ ∂τ,

αij, if i ∈/ ∂τ and ij ∈/ τ,

(4.19)

for any i ∈ τ and j ∈ {1,...,d}. As a consequence, we obtain the following generalization of Han’s hook length formula (4.3).

- Corollary 4.4. Let Bd(n) be the set of all d-ary trees with n vertices. Then


d j=1 |τ(vj)|wj

|∂τ|

n

w1 + ··· + wd d

w1 + ··· + wd d

v∈τ◦

1 n!

|τ(v)|−1

. (4.20)

=

|τ(v)|d|τ(v)|−1

τ∈Bd(n)

v∈τ

Proof. Consider the uniform fragmentation measure case as in Section 4.1, that is αi = d−|i| and wi,ij ≡ wj for all i ∈ Sd and 1 ≤ j ≤ d.

By using (4.2) and by noting that

|τ|−|∂τ|

αi

d

, (4.21)

=

d j=1 αijwi,ij

d j=1 wj

i∈τ◦

we deduce the result from (4.18) and the general combinatorial identity (7.5). As an example, when d = 2 and n = 3, we obtain

<table>
  <tr>
    <td> </td>
  </tr>
</table>


3

3

1 6

w1 + w2 2

1 12

w1 + w2 2

1 48 1≤i,j≤2

w1 + w2 2

=

+

wiwj

.

It is much more difficult to describe the MERWs in full generality. However, drawing on the previous situation, one can construct them using appropriate IDLA-like random walks under some additional assumptions.

25

