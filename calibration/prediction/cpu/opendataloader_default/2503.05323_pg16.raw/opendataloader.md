VARMA WALDSPURGER MASSOULIE´

# Appendix A. Proof of Claim 6

Fix ǫ˜ > 0 and note that for any i = j ∈ [n], we have

1 (|λj − λi| + n−1.5−ǫ˜)2

E

![](<2503.05323_pg16_images/imageFile1.png>)

∞

1 (|λj − λi| + n−1.5−ǫ˜)2

=

> x dx

P

![](<2503.05323_pg16_images/imageFile2.png>)

0

∞

1 √x − n−1.5−ǫ˜ dx

P |λj − λi| <

=

![](<2503.05323_pg16_images/imageFile3.png>)

![](<2503.05323_pg16_images/imageFile4.png>)

0

n3+2˜ǫ

∞

1 √x − n−1.5−ǫ˜ dx +

1

√x − n−1.5−ǫ˜ dx ≤

=

P |λj − λi| <

P |λj − λi| <

![](<2503.05323_pg16_images/imageFile5.png>)

![](<2503.05323_pg16_images/imageFile6.png>)

![](<2503.05323_pg16_images/imageFile7.png>)

![](<2503.05323_pg16_images/imageFile8.png>)

n3+2˜ǫ

0

n3+2˜ǫ

1 √x

dx ≤ 2c0n2.5+˜ǫ,

P |λj − λi| <

![](<2503.05323_pg16_images/imageFile9.png>)

![](<2503.05323_pg16_images/imageFile10.png>)

0

where the last inequality holds by (Nguyen et al., 2017, Corollary 2.2) for some constant c0 > 0. Using the above inequality, we get

  ≤ 8c0n3.5+˜ǫ.

E 

1 (|λj − λi| + n−1.5−ǫ˜)2

![](<2503.05323_pg16_images/imageFile11.png>)



i =j∈[n]:|i−j|≤2

Now, by the Markov’s inequality, with probability 1 − n−ǫ˜, we get

1 (|λj − λi| + n−1.5−ǫ˜)2 ≤ 8c0n3.5+2˜ǫ.

![](<2503.05323_pg16_images/imageFile12.png>)

i =j∈[n]:|i−j|≤2

As mini∈[n−1] |λi+1 − λi| ≥ n−1.5−ǫ˜ with probability 1 − o(1) by (Feng et al., 2019, Corollary 1), we get

1 (λj − λi)2 ≤

4 (|λj − λi| + n−1.5−ǫ˜)2 ≤ 32c0n3.5+2˜ǫ. (9)

![](<2503.05323_pg16_images/imageFile13.png>)

![](<2503.05323_pg16_images/imageFile14.png>)

i =j∈[n]:|i−j|≤2

i =j∈[n]:|i−j|≤2

Now, we focus on bounding the terms for which |i − j| ≥ 3. By (Nguyen et al., 2017, Corollary 2.5) and union bound, we have mini∈[n−3] |λi+3 − λi| ≤ n−6/5−ǫ/˜ 5 with probability 1 − c0n−ǫ˜ for some c0 > 0. Using this bound, we get

−2

|j − i| 3

1 mini∈[n−3](λi+3 − λi)2

1 (λi − λj)2 ≤

![](<2503.05323_pg16_images/imageFile15.png>)

![](<2503.05323_pg16_images/imageFile16.png>)

![](<2503.05323_pg16_images/imageFile17.png>)

i,j∈[n]:|i−j|≥3

i,j∈[n]:|i−j|≥3

n

1 i2 ≤ π2n17/5+2˜ǫ/5.

≤ 6n17/5+2˜ǫ/5

![](<2503.05323_pg16_images/imageFile18.png>)

i=1

Now, combining the above inequality with (9), we get with probability 1 − o(1)

1 (λj − λi)2 ≤ 32c0n3.5+2˜ǫ + π2n17/5+2˜ǫ/5 ≤ n3.5+3˜ǫ,

![](<2503.05323_pg16_images/imageFile19.png>)

i,j∈[n]:i =j

where the last inequality holds for n large enough. Picking ˜ǫ = ǫ/6 completes the proof.

16

