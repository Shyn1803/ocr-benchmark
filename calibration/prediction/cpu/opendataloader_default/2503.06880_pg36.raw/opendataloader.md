35

Obviously W contains an open neighborhood of zero. Now let z “ prpf1q,rpf2q,¨¨¨ ,rpfnqq. By assumption and the fact that W is compact, z R W. Since W compact we can find a bounded linear functional that strictly separates W and z0. Namely we can find pλ1,λ2,¨¨¨ ,λnq P Cn such that:

ÿ

λirpfiq ą 1 and @px1,¨¨¨ ,xnq P W, ÿ iďn

λixi ď 1 Therefore ›ř

iďn

iďn λifi› ď 1 and hence:

1 ă r ˜

λifi¸

ÿ

ÿ

ď 1

ď }r}

λifi

›

›

iďn

iďn

# which is absurd. Hence for any tfiuiďn Ď X˚ and σ P p0,1q:

( or

( Ď p1 ` σq␣pf1pxq,¨¨¨ ,fnpxqq|x P Xď1

prpf1q,¨¨¨ ,rpfnqq P tpf1pxq,¨¨¨ ,fnpxqq|x P Xď1

prpf1q,¨¨¨ ,rpfnqq P ␣pf1pxq,¨¨¨ ,fnpxqq|x P Xď1`σ

(

□

Proposition 5.3. Any non-reflexive Banach space X will have a bounded bi-orthogonal system pei,fjqi,jPN such that supn }ř

iďn ei} ă 8 or supn }ř

iďn fi} ă 8 Proof. Let r P X˚˚zQpXq and suppose H is an arbitrary finite dimensional subspace of X. Define:

␣|rpyq| : y P X“˚1 X HK

(

ρ “ sup

# . Suppose H “ Spanth1,h2,¨¨¨ ,hnu and H˚ “ Spantf1,f2,¨¨¨ ,fnu where fiphjq “ 1 iff i “ j. If ρ “ 0, then r P pHKqK. Observe that QpHqK “ Q1pHKq and pHKqK Ď Q1pHKqK. Then r P “

QpHqK‰

K “ QpHq Ď QpXq, which is absurd. Hence ρ ą 0. Below we will start constructing the desired bi-orthogonal system.

Suppose }r} “ 1. Fix σ P p0,1q. y1 P X“˚1 so that β1 “ rpy1q ą 21. By Proposition 5.2 we can find b1 P Xď1`σ so that y1pb1q “ β1. Define E1 “ Spantb1u and:

␣

(

rpyq|y P X“˚1 X E1K

ρ1 “ sup

By the previous remark, we have ρ1 ą 0. Next find y2 P Xď˚1 X E1K so that β2 “ rpy2q ą 21ρ1. Again by Proposition 5.2, find b2 P Xď1`σ so that y1pb2q “ β1,y2pb2q “ β2. Define E2 “ Spantb1,b2u and:

␣

(

rpyq|y P X“˚1 X E2K

ρ2 “ sup

and similarly ρ2 ą 0. By induction for each n P N we will have tbiuiďn Ď Xď1`σ, En “ Spantbiuiďn, yi`1 P Xď˚1 X EiK, tβiuiďn and:

␣

(

rpyq|y P X“˚1 X EnK

ρn “ sup

, βn`1 “ rpyn`1q P ˆ

ρn,ρnȷ and for each i,j P t1,2,¨¨¨ ,nu:

- 1

- 2


- 1

- 2


such that β1 “ rpy1q ą

#rpyiq, 1 ď i ď j ď n 0, 1 ď j ă i ď n

yipbjq “

Since HnK is decreasing as n increases, we have tρnu is non-increasing sequence in p0,1s and hence convergent. Assume that infn ρn “ limn ρn “ 0. For each ϵ P p0,1q and then suppose ρn ă ϵ for all n ě N. Fix f P Xď˚1 and for each n P N, define τnpfq “ maxiďn |fpbiq| and:

fpb1qy1 ` ÿ

1 βi“

fpbiq ´ fpbi´1q‰

1 β1

znpfq “

yi Since for each n P N:

1ăiďn

- 1

- 2


0 ă

ρn`1 ă βn ď ρn

