# B. Quadratic Unconstrained Binary Optimization Model

The Quadratic Unconstrained Binary Optimization (QUBO) model provides a framework for solving combinatorial optimization problems, where the objective is to determine the optimal configuration of binary variables that minimizes a quadratic objective function. Formulated as an unconstrained optimization problem, it encodes the constraints within the objective function. The model is defined over binary variables x i ∈ { 0 , 1 } , and uses the quadratic function H ( x ) to represent pairwise interactions:

$$
H(s) = (12)
$$

where Q ij denotes the interaction coefficients between x i and x j , and q i represents the linear coefficients for x i . The objective function H ( x ) can be interpreted as a Hamiltonian, analogous to the energy function in Ising model. To incorporate constraints from (3), we add penalty terms:

To incorporate constraints from (3), we add penalty terms:

$$
+ Pz + P3 Tk,i (13)
$$

where P 1 , P 2 , and P 3 are positive penalty coefficients that must be set large enough to ensure that any violation of the constraints is penalized heavily. Typically, P 3 is chosen to be larger than P 1 and P 2 to enforce constraints more strictly. Expanding (13) yields the quadratic terms Q and linear

terms q i as follows:

$$
Qij = Pi i#j i#j + P3 i4{S,D} (i,j)eE (i,k)eE k#j (j,i)eE (k,i)eE (i,j)eE (k,i)eE qi = _ P1 (15)
$$

$$
Pz + P3 ig{S,D} (i.j)eE (k,i)eE Ti.D
$$

# C. Model Ising

The Ising model is a mathematical representation in statistical physics used to describe magnetic materials, where the system’s energy depends on the configuration of spin variables.

$$
(16) i,j
$$

where J ij denotes the coupling strength between spins i and j , and h i represents the influence of an external magnetic field on spin i . To convert the QUBO model to the Ising model, we use

the transformation σ i = 2 x i − 1 , which maps the binary variables x i ∈ { 0 , 1 } to Ising spins σ i ∈ {− 1 , 1 } . The QUBO expression can be rewritten in terms of Ising variables:

$$
+1)(0j + 1) 0i + 1 H(ơ) = EQij + Eq 2 i#j = + 2 (Qij Oi 4 2 Qi Qij 2 (17) Liti
$$

Thus, the coefficients in the Ising model are:

$$
Qij (18) 4 Jij
$$

$$
itj(Qij + Qji) hi = (19) 2
$$

We use this mapping to transform the original optimization problem into the Ising model, allowing it to be solved using CIM.

# III. C OHERENT I SING M ACHINE

In this section, we introduce Coherent Ising Machine (CIM) and explain its application to solving our multi-objective routing model. CIM is a quantum-inspired optimization technique that

leverages principles from the Ising model. The Ising model represents optimization problems as energy minimization tasks, where the goal is to find the ground state of a system by minimizing its energy. In the context of combinatorial optimization, this ground state corresponds to an optimal or near-optimal solution. CIM utilizes an optical network of degenerate optical parametric oscillators (DOPOs) to represent spins in the Ising model. Each DOPO encodes the spin states using phase-coherent laser pulses, with the two possible phases corresponding to spin values of +1 or − 1 . The system’s energy is minimized by continuously adjusting the pump power, allowing CIM to evolve the spin states toward lower energy configurations and find solutions to the optimization problem. Theoretically, CIM operates by solving an Ising problem

defined by a Hamiltonian that represents the energy of the spin system. The objective is to find a spin configuration that minimizes this Hamiltonian, which corresponds to solving a combinatorial optimization problem. In practical implementations, the dynamic behavior of CIM can be modeled

