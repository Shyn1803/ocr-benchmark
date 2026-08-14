Information entropy of complex probability 9

![](<2503.03759_pg9_images/imageFile1.png>)

certain types of correlation that cannot be captured using real-valued probabilities alone.

Consider a complex random variable Z whose probability distribution is deﬁned over a discrete set of outcomes. The probability mass function P(z) is now complexvalued, meaning that P(z) ∈ C. This introduces a fundamental shift in how entropy is conceptualized, as the standard Shannon entropy is deﬁned solely for real, nonnegative probabilities. To extend this concept, a suitable framework must account for both the magnitude and phase of complex probabilities.

A plausible extension of Shannon entropy to complex probability distributions can be expressed as

H(Z) = E[I(Z)] =

z

P(z)I(z) = −

z

P(z)log P(z), (10)

where P(z) is complex. The challenge lies in the interpretation of the logarithm log P(z) for complex values, as the logarithm of a complex number is inherently multivalued. To resolve this, log P(z) is typically expressed in terms of its polar form

log P(z) = log |P(z)| + iθ(P(z)), (11)

where |P(z)| is the modulus (or absolute value) of P(z), and θ(P(z)) denotes the phase (or argument) of the complex probability. Here, log |P(z)| captures the traditional magnitude-based contribution to entropy, while iθ(P(z)) incorporates the phase information intrinsic to complex probabilities. Substituting the polar form of log P(z) into the expression for H(Z), we obtain the complex form of Shannon entropy:

H(Z) = −

= −

= −

z

z

z

P(z)log P(z)

P(z)(log |P(z)| + iθ(P(z)))

P(z)log |P(z)| − i

z

P(z)θ(P(z)). (12)

This formulation reveals two distinct components of the complex entropy. The ﬁrst component, − z P(z)log |P(z)|, resembles the standard Shannon entropy but now incorporates the magnitudes of the complex probabilities |P(z)|. This term quantiﬁes the uncertainty or information content in the distribution of probability magnitudes, maintaining a familiar structure while adapting to the complex domain. The second component, −i z P(z)θ(P(z)), introduces a phase-dependent contribution to the entropy, reﬂecting the coherence, interference, or relative phase relationships among the events. Unlike classical entropy, which focuses solely on magnitude, this phase term highlights the informational signiﬁcance of relative phases, an essential feature in systems with quantum mechanical or wave-like properties.

