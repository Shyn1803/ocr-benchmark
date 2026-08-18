Some key theoretical results behind the Gr¨bner walk are stated below. Detailed proofs and additional context may be found in Chapters 1 and 2 of [10].

Theorem 2. For an ideal I ◁ R , the following sets are in one-to-one correspondence:

$$
in< (I) , marked Grõbner bases full-dimensional is a term order of I cones of G(I)
$$

In our setting, a marked Gr¨bner basis is a reduced Gr¨bner basis with the leading terms identified (formally, each g is encoded as a pair ( g,x α ), where x α = in < ( g )). The first correspondence in Theorem 2 immediate, whilst the second correspondence is a consequence of [13, Theorem 1.11]: marked Gr¨bner bases encode the defining integer vectors of an H-description of the corresponding cone.

Lower-dimensional cones in G ( I ) correspond to generalized initial ideals in ω ( I ), where ω is any weight vector in the relative interior of said cone. Generically, such ideals are “almost monomial”, and may be retrieved with the help of the following lemma:

Lemma 3. Let G < be a marked Gro¨bner basis of I with regards to < and ω ∈ R n ≥ 0 be a weight vector on the boundary of the corresponding cone in G ( I ) . The set

$$
inw(G<) = {inw(g),9 € G<}
$$

At every step of the Gr¨bner walk, a basis of this form converted with Buchberger’s algorithm and then lifted to the basis of I corresponding to the adjacent full-dimensional cone, which corresponds to ( < t ) ω , i.e. the refinement of the target ordering < t by ω .

Lemma 4. Let M = { m 1 ,...,m r } be the marked Gro¨bner basis of in ω ( I ) with respect to the refinement ordering ( < t ) ω . Then

$$
mr mr
$$

is a Gr¨obner basis of I with respect to ( < t ) ω where f G < denotes the normal form of f with respect to the basis G < .

This process of subsequent passing to the generalized initial ideal and lifting to the adjacent basis is repeated until the target basis is computed.

# 3 FUNCTIONALITY

to load OSCAR . There is a straightforward interface through the function groebner_walk .

Example 5. Continuing from example Example 1, we can calculate ideal

$$
I= (y4 + 2} 2?
$$

with respect to < lex by starting from a Gr¨bner basis for the graded reverse lexicographic ordering < degrevlex . Since < degrevlex is the default internal ordering of any polynomial ring in OSCAR , it suffices to call the Gr¨bner walk in the following way.

