between the approximated solution and the raw data, thereby enhancing the overall accuracy of the model.

ND

1 ND

LossD =

i=1

2

uNN(xiD,tiD) − uiData

(2.6)







2

uNN ( ,t) t

x





x



2

uNN

uNN (x,t)





t

f (x,t,uNN(x,t))







Loss

# update 



N

Loss 

Y Done

2 2



N i i NN R R i i i i i i PDE NN R R R R NN R R R i

( )

u t Loss a u t f t u t N t

1 ( , )

x

 

R

= −  −

2 2

( , ) , , ( , )

x x x



=

1

2

N

1

B

= −

Β x x

i i i i BC NN B B B B

- Loss u t g t N
- Loss u t h N


( , ) ( , )

=

B i N

1

2

1



I

= −

i IC NN I I I i

( , ) ( )

I x x

0 1

=

Loss = LossPDE + LossBC + LossIC

Figure 2: FPINN framework to solve wave propagation

3. Normalized Fourier induced PINN to solve the wave equation 3.1. The analysis of general PINN and FPINN method to the wave equation in two different scale range

Although various PINN models have been successfully applied to the study of ordinary and partial differential equations, particularly in the case of the wave equation, our investigation shows that their performance deteriorates in large scale domain and long time range, potentially leading to non-convergence.

For example, let us consider two scenarios for two-dimensional wave propagation equation with Dirichlet boundary in Ω1 = [0,2π] × [0,2π],t ∈ (0,2). Ω2 = [0,10π] × [0,10π],t ∈ (0,10), respectively. The governed equation is

∂2u ∂t2

∂2u ∂x21

∂2u ∂x22

- 1

- 2


+ 12t2 (3.1) An analytical solution is given by

=

+

u(x1,x2,t) = t4 + sin(x1) · sin(x2) · sin(t).

Since the boundary and initial constraint functions can be directly derived from the exact solution, we will not explicitly state them here.

In this experiment, the solvers for PINN and FPINN are configured as a DNN and a FFM-based DNN with N subnetworks, respectively, and the scale factors are set as (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), and each subnetwork is configured with sizes of (20, 15, 15, 10). The first hidden layer of all subnetworks employs Fourier feature mapping as the activation function (see Eq.(2.3)), while the activation functions for the other

layers (except for the output layer) are selected as GELU(x) = x· 21[1+erf(√x2)], where erf(x) is Gaussian error function, and the output layers of all subnetworks are linear. We train the previously mentioned PINN

and FPINN models for 30,000 epochs, performing testing every 1,000 epochs during the training process.

6

