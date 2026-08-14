subgraph of G is the intersection graph of a compatible collection of subtrees of T. Thus, by Theorem 3.2 it suffices to show that G has a simple vertex.

Let V (G) = {v1,...,vn} and let T1,...,Tn be subtrees of T in Λ satisfying vi ∼ vj in G if and only if V (Ti) ∩ V (Tj) ̸= ∅. For each i, let wi be the unique vertex of Ti of minimum weighted distance to r. We may assume, without loss of generality, that dT(w1,r) ≥ dT(wj,r) for j = 2,...,n. We claim that v1 is simple in G. Suppose that vi,vj ∈ NG(v1) and Ti > Tj. It suffices to show that NG(vj) ⊆ NG(vi). Since

dT(w1,r) ≥ dT(wj,r) and

V (T1) ∩ V (Tj) ̸= ∅ it follows that

w1 ∈ V (Tj). Similarly

w1 ∈ V (Ti). Since Ti > Tj we have

wj ∈ V (Ti). Let vk ∈ NG(vj). Then

V (Tj) ∩ V (Tk) ̸= ∅. If wj ∈ V (Tk) then V (Ti) ∩ V (Tk) ̸= ∅. Otherwise

wk ∈ V (Tj) dT(r,wk) ≤ dT(r,w1)

and

w1 ∈ V (Ti) ∩ V (Tj) whence

wk ∈ V (Ti) since Ti > Tj. In either event

V (Ti) ∩ V (Tk) ̸= ∅ and so

vk ∈ NG(vi). Since vk was an arbitrary vertex of NG(vj), it follows that NG(vj) ⊆ NG(vi)

.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


14

