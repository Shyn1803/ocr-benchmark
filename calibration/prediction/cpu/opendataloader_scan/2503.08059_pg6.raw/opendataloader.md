Error

![](<2503.08059_pg6_images/imageFile1.png>)

Ground Truth

Prediction

1e-3

Prediction

Ground Truth

Error

e-2

3

2

20

40

(e)

Training

(d)

Training

6e-3

Validation

Validation

80.6

20

Training

10

Validation

200

100

92e-3

Epoch

Euler  Dopris

0.3

10-5

50

100

750

200

50

100

150

200

50

00

Epoch

Figure 4: Predicting DR and KS systems using SNODEs. (a) and (b) show the testing examples for the DR and KS systems, respectively. Here, the training set features a spatial resolution of N x = 32 , whereas the test set has N x = 128 . (c), (d), and (e) respectively illustrate the variations in training and validation losses across three training stages.

We first consider the DR system. In practice, the source term may vary over time due to changes in environmental factors, yielding the following equation with a time-varying source term u ( x,t ) :

$$
St 1 €
$$

where D = 0 . 01 is the diffusion coefficient and K = 0 . 01 is the reaction rate. Here, we use u ( x,t ) = ( πx ) / 5 + u 1 ( t ) , where u 1 ( t ) is a sampling function from the GRF. In addition, we consider the KS equation, which exhibits complex chaotic dynamics, of the following form

$$
St = ~SSI Szz 1 €
$$

where u ( x,t ) = x/ 16 + u 2 ( t ) , and u 2 ( t ) is the sampling function from the GRF. After training, our SNODEs framework exhibits excellent modeling capabilities on the aforementioned PDE systems. Moreover, our framework can be naturally applied to the super-resolution learning by using higher-resolution spatiotemporal data as the test set. In the temporal dimension, our approach is capable of estimating the system state for any given future moment through the ODESolve process. In terms of spatial dimension, our method allows for training with lower resolution data ( N x = 32 ) and testing in higher resolution data ( N x = 128 ). The corresponding outcomes are presented in Figures 4(a)-(b). Here, we take the DR system as an example and provide

Here, we take the DR system as an example and provide the capture of critical components of unknown dynam ics is facilitated through flow matching pre-training, with the training error depicted in Figure 4(c), and we obtain Ê1 = 0. 00998rz + 0.9955u. Herein, the regularization parameter Q is set to 0.01, resulting in the training loss ex ceeding the validation loss. In stage 2, Ê1 was fine-tuned through the ODESolve prediction, with the corresponding prediction error illustrated in Figure 4(d), culminating in F1 the Euler' method for the initial 120 epochs; incorporating rapid progressively increasing prediction steps: Subsequently; for the remaining 80 epochs; the number of prediction steps is maintained at a constant 20, and we switch to the Dopris" method for further training. In stage 3, we maintain Ê1 fixed and employ GeNN for residual learning, where the opti mization objective is F Ê1 and the prediction error is presented in Figure 4(e) Herein, the training strategy remains consistent with that of stage 2. In fact, within the temporal domain of the DR experiment, the influence of Ks2 was not identified in stage 1. However; accurate predictions were achieved through the employment of simple substitute terms in stage 2 Then in the stage 3, the modeling accuracy was further enhanced through residual learning. spatial Finally, we consider 2-d NS system for viscous, incompressible fluid in vorticity form; which reads

![](<2503.08059_pg6_images/imageFile2.png>)

Initial value

t = 5

1

u3(t)

0.5

0.0

0.0

-0.5

2t3 4 5

Initial value

t = 20

t = 1

t = 2

t = 4

1.0

7

0.0

1

1.0

U3

0.0

10 15 20

X

Figure 5: Predicting NS systems using SNODEs. (a) The predicted result for training data with spatial resolution N x = N y = 16 . (b) The predicted result for testing data with spatial resolution N x = N y = 80 .

$$
St YaSy Ay (z,y) € [0,272, t € [0, 20],
$$

where γ represents the stream function, ∆ is the Laplacian operator, and ν = 0 . 001 . Additionally, u ( x,y,t ) = u 3 ( t ) ×{ 0 . 1sin[2 π ( x + y )]+cos[2 π ( x + y )] } is the forcing function, where u 3 ( t ) is a function obtained from a GRF. The system is defined over a square domain with dimensions [0 , 2] 2 , and the time interval is [0 , 20] . Under this condition, we can express the stream function as the vorticity, i.e., γ = − ∆ − 1 s . In the discrete scenario within the Fourier domain, this corresponds to ˜ γ = − 1 / ( k 2 + l 2 )˜ s . To facilitate the training, we augment the first layer of SymNet with i k / ( k 2 + l 2 )˜ s and i l / ( k 2 + l 2 )˜ s in the Fourier domain. Then after training, Figure 5 demonstrates that our framework achieves the accurate operator learning in modeling the underlying dynamics, enabling the precise and stable prediction of system evolutions, even the initial values and parameter functions outside the training set distribution. Additional training details and experimental results for the above parametric PDE systems are provided in Appendix B.4.

