economic examples. Also, I provide intuition regarding improvement of the identiﬁcation region via graphical illustrations.

# 3.1 Characterization

The following theorem is the main result of the paper.

Theorem 1 The sharp lower and upper bounds on the DTE under Pr((Y0,Y1) ∈ C) = 1 are characterized as follows: for any δ ∈ R,

F∆L (δ) ≤ F∆ (δ) ≤ F∆U (δ),

where

where

∞

F∆L (δ) = sup

{Ak}∞k=−∞

k=−∞

F∆U (δ) = 1 − sup

{Bk}∞k=−∞

max µ0 (Ak) − µ1 ACk ,0 , (11)

∞

max µ0 (Bk) − µ1 BkC ,0 ,

k=−∞

{Ak}∞k=−∞ and {Bk}∞k=−∞ are both monotonically decreasing sequences of open sets,

ACk =

{y1 ∈ R|∃y0 ∈ Ak s.t. y1 − y0 ≥ δ and (y0,y1) ∈ C} ∪{y1 ∈ R|∃y0 ∈ Ak+1 s.t. y1 − y0 < δ and (y0,y1) ∈ C},

BkC =

{y1 ∈ R|∃y0 ∈ Bk s.t. y1 − y0 ≤ δ and (y0,y1) ∈ C} ∪{y1 ∈ R|∃y0 ∈ Bk+1 s.t. y1 − y0 > δ and (y0,y1) ∈ C} for any integer k.

Proof. See Appendix A.

Theorem 1 is obtained by applying Kantorovich duality in Lemma 2 to the optimal transportation problems (9) and (10). Note that the sharpness of the bounds is also conﬁrmed by Lemma 2. Since characterization of the upper bound is similar to that of the lower bound, I maintain the focus of the discussion on the lower bound. The minimization problem (9) can be written in the dual formulation as follows: for λ = ∞,

inf

π∈Π(µ0,µ1)

= sup

(ϕ,ψ)∈Φc

{1{y1 − y0 < δ} + λ(1 − 1C (y0,y1))}dπ

ϕ(y0)dµ0 + ψ (y1)dµ1 ,

17

