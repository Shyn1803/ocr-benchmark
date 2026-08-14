![](<2503.05506_pg11_images/imageFile1.png>)

Figure 8: When 1 ≤ j ≤ 25s, the edge vijvij+1 of G lies in a cycle of each length in [3,600s]

Consider the edges vi1vj1,vi50svj1 ∈ E4, where 1 ≤ i,j ≤ sℓ. For each p ∈ [3,50s], vj1vi1vi2 ...vip−2vi50svj1 is a cycle of length p containing vi1vj1 and vi50svj1 (see Figure 7). Consider the edges vi50svj50s,vi50s+1vj50s ∈ E4, where 1 ≤ i,j ≤ sℓ. For each 4 ≤ p ≤ 50s, vj50svi50svi50s+2 ...vi50s+p−2vi50s+1vj50s

is a cycle of length p containing vi50svj50s and vi50s+1vj50s (see Figure 7). And vj50svi50svi50s+1vj50s is a C3 containing both edges (see Figure 7).

Then we can use the similar cycle C⋆ as in Claim 8 and the similar replacement to prove every edge in E4 is contained in a cycle of length k if j ̸∈ {τi2,τi2 + sℓ−1,τi2 + sℓ−1 − s,τi2 + sℓ−1 − 2s,τi2 + 2sℓ−1 − 2s,...,τi1}, where 3 ≤ k ≤ 600s. When j ∈ {τi2,τi2 + sℓ−1,τi2 + sℓ−1 − s,τi2 + sℓ−1 − 2s,τi2 + 2sℓ−1 − 2s,...,vτ1

}, we can replace τi2 with τˆi2 := τi2 + s and add a vertex vτˆ2

i +sℓ−1−3s between vτˆ2

i +sℓ−1−2s and vτˆ2

i

i +2sℓ−1−2s in C⋆. Then we use a similar replacement to prove such edges in E4 are contained in a cycle of length k, 3 ≤ k ≤ 600s. Claim 10. Every edge in E3 lies in a cycle of length k, 3sℓ + 100s ≤ k ≤ v(G). Proof of Claim 10. Notice that for every 3 ≤ p ≤ 100s − 1, there is a path of length p contained in the copy of H(s) in G connecting vi and vi+1, where i ∈ [sℓ] and vi,vi+1 ∈ V (G1). Moreover, every edge in E3 lies in a path of length 100s−1 contained in the copy of H(s) in G connecting vj and vj+1 for some j ∈ [sℓ], where vj,vj+1 ∈ V (G1). Thus using the Hamilton cycle in G1, we can find a cycle of each length k, k ≥ 3sℓ + 100s containing e for every e ∈ E3.

11

