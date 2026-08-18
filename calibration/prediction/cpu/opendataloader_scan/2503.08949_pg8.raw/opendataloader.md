2. Shape of the Eigenfunction v s,E : To precisely understand how λ s,E varies in E , we must not only understand the operator F s,E but also the associated eigenfunction v s,E . This diﬀers from prior work, such as [Bap14], which circumvented the analysis of v s,E by instead estimating the action of F s,E on certain test vectors (which loses careful control on λ s,E for E ≈ E 0 ). We approximate the eigenfunction v s,E in Section 8, where we begin by deﬁning an explicit function ˜ u by

$$
(2-s) (1.10)
$$

for $ 2 Ct2 . This is the general behavior we expect for the eigenfunction v,E However, the precise ~ to as (t2 In K) ~1 , is not transparent to US So, instead of comparing v,E directly to ũ Specifically; as Lemma 8.5, we show that 1-1 t-2 Eũ.

$$
(1.11)
$$

where the constants c and C are uniform in K . While useful, this does not explain how v s,E varies with E and, indeed, we do not know how to do this.

We bypass this by making use of the identity

$$
In Xs,E lim (1.12) n=00
$$

The benefit of this representation is that it replaces v,E with the function ũ that is independent of E.

However , it comes at the expense of having to compute high powers of when applied to ũ. 3 Estimating Iterates of To deduce the monotonicity of we analyze the difference In In E1 (1.12). We have FsE FsE: using

$$
(1.13)
$$

We note the identity

where we deﬁne

$$
n =1 ~ = s,Ez s,E1 ` (1.14) j=0 Fn-j-1
$$

$$
t2 -s )u(z) Fs,E1
$$

When |r| 2 and y is close to 0 (which is where the above integral will mainly be supported) , acts as a negative operator for functions supported outside of [~Ct2 , Ct2]: Ct2

that F ◦ F j ˜ u ( x ) is negative for | x | ≥ Ct 2 and bound it away from zero. The contribution from | x | ≤ Ct 2 might be positive, so we also provide a bound on this quantity in the same Lemma 9.3, using (1.8). Throughout these analyses, we make repeated use of (1.11), to bound high powers of F s,E applied to ˜ u by a multiple of v s,E (on which F s,E acts diagonally). In Section 10, we use the estimates from Lemma 9.3 as inputs to show that the negative contri-

butions from the regime | x | ≥ Ct 2 outweigh the positive ones from when | x | ≤ Ct 2 . We therefore deduce that the F n − j − 1 s,E 2 ( F ◦ ) F j s,E 1 from (1.14) essentially act as nonpositive operators on ˜ u , when E 1 < E 2 are close to E 0 . Combining (1.13) and (1.14), we ﬁnd   F n s,E 2   1 −   F n s,E 1   1 ≤ 0. Then (1.12) shows that λ s,E is weakly decreasing near E 0 , which is stated as Lemma 10.2. This argument

