in Figure 1a indicate the expectation a random vector will lie in the tangent space. The expectation is approximately √︀ 𝑛/𝑑 , where 𝑛 and 𝑑 are the dimensions of the tangent space approximation and manifold, respectively [ 9 ]. An explanation is therefore sufficiently aligned with the tangent space when that fraction in the tangent space is greater than √︀ 𝑛/𝑑 . We see in Figure 1a that standard base-point choices on CIFAR10 are significantly below the vertical line. It is the goal of future work to determine if the dimension of the tangent space of CIFAR10 of 𝑛 = 144 or the parameter of the Gaussian base-point impacts the tangential alignment of IG on CIFAR10.

We provide in Figure 2 , example integrated gradient explanations for a point on MNIST32, FER2013, and Fashion-MNIST with differing base-point choice. We see that our method provides tangentially aligned explanations with 𝜇 𝑥 > 0 . 91 for all datasets. The tangentially aligned integrated gradient attributions are clear and perceptually aligned with the object to classify in the image. We see in Figure 2 that uniform, maximum ℓ 2 distance, and Gaussian are consistently random noise.

# 4.5. Comparison of Gradient Explainability Models with Tangential Integrated Gradients

In this section we compare tangentially aligned integrated gradients with three common gradient explainability models: Gradient, Smooth Grad and Input *Gradient. The aforementioned gradient explainability models do not require a base-point choice. We demonstrate that tangentially aligned integrated gradients significantly improves upon integrated gradients. The gradient explainability models for a given model are defined as follows:

- 1. Gradient The gradient of a model 𝑓 at 𝑥 ∈ R 𝑑 for class 𝑖 is defined as:

$$
Mf(x) grad(x)i = (33)
$$

- 2. Smooth Grad We define Smooth Grad with 𝑛 samples and standard deviation 𝜎 as:


$$
SmoothGrad(z) = (34) i=1
$$

where, 𝑎 ∼ 𝒩 (0 ,𝜎 2 ) . Following [ 9 ] we take 𝜎 = 0 . 02 and 𝑛 = 25 .

3. Input*Gradient Input*Gradient is defined as:

$$
Input * Gradient = 2 (35)
$$

In Figure 1b we provide density plots of the fraction an attribution is in the tangent space for: Gradient, Smooth Grad, Input*Gradient and tangentially aligned integrated gradients. We see in Figure 1b that tangentially aligned integrated gradients provides attributions consistently in the tangent space, out-performing the aforementioned gradient explainability models. In Figures 1a and 1b Gradient, Smooth Grad and Input*Gradient provide better tangential alignment than the common base-point choices provided in Section 2.2 on MNIST and CIFAR10. On Fashion-MNIST we see that the zero base-point choice provides comparable performance with Gradient, Smooth Grad and Input*Gradient. In Figures 1a and 1b we see that on FER2013, Gradient, Smooth Grad and Input*Gradient perform similarly to Gaussian, maximum ℓ 2 distance and zero base-point choices for integrated gradients. All gradient models on FER2013 outperform the uniform base-point choice for integrated gradients. We see in Figures 1a and 1b , Gradient, Smooth Grad, and Input*Gradient tend to out-perform Integrated gradients with standard the standard base-point choices. Tangential integrated gradients out-performs the aforementioned gradient explainability models and standard base-point choices.

