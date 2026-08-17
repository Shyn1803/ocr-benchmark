problem becomes

$$
in Qi (t). Ui(t) = 0 on (2) u1 (t) = u2 (t) on T(t) ,
$$

( )| Ω 𝑖 ( 𝑡 ) The non-overlapping domain decompositions can then be derived by approximating the transmission problem. For example, consider the classic Robin–Robin method, first introduced in [ 27 ]. By taking linear combinations of the last two equations in ( 2 ), one has the equivalent Robin conditions

$$
Vi(t) + sou1 (t) = ơ(t) Vuz(t) Vi(t) + sou2 (t) on F(t) for i = 1,2,
$$

and a method parameter 𝑠 0 > 0. Alternating between the subdomains then gives the Robin– Robin method as computing ( 𝑢 𝑛 1 , 𝑢 𝑛 2 ) for 𝑛 = 1 , 2 , . . . with

$$
in Q1 (t) , on (t) F(t), on F(t), (3) w(t) + B(t))u? (t) = f2(t) in Q2(t) , u2 (t) = 0 on F(t) , v2(t)+soun (t) on T(t) .
$$

2 𝑖 ( ) 𝑖 ( ) ( )| Ω 𝑖 ( 𝑡 ) Robin method is sequential, but the computation of each 𝑢 𝑛 𝑖 can be implemented in parallel when Ω 𝑖 ( 𝑡 ) is a union of nonadjacent subdomains, as is the case in Figure 1 . The well posedness of parabolic equations on evolving domains can be derived via

the framework [ 3 ], which relies on a variational formulation where the standard Sobolev– Bochner solution space

$$

$$

is generalized to evolving domains Ω ( 𝑡 ) . The framework has also been extended to a Banach space setting [ 2 ]. This variational setting constitutes the starting point of the design and analysis of a wide range of finite element methods for equations on evolving domains. The

