![](<2503.08059_pg6_images/imageFile1.png>)

Figure 4: Predicting DR and KS systems using SNODEs. (a) and (b) show the testing examples for the DR and KS systems, respectively. Here, the training set features a spatial resolution of Nx = 32, whereas the test set has Nx = 128. (c), (d), and (e) respectively illustrate the variations in training and validation losses across three training stages.

We first consider the DR system. In practice, the source term may vary over time due to changes in environmental factors, yielding the following equation with a time-varying source term u(x,t):

st = Dsxx + Ks2 + u(x,t), x ∈ [0,1], t ∈ [0,1], (7) where D = 0.01 is the diffusion coefficient and K = 0.01 is the reaction rate. Here, we use u(x,t) = (πx)/5 + u1(t), where u1(t) is a sampling function from the GRF. In addition, we consider the KS equation, which exhibits complex chaotic dynamics, of the following form

st = −ssx − sxx − u(x,t)sxxxx, x ∈ [0,32π], t ∈ [0,20],

(8)

where u(x,t) = x/16 + u2(t), and u2(t) is the sampling function from the GRF. After training, our SNODEs framework exhibits excellent modeling capabilities on the aforementioned PDE systems. Moreover, our framework can be naturally applied to the super-resolution learning by using higher-resolution spatiotemporal data as the test set. In the temporal dimension, our approach is capable of estimating the system state for any given future moment through the ODESolve process. In terms of spatial dimension, our method allows for training with lower resolution data (Nx = 32) and testing in higher resolution data (Nx = 128). The corresponding outcomes are presented in Figures 4(a)-(b).

Here, we take the DR system as an example and provide the training details for our SNODEs framework. In stage 1, the rapid capture of critical components of unknown dynamics is facilitated through flow matching pre-training, with the training error depicted in Figure 4(c), and we obtain Fˆ1 = 0.0099sxx + 0.9955u. Herein, the regularization parameter α is set to 0.01, resulting in the training loss exceeding the validation loss. In stage 2, Fˆ1 was fine-tuned through the ODESolve prediction, with the corresponding prediction error illustrated in Figure 4(d), culminating in Fˆ1 = 0.0098sxx+u−0.0083s+0.0046. Herein, we employ the ”Euler” method for the initial 120 epochs, incorporating

![](<2503.08059_pg6_images/imageFile2.png>)

Figure 5: Predicting NS systems using SNODEs. (a) The predicted result for training data with spatial resolution Nx = Ny = 16. (b) The predicted result for testing data with spatial resolution Nx = Ny = 80.

progressively increasing prediction steps. Subsequently, for the remaining 80 epochs, the number of prediction steps is maintained at a constant 20, and we switch to the ”Dopri5” method for further training. In stage 3, we maintain Fˆ1 fixed and employ a GeNN for residual learning, where the optimization objective is F − Fˆ1 and the prediction error is presented in Figure 4(e). Herein, the training strategy remains consistent with that of stage 2. In fact, within the temporalspatial domain of the DR experiment, the influence of Ks2 on the dynamics is minimal. Consequently, this term was not identified in stage 1. However, accurate predictions were achieved through the employment of simple substitute terms in stage 2. Then in the stage 3, the modeling accuracy was further enhanced through residual learning.

Finally, we consider a 2-d NS system for a viscous, incompressible fluid in vorticity form, which reads

st = γxsy − γysx + ν∆s + u(x,y,t), ∆γ = −s, (x,y) ∈ [0,2]2, t ∈ [0,20],

(9)

where γ represents the stream function, ∆ is the Laplacian operator, and ν = 0.001. Additionally, u(x,y,t) = u3(t)×{0.1sin[2π(x+y)]+cos[2π(x+y)]} is the forcing function, where u3(t) is a function obtained from a GRF. The system is defined over a square domain with dimensions [0,2]2, and the time interval is [0,20]. Under this condition, we can express the stream function as the vorticity, i.e., γ = −∆−1s. In the discrete scenario within the Fourier domain, this corresponds to γ˜ = −1/(k2 + l2)˜s. To facilitate the training, we augment the first layer of SymNet with ik/(k2 +l2)˜s and il/(k2 +l2)˜s in the Fourier domain. Then after training, Figure 5 demonstrates that our framework achieves the accurate operator learning in modeling the underlying dynamics, enabling the precise and stable prediction of system evolutions, even the initial values and parameter functions outside the training set distribution. Additional training details and experimental results for the above parametric PDE systems are provided in Appendix B.4.

