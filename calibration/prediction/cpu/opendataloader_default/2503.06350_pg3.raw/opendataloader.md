If f : [0,∞) −→ R is l`dla`g, we will denote by f− the left limit of f (with the convention that f0− = f0), and by f+ the right limit of f. The left jump of f is denoted by ∆f = f −f−. For later use, we will state Froda’s theorem (in a slightly more general form, applying to ﬁnite variation functions of time).

Lemma 1. Suppose f has locally ﬁnite variation. Then f is l`adl`ag and

{t ∈ [0,∞) : f is discontinuous at t} = {f = f−} ∪ {f = f+}. Furthermore, the above sets are all at most countable.

3. Main results The main theorem of this article, Theorem 1, can be stated as follows.

Theorem 1. Let (Xn)∞n=1 be a sequence of semimartingales such that, for each t ≥ 0, the set

t

ξdXn : n ∈ N,ξ is predictable and |ξ| ≤ 1

co

0

is bounded in probability, and (X0n)∞n=1 is bounded. Then there exists Xn ∈ co{Xm : m ≥ n} and a semimartingale X such that X = lims↓·,s∈Q+ limn→∞ Xsn and

lim

P − lim

n→∞

s↓·,s∈Q+

s

Y d Xn =

0

·

0

Y d X

for each continuous semimartingale Y .

The continuity condition on Y situates Theorem 1 as a stochastic counterpart to the following well-known version of Prokhorov’s theorem: if (gn)∞n=1 is a sequence of ﬁnite variation functions on [0,1] with supn supt∈[0,1] var(gn)t ≤ 1, there exists a sub-

sequence (nk)∞k=1 and a ﬁnite variation g such that limk→∞ 0 1 fdgnk = 0 1 fdg for all continuous f. In Section 5, we show the continuity condition in Theorem 1 cannot be

weakened—mirroring the deterministic case.

The imposition of a boundedness condition on Theorem 1 is natural, and not a signiﬁcant restriction. Indeed, the boundedness conditions assumed in the literature are often stronger (see, for example, [KP91; DS99]). Furthermore, since the boundedness condition from Theorem 1 is based on boundedness in probability, Theorem 1 is not chained to any particular choice of measure, an important property when working with multiple equivalent probability measures.

Let us note the following corollary of Theorem 1 for H1-bounded sequences of martingales. Corollary 1. Let (Mn)∞n=1 be a sequence of martingales such that

(Mn)∗t dP < ∞

sup

n Ω

3

