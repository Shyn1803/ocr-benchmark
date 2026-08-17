between the approximated solution and the raw data, thereby enhancing the overall accuracy of the model.

$$
ND LossD (2.6) ND i=l u Data
$$

![](<2503.05716_pg6_images/imageFile1.png>)

(x,t)

Loss PDE

1,

(x,t)

Au nn

Loss B€

f (x,t,unv (x,t))

Iunn

IC Loss =

Loss 

N

update

Loss 

Loss =

Loss PDE

Loss Bc + Lossic

Done

Figure 2: FPINN framework to solve wave propagation

# 3. Normalized Fourier induced PINN to solve the wave equation

3.1. The analysis of general PINN and FPINN method to the wave equation in two different scale range

Although various PINN models have been successfully applied to the study of ordinary and partial differential equations, particularly in the case of the wave equation, our investigation shows that their performance deteriorates in large scale domain and long time range, potentially leading to non-convergence. For example, let us consider two scenarios for two-dimensional wave propagation equation with Dirichlet

For example; let us consider two scenarios for two-dimensional wave propagation equation with Dirichlet = The governed equation is

$$
02u 92u 92u 4 12t2 (3.1) 2
$$

An analytical solution is given by

$$

$$

Since the boundary and initial constraint functions can be directly derived from the exact solution, we will not explicitly state them here.

In this experiment, the solvers for PINN and FPINN are configured as a DNN and a FFM-based DNN with N subnetworks, respectively, and the scale factors are set as (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), and each subnetwork is configured with sizes of (20, 15, 15, 10). The first hidden layer of all subnetworks employs Fourier feature mapping as the activation function (see Eq.( 2.3 )), while the activation functions for the other layers (except for the output layer) are selected as GELU( x ) = x · 1 2 [1+ erf ( x √ 2 )], where erf ( x ) is Gaussian error function, and the output layers of all subnetworks are linear. We train the previously mentioned PINN and FPINN models for 30,000 epochs, performing testing every 1,000 epochs during the training process.

