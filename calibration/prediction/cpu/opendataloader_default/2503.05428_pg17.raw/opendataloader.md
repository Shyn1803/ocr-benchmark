To complete the proof, our method will be to introduce a certain system of PDEs, then show that this system satisﬁes the Lopatinskii conditions [1], see also [44, Chapter 5, Proposition 11.9], if and only if λ is in the complement of the right side of (49). When the Lopatinskii conditions are satisﬁed, the system is a Fredholm operator which implies M(λ) is also Fredholm. Therefore, in this case λ ∈ σess(L)c which will establish the right inclusion of (49). The Lopatinskii conditions fail if either the system is not elliptic in the interior, or at the boundary. As we will see, interior ellipticity of the system is equivalent to

 

 

c

λ ∈

σpt(x,ξ)

. (53)

(x,ξ)∈M×R3\{0}

We have already shown that failure of this condition leads to existence of a Weyl sequence. Assuming interior ellipticity, we will show that boundary ellipticity is equivalent to

λ ∈

![](<2503.05428_pg17_images/imageFile1.png>)

![](<2503.05428_pg17_images/imageFile2.png>)

i|Pn − max(0,N2), max(0,N2)

x∈∂M

c

We will show that failure of this condition also leads to existence of a Weyl sequence, which will complete the proof. Let us begin now deriving the PDE system.

For any v ∈ H let us consider the decomposition given by Lemma 2, which can be written as v = w + T∗ϕ

where w ∈ Ker(T) and ϕ ∈ H1(M). Let us further decompose w according the standard Helmholtz decomposition as

w = ∇ × (ρ0wv) + ∇ϕv where ϕv ∈ H1(M) and the vector potential ρ0wv is in the space

HCurl,0(M) = {u ∈ L2(ρ0 dx) : ∇ × u ∈ L2(ρ0 dx), n × u|∂M = 0}, while also satisfying

∇ · (ρ0wv) = 0.

Given that M is a ball, a unique such decomposition exists (see [2, Section 3]). Let us set ρ0zv = ∇ϕv which must then satisfy

∇ × (ρ0zv) = 0. Then w ∈ Ker(T) is equivalent to

ρ0g0′

g0′ c2 · ∇ × (ρ0wv) +

c2 · zv = 0, n · zv|∂M = 0. Now, suppose that u ∈ Ker(T) satisﬁes

∇ · (ρ0zv) +

![](<2503.05428_pg17_images/imageFile3.png>)

![](<2503.05428_pg17_images/imageFile4.png>)

M(λ)u = f. (54) As described above for v, there will be wu and zu such that

u = ∇ × (ρ0wu) + ρ0zu where

∇ × (ρ0zu) = 0, (55) ∇ · (ρ0wu) = 0, (56)

ρ0g0′

g0′ c2 · ∇ × (ρ0wu) +

c2 · zu = 0, (57) n · zu|∂M = 0, (58) n × wu|∂M = 0. (59)

∇ · (ρ0zu) +

![](<2503.05428_pg17_images/imageFile5.png>)

![](<2503.05428_pg17_images/imageFile6.png>)

17

