With these lemmas at hand, we now prove our main theorem by an inductive argument. In particular, we show that the following two families of Gaussian processes, introduced in Section 4, remain non-degenerate throughout training:

{ZW0lδxls−1(ξi)}i∈[m],s∈[t],2≤l≤L, (C.1) { ZW0l⊤dhls(ξi)}i∈[m],s∈[t],2≤l≤L. (C.2)

Recall that a Gaussian process is non-degenerate if its covariance matrix C at any finite collection of points satisfies det(C) ̸= 0 (Adler and Taylor, 2009). Using the filtration framework introduced in Section 4, our proof follows the natural flow of computation in the network, proceeding layer by layer and separately handling forward and backward passes. We break this into four key steps, each building upon the results of previous steps:

- • Step 1: prove non-degeneracy for the features in the first hidden layer ZW02δx1s(ξi). This forms our base case as it only depends on the input data and network initialization, providing the foundation for our inductive argument.
- • Step 2: prove non-degeneracy for the features in remaining layers ZW0lδxls−1(ξi), 3 ≤ l ≤ L. This step leverages the non-degeneracy established in Step 1 and shows how it propagates through deeper layers of the network.
- • Step 3: prove non-degeneracy for the gradients in the last layer ZW0L⊤dhLs (ξi). Here we transition from analyzing forward features to backward gradients, showing how the established feature properties ensure meaningful gradient flow.
- • Step 4: prove non-degeneracy for the gradients in remaining layers ZW0l⊤dhls(ξi), 2 ≤ l ≤ L − 1. Finally, we complete our analysis by showing how gradient non-degeneracy propagates backward through the network, ensuring effective training dynamics at all layers.


The proof proceeds by induction on the time step t, where at each step we verify these properties hold across all layers. This structure allows us to carefully track how the non-degeneracy property is maintained as information flows both forward and backward through the network during training. This systematic proof structure allows us to establish the global property of non-degeneracy by carefully tracking local changes at each layer and time step. We now proceed with the detailed proof.

Proof of Theorem 4.5. Considering Trajectory Until Error Signals Vanish. Throughout this proof, we focus on the training trajectory up to the time when all error signals ˚χt,i become zero. This is because once the error signals vanish, there are no further parameter updates, and the training dynamics remain static thereafter. Our analysis ensures that up to this point, the Gaussian processes governing the feature and gradient updates remain non-degenerate, thereby maintaining the linear independence of features across all layers.

Connecting ZWδx to hl and xl. Recall from Section 3 that each pre-activation hl(ξ) and post-activation xl(ξ) can be decomposed into a primary Gaussian increment plus lower-order (history-dependent) terms in the infinite-width limit:

Because these additional terms do not alter the essential covariance structure when conditioned on past information (they vanish or become deterministic in the limit), the linear (in)dependence

19

