is employed to construct the following practical loss function to train the neural network solution U ( x ; θ ) ,

$$
WI WB JR,M(0) = (U(x;0) = g(x) )? . (2.7)
$$

the energy term and the boundary condition term are approximated by the Monte–Carlo method; the weight factors w I and w B are analogous to those in the PINN loss.

The integral form of the deep Ritz loss function, before approximation via numerical integration, reads

$$
JR(0) :=WI = f(x)U(x; 0) dx + WB (U(x;0) ds(x) . (2.8) ~g(x))?
$$

Ω ∂ Ω The subscript R indicates that the loss is formed by the deep Ritz formulation. In addition, the subscript M in the loss J R,M ( θ ) in Eq. (2.7) means that the integral in the deep Ritz loss J R ( θ ) in Eq. (2.8) is approximated by the Monte–Carlo method.

When the boundary condition is implemented as hard constraints using ansatz functions, that is, using the neural network function   U ( x ; θ ) in Eq. (2.6), we obtain the integral loss function

$$
(0) := = f(x)Ũ(x;0) dx
$$

using the Monte Carlo method.

It has been numerically studied that for the Poisson model problem, the trained solution U ( x ; θ P ) with the PINN loss J P,M ( θ ) gives better training results than the trained solution U ( x ; θ R ) with the deep Ritz loss J R,M ( θ ) ; see [40]. In our work, we will reinvestigate the performance of the two approaches for various hyper parameter settings and report some of our new ﬁndings.

As an enhancement to soft enforcement of boundary conditions, an augmented Lagrangian term can be included to the loss function [42] to obtain,

$$

$$

and

$$
LR,M(0,X) := JR,M(0) + (U(x;0) = g(x))A(x),
$$

x ∈ X ( ∂ Ω) for the PINN and deep Ritz loss functions, respectively. Here, the boundary condition is enforced as constraints on the neural network solution U ( x ; θ ) by introducing Lagrange multipliers λ ( x ) for each collocation point x in the training sampling set X ( ∂ Ω) . Hence, λ ( x ) are additional parameters that have to be trained, in addition to θ . The use of such an augmented Lagrangian term can improve slow training progress for the boundary loss term and can provide a more accurate trained neural network solution, U ( x ; θ ) . In the augmented Lagrangian approach, the parameters θ and λ are then optimized for the PINN and deep Ritz loss functions in the following sense:

$$
= arg resp arg max min M LR,1
$$

We note that the above optimization problems for θ are non-linear and non-convex while those for λ are linear. We thus use the Adam optimization method [20] in the gradient update for θ with a small learning rate ǫ and a simple gradient update for λ with a learning rate α , i.e.,

$$
Or
$$

The learning rate α is often set to a larger value than the learning rate ǫ , as proposed in two-scale update schemes for min-max optimization problems; see [14, 25, 7]. In our numerical experiments, we set ǫ = 0 . 001 for the Adam optimizer and α = 1 for the gradient ascent update.

We note that the augmented Lagrangian method can be considered as a loss balancing scheme, and in our numerical experiments, we will also conduct comparisons on various loss balancing schemes as listed in Table 1.

