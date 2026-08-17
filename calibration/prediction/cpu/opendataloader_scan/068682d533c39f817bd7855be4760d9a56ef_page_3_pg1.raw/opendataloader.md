# IV.   D IRECT MIMO   QFT   D ESIGN  

The MIMO QFT design technique provides a design procedure to synthesize a fixed diagonal controller transfer function matrix G (s) and prefilter F (s) to satisfy specifications on the closed-loop system shown in Fig.2, where P (s) is the MIMO uncertain plant. The basic principle for MIMO QFT design is to

convert the MIMO control system into a set of equivalent MISO control systems. Using fixed-point theorem, the MIMO control problem for an m × m system can be converted into m equivalent single-loop MISO problems, each with two inputs and one output. The objective of the design is to achieve set point tracking, while minimizing the outputs due to the disturbance inputs (cross-coupling effects) [5, 6].

# V.   C OMBINED QFT/EEAS   D ESIGN  

# A. Problem formulation With no loss of

generality and for simplicity, the design process is developed for 2 × 2 MIMO plants. The procedure can be easily extended to the general MIMO case. Consider the feedback structure shown in Fig. 3. The transfer function matrix 2 , 1 , , )] ( [ ) ( = = j i s p s P ij   represents the LTI uncertain 2 × 2 MIMO plant to be controlled. The 3 , 2 , 1 , )] ( ), ( [ 2 1 = = i s g s g diag G i i i and )] ( ), ( [ ) ( 22 11 s f s f diag s F = , which are assumed diagonal, represent the feedforward compensators and the prefilter matrix, respectively. Also, the nonlinear elements 1 N and 2 N are assumed to be ideal relays with outputs 01 M ± and 02 M ± . Moreover, 1 V and 2 V are the excitation signals.

Let ) ( / s T R Y be the input-output relation from the input ) ( s R to the output ) ( s Y , which is clearly derived as  

V 1 = A 0 1 Sin (ω

![](<068682d533c39f817bd7855be4760d9a56ef_page_3_pg1_images/imageFile2.png>)

(@ol

F(s

P(s

V 2 = A 0 2 Sin (ω

Fig. 3. The combined QFT/EEAS structure for 2 × 2 MIMO plants

  where, ) ( ω ij A and ) ( ω ij B are the upper and lower specifications. For simplicity, this paper will concentrate on tracking performance in (9), but there may be other specifications on sensitivity, sensor noise to input sensitivity, as well as engineering considerations such as those in direct MIMO-QFT. At high frequencies the benefits of feedback are negligible. High frequency specifications will result in large bandwidth with very little closed-loop performance improvement. It is thus recommended that the specifications to be enforced to the lowest possible frequency h ω (the Horowitz frequency). In addition, an implicit design objective is the minimization of the loop bandwidths when sensor noise attenuation is concerned.

# B. Development of the Design Process

are satisfied, the closed-loop transfer of this MIMO control system could be expressed as

$$
t11 (s) t12 (s) 10) t21 (s) t22 (s)
$$

where, Y (s) is the system output, R (s) is the input vector. Through an appropriate transformation, the four

transfer functions in the closed-loop transfer matrix are derived as:  

$$
8
$$

Nf = diag (nf1,nf2) the describing functions of the relays) are

and it is assumed here that the plant set is finite or can be adequately approximated by a finite set so that numerical algorithms can be developed. The combined QFT/EEAS control design task is to find ) ( s G i and ) ( s F with proper rational and stable elements, in order to satisfy the performance specifications ∀ P   ∈ {P}. For example, tracking specifications may require that ∀ P   ∈ {P},  

$$
(9)
$$

![](<068682d533c39f817bd7855be4760d9a56ef_page_3_pg1_images/imageFile1.png>)

F (s)

G (s)  

Fig. 2. 2DOF MIMO-QFT Control Structure

$$
t21 922 912 t21 = 921 922 (11) 1+ 82
$$

$$
t22 t12 g2 922 f22 922 For input r2 t12 912 t21 = 921 911 922
$$

$$
where, = = Ap1 , q11 912 921 922 Ap2z ~Np1z
$$

These four transfer functions represent the resulting four equivalent single-loop MISO control systems, as expressed by their signal flow graphs shown in Fig. 4.

![](<068682d533c39f817bd7855be4760d9a56ef_page_3_pg1_images/imageFile3.png>)

Cii

0 Vii

g i

q ii  

$$
kzi Qik
$$

