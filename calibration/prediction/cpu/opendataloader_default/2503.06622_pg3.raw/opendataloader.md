In Section 2, we give motivation from non-linear stochastic ﬁltering, volatility modelling in ﬁnance, pathwise stochastic optimal control and mean-ﬁelds SDE with common noise system; topics also closely related to [11, 12]. We do not strive for precise statements, but try to explain how rough stochastic processes naturally emerge, together with motivation for what is to come: Section 3 deals with the mathematics of randomisation of rough Itoˆ processes, one obstacle being the potentially uncountable number of rough paths that ﬁgure as parameter in (1.1). The remaining section discuss applications to RSDE and then also mean-ﬁeld RSDEs. The body of work surrounding RSDEs, control and common noise also resonates with early remarks made by the authors of [10], conjecturing the use of rough paths for conditioned forward stochastic dynamics (in their context of mean ﬁeld games with common noise).

Acknowledgement: PKF and HZ acknowledge support from DFG CRC/TRR 388 “Rough Analysis, Stochastic Dynamics and Related Fields”, Projects A07, B04 and B05. Part of this work was carried out during a visit of the ﬁrst author to Shandong University. KL acknowledges supports from EPSRC [grant number EP/Y016955/1]. HZ is partially supported by the Fundamental Research Funds for the Central Universities, NSF of China and Shandong (Grant Numbers 12031009, ZR2023MA026), Young Research Project of Tai-Shan (No.tsqn202306054).

# 2 Motivating examples

2.1 Non-linear stochastic ﬁltering

We follow [16, 8]. One has an observation process Yt = 0 t h(Xs,Ys)ds+Bt⊥ where the signal process X is assumed to have “correlated” dynamics,

dXt = ˜b(t,Xt,Yt)dt + σ(t,Xt,Yt)dBt(ω) + f(t,Xt,Yt)dBt⊥(ω)

= b(t,Xt,Yt)dt + σ(t,Xt,Yt)dBt(ω) + f(t,Xt,Yt)dYt(ω). (2.1)

Here, (B,B⊥) and (B,Y ) are independent Brownians under some original measure Po and P, respectively, related by the Girsanov formula

dPo dP F

![](<2503.06622_pg3_images/imageFile1.png>)

t

= exp

t

- 1

![](<2503.06622_pg3_images/imageFile2.png>)

- 2


h(s,Xs,Ys)dYs −

0

t

|h(s,Xs,Ys)|2ds =: exp(It).

0

Formally at least, the conditional dynamics of Xt given the observation {Yt : 0 t T} should be captured by the solution XY to a rough SDE of the form (1.5)2

dXtY = b(t,XtY,Yt)dt + σ(t,XtY,Yt)dBt(ω) + (f,Dyf)(t,XtY,Yt)dYt, (2.2) together with the “rough stochastic” Girsanov exponent

ItY =

t

- 1

![](<2503.06622_pg3_images/imageFile3.png>)

- 2


(h,(Dxhf + Dyh))(s,XsY,Ys)dYs −

0

0

Bearing exponential integrability, one deﬁnes a ﬂow of measures µYt ,ϕ := E[ϕ(XtY)exp(ItY)],

![](<2503.06622_pg3_images/imageFile4.png>)

2Assuming regular t dependence in f.

t

|h(s,XsY,Ys)|2ds.

3

