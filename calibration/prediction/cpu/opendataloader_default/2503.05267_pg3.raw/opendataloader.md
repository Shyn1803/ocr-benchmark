Transmission problems and domain decompositions for parabolic equations on evolving domains 3

problem becomes



𝑢𝑖(𝑡) − ∇ · 𝛼(𝑡)∇𝑢𝑖(𝑡) + ∇ · w(𝑡) + 𝛽(𝑡) 𝑢𝑖(𝑡) = 𝑓𝑖(𝑡) in Ω𝑖(𝑡), 𝑢𝑖(𝑡) = 0 on 𝜕Ω𝑖(𝑡) \ Γ(𝑡) for 𝑖 = 1, 2,

(2)

𝑢1(𝑡) = 𝑢2(𝑡) on Γ(𝑡), 𝛼(𝑡)∇𝑢1(𝑡) · 𝜈1(𝑡) + 𝛼(𝑡)∇𝑢2(𝑡) · 𝜈2(𝑡) = 0 on Γ(𝑡),

 

where 𝜈𝑖(𝑡) is the unit outward normal vector of 𝜕Ω𝑖(𝑡), 𝑓𝑖(𝑡) = 𝑓 (𝑡)|Ω𝑖(𝑡), and 𝑢𝑖(𝑡) = 𝑢(𝑡)|Ω𝑖(𝑡).

The non-overlapping domain decompositions can then be derived by approximating the transmission problem. For example, consider the classic Robin–Robin method, first introduced in [27]. By taking linear combinations of the last two equations in (2), one has the equivalent Robin conditions

𝛼(𝑡)∇𝑢1(𝑡) · 𝜈𝑖(𝑡) + 𝑠0𝑢1(𝑡) = 𝛼(𝑡)∇𝑢2(𝑡) · 𝜈𝑖(𝑡) + 𝑠0𝑢2(𝑡) on Γ(𝑡) for 𝑖 = 1, 2,

and a method parameter 𝑠0 > 0. Alternating between the subdomains then gives the Robin– Robin method as computing (𝑢1𝑛, 𝑢2𝑛) for 𝑛 = 1, 2, . . . with



- 𝑢1𝑛(𝑡) − ∇ · 𝛼(𝑡)∇𝑢1𝑛(𝑡) + ∇ · w(𝑡) + 𝛽(𝑡) 𝑢1𝑛(𝑡) = 𝑓1(𝑡) in Ω1(𝑡), 𝑢1𝑛(𝑡) = 0 on 𝜕Ω1(𝑡) \ Γ(𝑡),

𝛼(𝑡)∇𝑢1𝑛(𝑡) · 𝜈1(𝑡) + 𝑠0𝑢1𝑛(𝑡) = 𝛼(𝑡)∇𝑢2𝑛−1(𝑡) · 𝜈1(𝑡)+𝑠0𝑢2𝑛−1(𝑡) on Γ(𝑡),

- 𝑢2𝑛(𝑡) − ∇ · 𝛼(𝑡)∇𝑢2𝑛(𝑡) + ∇ · w(𝑡) + 𝛽(𝑡) 𝑢2𝑛(𝑡) = 𝑓2(𝑡) in Ω2(𝑡), 𝑢2𝑛(𝑡) = 0 on 𝜕Ω2(𝑡) \ Γ(𝑡),


(3)

𝛼(𝑡)∇𝑢2𝑛(𝑡) · 𝜈2(𝑡) + 𝑠0𝑢2𝑛(𝑡) = 𝛼(𝑡)∇𝑢1𝑛(𝑡) · 𝜈2(𝑡)+𝑠0𝑢1𝑛(𝑡) on Γ(𝑡).

 

Here, 𝑢02 is an initial guess and 𝑢𝑖𝑛(𝑡) approximates 𝑢𝑖(𝑡) = 𝑢(𝑡)|Ω𝑖(𝑡). Note that the Robin– Robin method is sequential, but the computation of each 𝑢𝑖𝑛 can be implemented in parallel when Ω𝑖(𝑡) is a union of nonadjacent subdomains, as is the case in Figure 1.

The well posedness of parabolic equations on evolving domains can be derived via the framework [3], which relies on a variational formulation where the standard Sobolev– Bochner solution space

𝐻1 (0,𝑇); 𝐻−1(Ω) ∩ 𝐿2 (0,𝑇); 𝐻01(Ω) (4)

is generalized to evolving domains Ω(𝑡). The framework has also been extended to a Banach space setting [2]. This variational setting constitutes the starting point of the design and analysis of a wide range of finite element methods for equations on evolving domains. The

