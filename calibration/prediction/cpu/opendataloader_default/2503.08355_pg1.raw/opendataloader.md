arXiv:2503.08355v1 [math.ST] 11 Mar 2025

Pointwise Minimax Vector Field Reconstruction from Noisy ODE

Hugo Henneuse 1,2

hugo.henneuse@universite-paris-saclay.fr March 12, 2025

Abstract

This work addresses the problem of estimating a vector ﬁeld from a noisy Ordinary Diﬀerential Equation (ODE) in a non-parametric regression setting with a random design for initial values. More speciﬁcally, given a vector ﬁeld f : RD → RD governing a dynamical system deﬁned by the autonomous ODE: y′ = f(y), we assume that the observations are y˜Xi(tj) = yXi(tj)+εi,j where yXi(tj) is the solution of the ODE at time tj with initial condition y(0) = Xi, Xi is sampled from a probability distribution µ, and εi,j some noise. In this context, we investigate, from a minimax perspective, the pointwise reconstruction of f within the envelope of trajectories originating from the support of µ. We propose an estimation strategy based on preliminary ﬂow reconstruction and techniques from derivative estimation in non-parametric regression. Under mild assumptions on f, we establish convergence rates that depend on the temporal resolution, the number of sampled initial values and the mass concentration of µ. Importantly, we show that these rates are minimax optimal. Furthermore, we discuss the implications of our results in a manifold learning setting, providing insights into how our approach can mitigate the curse of dimensionality.

# 1 Introduction

Longitudinal data commonly arise in the study of dynamical systems across various disciplines, from physics to biology and economics (see e.g. Hirsch et al., 2013). By observing multiple trajectories in a given space, we aim to extract key information about the underlying dynamics, such as governing laws, stability properties, or long-term trends. A common approach to modeling such phenomena is to assume that the observed trajectories follow an underlying diﬀerential system, which provides a structured framework for inference, prediction, and control.

However, real-world data are often subject to noise, missing observations, and irregular sampling, making their analysis particularly challenging and raising interesting statistical questions. In particular, given noisy observations of trajectories governed by an autonomous diﬀerential equation:

y′ = f(y), (1) where f : Rd → Rd is the vector ﬁeld governing the system, can we reconstruct f from the observed data ?

This question has recently garnered signiﬁcant interest among the machine learning and statistical communities. Most existing works focus on the case where f is assumed to belong to a parametric class of functions (e.g. see the surveys McGoﬀ et al., 2015; Ramsay and Hooker, 2017; Dattner, 2021). In contrast, the non-parametric literature is scarcer and primarily numerical (Chen et al., 2018; Heinonen et al., 2018; Bhat et al., 2020; Gottwald and Reich, 2021; Lahouel et al., 2024). More recently, some studies have provided theoretical analyses of the statistical performance of their proposed estimation strategies. Notably, Scho¨tz and Siebel (2024); Scho¨tz (2025) introduce two statistical models: the snake model and the stubble model. In the snake model, a few long trajectories are observed, covering the space of interest. In the stubble model, many short trajectories are observed, with initial values forming a deterministic and uniform cover of

![](<2503.08355_pg1_images/imageFile1.png>)

1Laboratoire de Math´ematiques d’Orsay, Universit´e Paris-Saclay, Orsay, France 2DataShape, Inria Saclay, Palaiseau, France

1

