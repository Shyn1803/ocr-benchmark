Benjamin Colmey and Richard Lascar 11

with

ρ(y, x, η′) = ϕ(y, η′) − ϕ(x, η′) − (y − x)ϕx(x, η′), ρ vanishes at order ≥ 2 in y = x. For checking (3.10), we see

- (3.11) Q(aei

ϕ

![](<2503.04189_pg11_images/imageFile1.png>)

h) = ei

1

![](<2503.04189_pg11_images/imageFile2.png>)

h((x′−y′)θ′+ϕ(y,η′)) q(x, θ′) (2πh)n−1

![](<2503.04189_pg11_images/imageFile3.png>)

a(y, η′) dy′dθ′.

a having compact support and ϕ being a symbol, one has |ϕ′y| ≤ C′ on supp(qa), so for |θ′| ≥ C > 0, large, the phase of (3.11) H = (x′ − y′)θ′ + ϕ(y, η′) satisﬁes

|Hy′′| ≥ c(1 + |θ′|), for |θ′| ≥ C > 0, large

and if we split the integrand of (3.11) in qa = χ(θ′)qa+(1−χ(θ′))qa, we integrate the second term by parts and obtain

- (3.12) Q(aei

ϕ

![](<2503.04189_pg11_images/imageFile4.png>)

h) = Q′ϕ(a)ei

ϕ

![](<2503.04189_pg11_images/imageFile5.png>)

h + R(a),

where Q′ϕ is a Gs symbol of order Ssm,k+1 having the expansion (3.10) by the stationary phase lemma as R(a) is an Os(h∞) remainder. It is easy to see in view of these arguments that a1 ∈ Ssm−1,k. Moreover, it is to be observed that the above expansion is only a formal Gevrey 2s − 1 symbol.

The microlocal invertibility of FIO reduces to the PDO case. We refer to [5] for a proof of the Gevrey elliptic result in classes Ssm.

For proving Theorem 2, we rewrite (3.8) in the form (hDx

1

+ Q(x, hDx; h))Fu = F(hDx

1

+ Q′)u,

close to (x0, ξ0; x0, ξ0) for some PDO Q′(x, hDx; h) of bi-order (−1, 0) in using a left microlocal inverse of F close to (x0, ξ0′). Indeed, we compute FF∗ and F∗F, and one has writing y = (x1, y′).

One has, following Eskin [8], FF∗u(x, h) =

1 (2πh)n−1

![](<2503.04189_pg11_images/imageFile6.png>)

e

i

![](<2503.04189_pg11_images/imageFile7.png>)

h(ϕ(x,ξ′)−ϕ(y,ξ′))a(x, ξ′)a(y, ξ′)u(x1, y′) dy′ dξ′,

![](<2503.04189_pg11_images/imageFile8.png>)

ϕ(x, ξ′) having been obtained in (3.6). We split the integral above into two terms. The ﬁrst is a h-PDO, the second is a smoothing operator. First, we note that the map:

(x, y′, ξ′) → (x, y′, Σ(x, y′, ξ′)), with

- (3.13) Σ(x, y′, ξ′) =

1

0

ϕ′x′(x1, y′ + t(x′ − y′), ξ′) dt

is a Gs-diﬀeo in a neighbourhood of (x0, y0′, η0′) with |x1| ≤ δ, |x′ − y′| ≤ δ, 0 < δ small,

close to the identity. Let (x, y′, η′) → (x, y′, Σ−1(x, y′, η′)) be an inverse map. One has obviously ϕ(x, ξ′) − ϕ(y, ξ′) = Σ(x, y′, ξ′)(x′ − y′), and

- (3.14) FF∗u(x, h) = K1u(x, h) + K2u(x, h),


