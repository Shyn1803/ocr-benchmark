Empirical Error Estimates for Graph Sparsiﬁcation

![](<2503.08031_pg36_images/imageFile1.png>)

Lemma G.5 (Huang et al. (2023), Proposition 9). Let X1,...,Xn be i.i.d. random vectors in Rp, and let h be a function h ∶ Rp × Rp → R satisfying E(h(X1,X2) X1) = 0. Suppose there is a sequence of functions φ1,...,φK ∶ Rp → R such that h can be represented as

K

φk(x)φk(x′)

h(x,x′)=

k=1

for all x,x′ ∈ Rp. Also, let φ(X1) = (φ1(X1),...,φK(X1)) and let Σ ∈ RK×K denote the covariance matrix of φ(X1). Lastly, let τ2 = var(h(X1,X2)), and let Z1,...,ZK denote independent standard normal random variables. Then,

h(Xi,Xj) τ2n(n − 1)

K

3 7

≤ t − P

1 τ λk(Σ)(Zk2 − 1)≤ t ≲ n−15 + n−141 1

τ h(X1,X2) L3

![](<2503.08031_pg36_images/imageFile2.png>)

P

sup

.

![](<2503.08031_pg36_images/imageFile3.png>)

![](<2503.08031_pg36_images/imageFile4.png>)

![](<2503.08031_pg36_images/imageFile5.png>)

![](<2503.08031_pg36_images/imageFile6.png>)

![](<2503.08031_pg36_images/imageFile7.png>)

![](<2503.08031_pg36_images/imageFile8.png>)

t∈R

1≤i≠j≤n

k=1

