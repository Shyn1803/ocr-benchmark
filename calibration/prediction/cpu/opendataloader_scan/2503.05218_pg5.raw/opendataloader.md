Remark: The condition in (5) is best possible. For instance, there is a tripartite graph G with densities α = 1 − 1 /n + α ′ n ( δ a − 2) ,β = 1 − 1 /n + β ′ n ( δ b − 2) ,γ = 1 − 1 /n + γ ′ n ( δ c − 2) satisfying α ′ β ′ n ( δ a + δ b − 1) + γ ′ n ( δ c − 1) = 1 such that G does not have a triangle-factor. To see this, consider a tripartite graph G with parts A , B and C . Denote the edge densities of G [ A,B ], G [ A,C ] and G [ B,C ] by α , β and γ , respectively. Let x ∈ A , B 1 be a subset of B such that | B 1 | = αn 2 − n ( n − 1) and C 1 be a subset of C such that | C 1 | = β 2 − n ( n − 1). Define the edge set of G to be the set of all edges between A \ { x } and B , A \ { x } and C , { x } and B 1 , { x } and C 1 .

The rest of the paper is organized as follows. In Section 2, we will introduce notions and calculations needed for our proofs. Section 3 is devoted to prove our main result. In section 4, we will prove the triangle-factor case.

# 2 Preliminaries

Let

$$

$$

and

$$

$$

R 1 and R 2 is a partition of R such that

$$
R1
$$

2 \ 1 Let T min ( α,β,γ ) denote the minimum number of divided by n 3 . From [BJT10], we have the following:

Theorem 2.1 (

Conjecture 2.1 ( 2 γ − 2 .

For integers n > r ≥ 1, let [ n ] := { 1 , 2 , ··· ,n } be the standard n element set and   [ n ] r   = { T ⊆ [ n ] : | T | = r } be the collection of all its r -subsets. An n -vertex r -uniform hypergraph H is a pair H = ( V,E ), where V := [ n ] and E ( H ) ⊂   [ n ] r   . Let ν ( H ) be the matching number of H , that is, the maximum number of pairwise vertex-disjoint members of E ( H ). An r -uniform hypergraph H is called n -balanced r -partite if V ( H ) is partitioned into sets V 1 ,V 2 ,...,V r such that | V 1 | = | V 2 | = ··· = | V r | = n and each hyperedge meets every V i in precisely one vertex. Aharoni and Howard [AH17] showed the tight hyperedge density needed to guarantee the existence of a matching of size k in an n -balanced r -partite r -uniform hypergraphs. (see Observation 1.9 in [AH17])

Lemma 2.2 (Aharoni and Howard [AH17]) . If H is an n -balanced r -partite r -uniform hypergraph and e ( H ) > ( k − 1) n r − 1 then ν ( H ) ≥ k and the bound is tight.

For a graph G and U ⊆ V ( G ), we use G − U to denote the subgraph of G induced by V ( G ) \ U , and we use G [ U ] to denote the subgraph of G induced by U . For a graph G and E ⊆ E ( G ), we use H − E to denote the graph obtained from G by deleting E .

