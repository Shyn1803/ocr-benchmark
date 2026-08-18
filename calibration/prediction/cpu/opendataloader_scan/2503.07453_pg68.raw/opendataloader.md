# J Guarantee for UncertainStateAction

In this section, we present the main guarantee of UncertainStateAction ( Algorithm 6 ) as a standalone algorithm; see Lemma J.1 . Then, in Lemma J.2 , we provide its guarantee when used as a subroutine within MTSS ( Algorithm 4 ). For a discussion of the motivation for these results, we refer back to Section I.1.3 .

Lemma J.1. Consider a call to UncertainStateAction h ( C 0: h − 1 ,   π 1: h , Σ h ; a ,N, N ) ( Algorithm 6 ) for some given h, C 0: h − 1 ,   π 1: h , Σ h , a ∈ A , N , and N such that σ min (Σ h ) ≥ λ , for some λ ∈ (0 , 1) . Then, for any δ ′ ∈ (0 , 1) and ζ ∈ (0 , 1 / 2) , with probability at least 1 − δ ′ , the output (ˆ x h , ˆ a h ) of UncertainStateAction satisfies:

$$
4log 16HLCE @e max (90) he[H] N
$$

Furthermore; there exists € Ce, ae] 2 1 and Xh,span Xh,span log

$$
4log X6' Vxh € > 2 max (91) he[H] N Xh,span ;
$$

Proof of Lemma J.l. Fix &' TaIs} Further , for 0 € [0 . h Note that De(ze,ae) consists of N iid. pairs sampled from [(zh; = Freedman's inequality (Lemma C.2) and the union bound over Q € [0 . h is an event € of probability at least 1 ah )

$$
2 4 logl N N (x,a)eDe(ze,ae) 4 2 N + N (92) log
$$

where the last step follows by the facts that |F| Now . Therefore;

$$
max (x,a)eDe(ze,ae) max (x,a)eDe(xe,ae) < 2 (sv max < 2 (93)
$$

where the last inequality follows by the fact that

$$
max max
$$

