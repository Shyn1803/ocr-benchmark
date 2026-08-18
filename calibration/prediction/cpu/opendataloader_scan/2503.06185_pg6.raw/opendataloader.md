which is derived from the following regularized least squares model

$$
RBB argmin
$$

where regularized parameter τ k ∈ [0 , ∞ ).

Property 1. @k BB2] it is monotonically increasing with respect to the parameter Tk and

Using a similar process, we obtain β RBB k as

$$
RBB Bk (29)
$$

Combining the rule of penalty parameter (19) with (28) and (29), we get the RBB step size penalty parameters in ADMM as

$$
RBB RBB Pk = 1/vak (30) BRBB_
$$

In the spectral gradient step size methods, alternating strategy between long and short step sizes can improve the performance of algorithm. By adaptively adjusting the parameter τ k , RBB method can be viewed as a continuous alternating step size method. One of its advantages is that if the regularization parameter is appropriately selected according to the nature of problem, then RBB generates reasonable step sizes, avoiding manual setting of alternating thresholds. Based on the analysis in the preceding section, the penalty parameter selection problem in ADMM is now transformed to the regularization parameter τ k selection problem in RBB.

We now consider how to select appropriate parameter τ k in the RBB step sizes (28) and (29). The RB strategy (12) is an eﬀective method for adjusting the penalty parameter, which describes the convergence properties of ADMM [22]. Combined with the spectral penalty parameter scheme (30), the RB strategy inspires us that if   r k   2 >   d k   2 , then in the next iteration, a small spectral gradient step size is reasonable (corresponding to a large regularization parameter τ k +1 ); otherwise, a large spectral gradient step size (corresponding to a small regularization parameter τ k +1 ) is selected when   r k   2 <   d k   2 . Based on these analyses, a natural conclusion is that the size of regularization parameter should be proportional to the ratio of   r k   2 and   d k   2 . Therefore, we obtain the regularization parameter as follows

$$
(+k)" (31) Tk+1
$$

where q > 0 is a constant that acts as a scaling factor.

Remark 1 . Similar to the procedure in [26], scaling covariant and translation invariant.

# 3.2 Selecting regularization parameter of regularized MV model

In this subsection, we ﬁrst give the initial regularization parameter λ 0 based on the sample size and the number of assets, and then consider adaptively adjusting the regularization parameters based on the ﬁnancial goal: controlling the number of short sales. For analysis, the ℓ regularized model (3) can be rewritten as

regularized model (3) can be rewritten as

$$
min 2 llelm 1 1, (32) Tln ERn
$$

where matrix R m × n is the historical returns of asset i on its i -th column over m observation periods, see [7]. The observation data contained in this matrix is used to estimate two important parameters in MV model: expected return and covariance matrix. If the number of the chosen observations m is small compared to the number of assets, then the sample covariance matrix becomes ill-conditioned, one suﬀers from the over-ﬁtting problem [12, 3]. In this case, a high regularization promotes the sparsity of the solutions and mitigates over-ﬁtting. On the other hand, if the number of samples is large enough, then the model obtained is truth and a small amount of regularization is reasonable. Based on these, we regard 1 m as a factor of the initial regularization parameter λ 0 . The second factor that aﬀects regularization is the number of assets n . For any x = 0, the following

The second factor that affects regularization is the number of assets 1 . following inequalities hold

$$
Ilzllz 1.
$$

