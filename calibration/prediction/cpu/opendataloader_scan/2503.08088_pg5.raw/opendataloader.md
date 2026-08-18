For a set X ⊆ V ( G ), the (open) neighborhood of X , denoted by N G ( X ), is the set { v ∈ V ( G ) \ X : v is adjacent to a vertex in X } . The closed neighborhood of X is the set N G [ X ] = N G ( X ) ∪ X . We simply use N ( v ) ,N [ v ] ,N ( X ), and N [ X ] to denote N G ( v ) ,N G [ v ] ,N G ( X ) , and N G [ X ], respectively when the context of the graph G is clear. We use G [ X ] to denote the subgraph of G induced by the vertices in X . A vertex v dominates itself and all its neighbors. A set X ⊆ V ( G ) is called a clique of G if every pair of vertices of X are adjacent. For disjoint subsets X and Y of V ( G ), G [ X,Y ] denotes the set of edges { e ∈ E ( G ) : e has one endpoint in X and the other endpoint in Y } . If the graph G is clear from the context, we write [ X,Y ] rather than G [ X,Y ]. We say that G [ X,Y ] is complete if every vertex in X is adjacent to every vertex in Y in G . For a given positive integer k , we use the notation [ k ] to denote the set { 1 ,... ,k } .

For a set D ⊆ V ( G ) and a vertex u ∈ D , the D -external private neighborhood of u , denoted by epn( u,D ), is the set { v ∈ V ( G ) \ D : N ( v ) ∩ D = { u }} . A vertex in epn( u,D ) is a D -external private neighbor of u . We say that a vertex v ∈ V ( G ) \ D is D defended if there exists a vertex u ∈ N ( v ) ∩ D such that ( D \ { u } ) ∪ { v } is a dominating set of G . Speciﬁcally, we say that v ∈ V ( G ) \ D is D defended by a vertex u if u ∈ N ( v ) ∩ D and ( D \ { u } ) ∪ { v } is a dominating set of G . We note that D is a secure dominating set of G if and only if every vertex in V ( G ) \ D is D -defended. We also note that if D is a dominating set of G and epn( u,D ) = ∅ for some u ∈ D , then every neighbor of u in V ( G ) \ D is D -defended by u . We state this observation formally as follows.

Observation 2. If D is a dominating set of a graph G and epn( u,D ) = ∅ for some vertex u ∈ D , then every neighbor of u that belongs to V ( G ) \ D is D -defended by u .

As a consequence of Observation 2 , if D is a dominating set of G and epn( u,D ) = ∅ for every u ∈ D , then every vertex in V ( G ) \ D is D -defended, implying that D is a secure dominating set of G . For a given dominating set D of G , we partition D as A D ∪ B D , where the sets A D and B D are deﬁned as follows.

- A D = { u ∈ D : there exists a neighbor of u in V ( G ) \ D that is not D -defended. } ( P 1 )
- B D = D \ A D .


We now prove the following useful lemma. We remark that some of the facts that appear in the following lemma have appeared implicitly in several papers (see [ 4 , 15 ]).

Lemma 1. Let D be a dominating set of G and A D ∪ B D be a partition of D as deﬁned in ( P 1 ) .

- (a) If A D = ∅ , then D is a secure dominating set of G .
- (b) If a vertex v in V ( G ) \ D is not D -defended, then N ( v ) ∩ D ⊆ A D .


(d) has 0 non-neighbor in epn(u; D), that is, epn(u; D) N(v) # 0.

If D' is a superset of D, then 0 partition of D' defined in (P1). AD'

Observation 2 .

