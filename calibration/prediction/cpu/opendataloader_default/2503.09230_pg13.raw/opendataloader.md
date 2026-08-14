agrees with G in the neighborhood of Π if H ∩ Π = G ∩ Π and for each face f of H, there exists a corresponding face φ(f) of G incident to exactly the same vertices of G ∩ Π.

We point out that we can take φ(f) = f in case f is contained in Π, since we assume that the embeddings of H and G coincide within Π. The nontrivial case arises when f is not contained in Π.

Lemma 13. Let G be a 3-connected graph embedded in a fixed surface Σ with fw(G) ⩾ 3 and let (Π,Π+) be a pair of nested surfaces with boundary contained in Σ and contoured by G. Then there exists a 3-connected surface minor H of G ∩ Π+ that agrees with G in the neighborhood of Π.

Proof. We define H as the surface minor of G ∩ Π+ obtained by contracting each component of (G ∩ Π+) − V (G ∩ Π) into a single vertex. We obtain an embedding of H in Π+ by modifying the canonical embedding of G ∩ Π+ in this surface. Specifically, we continuously contract the components of (G ∩ Π+) − V (G ∩ Π) and their enclosed faces into single points. This contraction step can be modeled by a continuous map σ : Π+ → Π+, in such a way that the embedding of H is the image under σ of the embedding of G ∩ Π+. We choose σ to be injective outside of the components of (G ∩ Π+) − V (G ∩ Π), and the identity within Π. This can be done without loss of generality.

Figure 7: A graph G ∩ Π+ restricted to some disk ∆ = ∆i which is a component of Π+ − int(Π) (left), and the corresponding minor H restricted to the same disk (right). The two larger vertices of H correspond to component vertices. The green and the blue cycle are cuffs (that is, boundary components) of Π and Π+ respectively. The figure shows, for each i ∈ [3], a face fi of H contained in ∆ along with and the corresponding face φ(fi) = σ−1(fi) of G.

We first argue that H agrees with G in the neighborhood of Π. Since σ is the identity within Π, we see immediately that H ∩ Π = G ∩ Π. Now consider some face f of H. We let φ(f) := σ−1(f) denote the corresponding face of G. We proceed to check that this is indeed a face of G, which is moreover incident to the same vertices of G ∩ Π as f.

If f is contained in Π, then we have σ−1(f) = f and there is nothing to check.

Therefore, we may assume that f is contained in Π+ − Π. We observe that σ−1(f) is a face of G since we obtained H from G ∩ Π+ only by contracting edges. No edge or vertex was deleted. Because σ is the identity within Π, hence in particular on the boundary of Π, we see that σ−1(f) is incident to exactly the same vertices of G ∩ Π as f.

13

