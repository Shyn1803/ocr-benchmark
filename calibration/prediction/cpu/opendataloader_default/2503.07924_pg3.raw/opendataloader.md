- B. Quadratic Unconstrained Binary Optimization Model

The Quadratic Unconstrained Binary Optimization (QUBO) model provides a framework for solving combinatorial optimization problems, where the objective is to determine the optimal configuration of binary variables that minimizes a quadratic objective function. Formulated as an unconstrained optimization problem, it encodes the constraints within the objective function. The model is defined over binary variables xi ∈ {0,1}, and uses the quadratic function H(x) to represent pairwise interactions:

H(x) =

i̸=j

Qijxixj +

i

qixi (12)

where Qij denotes the interaction coefficients between xi and xj, and qi represents the linear coefficients for xi. The objective function H(x) can be interpreted as a Hamiltonian, analogous to the energy function in Ising model.

To incorporate constraints from (3), we add penalty terms:

H(x) = f(x) + P1

i

xS,i − 1

2

+ P2

i

xi,D − 1

2

+ P3

i̸∈{S,D}

 

j

xi,j −

k

xk,i

 

2

(13)

where P1, P2, and P3 are positive penalty coefficients that must be set large enough to ensure that any violation of the constraints is penalized heavily. Typically, P3 is chosen to be larger than P1 and P2 to enforce constraints more strictly.

Expanding (13) yields the quadratic terms Qij and linear terms qi as follows: Qij =P1

i̸=j

xS,ixS,j + P2

i̸=j

xi,Dxj,D

+ P3

i̸∈{S,D}

  

(i,j)∈E (i,k)∈E k̸=j

xi,jxi,k

+

(j,i)∈E (k,i)∈E k̸=j

xj,ixk,i − 2

(i,j)∈E (k,i)∈E

xi,jxk,i

  

(14) qi = − P1

i

xS,i − P2

i

xi,D

+ P3

i̸∈{S,D}

 

(i,j)∈E

xi,j +

(k,i)∈E

xk,i

  + f(x)

(15)

- C. Ising Model


The Ising model is a mathematical representation in statistical physics used to describe magnetic materials, where the system’s energy depends on the configuration of spin variables.

In the Ising model, each spin variable σi ∈ {−1,1} represents a binary state. The model’s Hamiltonian is given by:

H(σ) = −

i,j

Jijσiσj −

i

hiσi (16)

where Jij denotes the coupling strength between spins i and j, and hi represents the influence of an external magnetic field on spin i.

To convert the QUBO model to the Ising model, we use the transformation σi = 2xi − 1, which maps the binary variables xi ∈ {0,1} to Ising spins σi ∈ {−1,1}. The QUBO expression can be rewritten in terms of Ising variables:

σi + 1 2

(σi + 1)(σj + 1) 4

qi ·

Qij ·

+

H(σ) =

i

i̸=j

(Qij + Qji) 4

Qij 4

qi 2

+ i̸=j

=

σiσj +

σi

i

i̸=j

Qij 4

qi 2

+ i̸=j

+ i

(17) Thus, the coefficients in the Ising model are:

Qij 4

Jij = −

(18)

(Qij + Qji) 4

qi 2 − i̸=j

(19)

hi = −

We use this mapping to transform the original optimization problem into the Ising model, allowing it to be solved using CIM.

III. COHERENT ISING MACHINE

In this section, we introduce Coherent Ising Machine (CIM) and explain its application to solving our multi-objective routing model.

CIM is a quantum-inspired optimization technique that leverages principles from the Ising model. The Ising model represents optimization problems as energy minimization tasks, where the goal is to find the ground state of a system by minimizing its energy. In the context of combinatorial optimization, this ground state corresponds to an optimal or near-optimal solution. CIM utilizes an optical network of degenerate optical parametric oscillators (DOPOs) to represent spins in the Ising model. Each DOPO encodes the spin states using phase-coherent laser pulses, with the two possible phases corresponding to spin values of +1 or −1. The system’s energy is minimized by continuously adjusting the pump power, allowing CIM to evolve the spin states toward lower energy configurations and find solutions to the optimization problem.

Theoretically, CIM operates by solving an Ising problem defined by a Hamiltonian that represents the energy of the spin system. The objective is to find a spin configuration that minimizes this Hamiltonian, which corresponds to solving a combinatorial optimization problem. In practical implementations, the dynamic behavior of CIM can be modeled

