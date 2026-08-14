A PREPRINT

![](<2503.09086_pg5_images/imageFile1.png>)

is employed to construct the following practical loss function to train the neural network solution U(x;θ), JR,M(θ) :=

- 1

![](<2503.09086_pg5_images/imageFile2.png>)

- 2


wB |X(∂Ω)|

wI |X(Ω)|

(U(x;θ) − g(x))2. (2.7)

|∇U(x;θ)|2 − f(x)U(x;θ) +

![](<2503.09086_pg5_images/imageFile3.png>)

![](<2503.09086_pg5_images/imageFile4.png>)

x∈X(Ω)

x∈X(∂Ω)

Here, again, the boundary condition is enforced with the L2-integral of the error, U(x;θ) − g(x), and the integrals of the energy term and the boundary condition term are approximated by the Monte–Carlo method; the weight factors wI and wB are analogous to those in the PINN loss.

The integral form of the deep Ritz loss function, before approximation via numerical integration, reads JR(θ) := wI

- 1

![](<2503.09086_pg5_images/imageFile5.png>)

- 2


|∇U(x;θ)|2 − f(x)U(x;θ) dx + wB

(U(x;θ) − g(x))2 ds(x). (2.8) The subscript R indicates that the loss is formed by the deep Ritz formulation. In addition, the subscript M in the loss JR,M(θ) in Eq. (2.7) means that the integral in the deep Ritz loss JR(θ) in Eq. (2.8) is approximated by the Monte–Carlo method.

∂Ω

Ω

When the boundary condition is implemented as hard constraints using ansatz functions, that is, using the neural network function U(x;θ) in Eq. (2.6), we obtain the integral loss function

- 1

![](<2503.09086_pg5_images/imageFile6.png>)

- 2


|∇ U(x;θ)|2 − f(x) U(x;θ) dx and train the neural network U(x;θ) for the loss JR

(θ) :=

JR

I

Ω

I,M(θ) by approximating the integral in JR

using the Monte– Carlo method.

I

It has been numerically studied that for the Poisson model problem, the trained solution U(x;θP) with the PINN loss JP,M(θ) gives better training results than the trained solution U(x;θR) with the deep Ritz loss JR,M(θ); see [40]. In our work, we will reinvestigate the performance of the two approaches for various hyper parameter settings and report some of our new ﬁndings.

As an enhancement to soft enforcement of boundary conditions, an augmented Lagrangian term can be included to the loss function [42] to obtain,

1 X(∂Ω)

(U(x;θ) − g(x))λ(x)

LP,M(θ,λ) := JP,M(θ) +

![](<2503.09086_pg5_images/imageFile7.png>)

x∈X(∂Ω)

and

1 X(∂Ω)

LR,M(θ,λ) := JR,M(θ) +

(U(x;θ) − g(x))λ(x),

![](<2503.09086_pg5_images/imageFile8.png>)

x∈X(∂Ω)

for the PINN and deep Ritz loss functions, respectively. Here, the boundary condition is enforced as constraints on the neural network solution U(x;θ) by introducing Lagrange multipliers λ(x) for each collocation point x in the training sampling set X(∂Ω). Hence, λ(x) are additional parameters that have to be trained, in addition to θ. The use of such an augmented Lagrangian term can improve slow training progress for the boundary loss term and can provide a more accurate trained neural network solution, U(x;θ). In the augmented Lagrangian approach, the parameters θ and λ are then optimized for the PINN and deep Ritz loss functions in the following sense:

(θP,λP) := arg max

min

LP,M(θ,λ) resp. (θR,λR) := arg max

min

LR,M(θ,λ) .

λ

θ

λ

θ

We note that the above optimization problems for θ are non-linear and non-convex while those for λ are linear. We thus use the Adam optimization method [20] in the gradient update for θ with a small learning rate ǫ and a simple gradient update for λ with a learning rate α, i.e.,

λ = λ + α∇λLP,M or λ = λ + α∇λLR,M. The learning rate α is often set to a larger value than the learning rate ǫ, as proposed in two-scale update schemes for min-max optimization problems; see [14, 25, 7]. In our numerical experiments, we set ǫ = 0.001 for the Adam optimizer and α = 1 for the gradient ascent update.

We note that the augmented Lagrangian method can be considered as a loss balancing scheme, and in our numerical experiments, we will also conduct comparisons on various loss balancing schemes as listed in Table 1.

5

