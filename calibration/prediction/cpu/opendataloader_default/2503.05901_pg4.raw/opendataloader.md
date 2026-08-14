4 A.´ NAGY, M. OLAH,´ M. STOIKA, AND CS. VINCZE

but there are no equidistant points above the graph of the function f. Therefore it is impossible to ﬁnd diﬀerent equidistant points along a vertical line. In particular, by choosing y1 = G(x) < y = y2, Lemma 1 shows that

d((x, y2), L) − d((x, y1), L) < d((x, y2), (x, y1)) = y2 − y1 ⇒ d((x, y), L) < y = d((x, y), K)

because equality of type (2) must be avoided. We can ﬁnish the proof by choosing 0 < y1 = y < G(x) = y2 as follows:

d((x, y2), L) − d((x, y1), L) < d((x, y2), (x, y1)) = y2 − y1 ⇒

d((x, y), K) = y < d((x, y), L) and the inequality is automatically satisﬁed in case of y ≤ 0. Deﬁnition 1. A function G: Rn → R+ is an equidistant function if its graph is the equidistant set of K and L for a positive-valued continuous function f. Lemma 3. The equidistant function G: Rn → R+ belonging to a positive-valued continuous function f : Rn → R+ is continuous. Proof. Taking xn → x, the sequence yn = G(xn) is obviously bounded because of the continuity of the function f: for all but ﬁnitely many indices,

0 < yn = G(xn) < f(xn) < f(x) + ε. Therefore it has a convergent subsequence. Since the distance-measuring functions d((x, y), L) and d((x, y), K) are continuous, it can easily be seen that any convergent subsequence of yn gives a subsequence of (xn, yn) tending to a point (x, y) such that

d((x, y), L) = d((x, y), K). The unicity of the equidistant point at x implies that y = G(x) is the common limit of the convergent subsequences of yn = G(xn). Therefore yn = G(xn) → y = G(x).

Theorem 1. Let I be a ﬁnite nonempty index set and consider the family {fi | i ∈ I} of positivevalued continuous functions deﬁned on Rn with corresponding equidistant functions {Gi | i ∈ I}. If Gmin is the equidistant function belonging to the function

fmin: Rn → R, fmin(x) = min{fi(x) | i ∈ I}, then

Gmin(x) = min{Gi(x) | i ∈ I}

for any x ∈ Rn. Proof. Since all functions are positive-valued, we can use the epigraphs as focal sets in the sense of Remark 1. Let x ∈ Rn be an arbitrary point, Li := epi fi (i ∈ I) and suppose that

y > min{Gi(x) | i ∈ I}.

Then there exists at least one index i ∈ I such that y > Gi(x) and Lemma 2 implies that d((x, y), Li) < d((x, y), K). Since L := epi fmin = ∪i∈I epi fi = ∪i∈I Li, we have

d((x, y), L) = d((x, y), ∪i∈I Li) ≤ d((x, y), Li) < d((x, y), K) and Lemma 2 implies that y > Gmin(x). On the other hand, suppose that

y < min{Gi(x) | i ∈ I}.

Then y < Gi(x) for all i ∈ I and Lemma 2 implies that d((x, y), K) < d((x, y), Li) for all i ∈ I. Thus

d((x, y), K) < min {d((x, y), Li) | i ∈ I} = d((x, y), ∪i∈I Li) = d((x, y), L)

