In Section 2, we give motivation from non-linear stochastic ﬁltering, volatility modelling in ﬁnance, pathwise stochastic optimal control and mean-ﬁelds SDE with common noise system; topics also closely related to [11, 12]. We do not strive for precise statements, but try to explain how rough stochastic processes naturally emerge, together with motivation for what is to come: Section 3 deals with the mathematics of randomisation of rough Itoˆ processes, one obstacle being the potentially uncountable number of rough paths that ﬁgure as parameter in (1.1). The remaining section discuss applications to RSDE and then also mean-ﬁeld RSDEs. The body of work surrounding RSDEs, control and common noise also resonates with early remarks made by the authors of [10], conjecturing the use of rough paths for conditioned forward stochastic dynamics (in their context of mean ﬁeld games with common noise).

Acknowledgement : PKF and HZ acknowledge support from DFG CRC/TRR 388 “Rough Analysis, Stochastic Dynamics and Related Fields”, Projects A07, B04 and B05. Part of this work was carried out during a visit of the ﬁrst author to Shandong University. KL acknowledges supports from EPSRC [grant number EP/Y016955/1]. HZ is partially supported by the Fundamental Research Funds for the Central Universities, NSF of China and Shandong (Grant Numbers 12031009, ZR2023MA026), Young Research Project of Tai-Shan (No.tsqn202306054).

# 2 Motivating examples

# 2.1 Non-linear stochastic ﬁltering

We follow [16, 8]. One has an observation process Y t =   X is assumed to have “correlated” dynamics,

$$
dXt = = (2.1)
$$

Here, ( B,B ⊥ ) and ( B,Y ) are independent Brownians under some original measure P o and P , respectively, related by the Girsanov formula

$$
dPo exp ( h(s, Xs;Ys)dYs 2 Jh(s; Xs,Ys)l?ds =: exp(It) Ft
$$

  Formally at least, the conditional dynamics of X t given the observation { Y t : 0   t   T } should be captured by the solution X Y to a rough SDE of the form (1.5) 2

$$
dXY (2.2)
$$

together with the “rough stochastic” Girsanov exponent

$$

$$

Bearing exponential integrability, one deﬁnes a ﬂow of measures

2 Assuming regular t dependence in f .

$$
4) :=
$$

