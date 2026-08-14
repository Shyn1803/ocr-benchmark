IV. DIRECT MIMO QFT DESIGN

The MIMO QFT design technique provides a design procedure to synthesize a fixed diagonal controller transfer function matrix G(s) and prefilter F(s) to satisfy specifications on the closed-loop system shown in Fig.2, where P(s) is the MIMO uncertain plant.

The basic principle for MIMO QFT design is to convert the MIMO control system into a set of equivalent MISO control systems. Using fixed-point theorem, the MIMO control problem for an m × m system can be converted into m equivalent single-loop MISO problems, each with two inputs and one output. The objective of the design is to achieve set point tracking, while minimizing the outputs due to the disturbance inputs (cross-coupling effects) [5, 6].

V. COMBINED QFT/EEAS DESIGN A. Problem formulation

With no loss of generality and for simplicity, the design process is developed for 2 × 2 MIMO plants. The procedure can be easily extended to the general MIMO case. Consider the feedback structure shown in Fig. 3. The transfer function matrix P(s) = [pij (s)] , i, j = 1,2 represents the LTI uncertain 2 × 2 MIMO plant to be controlled. The Gi = diag[gi1(s),gi2(s)], i =1,2,3 and

F(s) = diag [ f11(s), f22(s)], which are assumed diagonal, represent the feedforward compensators and the prefilter matrix, respectively. Also, the nonlinear elements N1and

N2 are assumed to be ideal relays with outputs ±M01and ±M02 . Moreover, V1and V2 are the excitation signals.

Let TY /R (s) be the input-output relation from the input R(s) to the outputY(s) , which is clearly derived as

TY/R(s) = [I + P(s)G(s)]−1 P(s)G(s)F(s ) (8) where, G = G3G2N fG1 ( N f = diag (nf1,nf 2) , are the describing functions of the relays).

Due to uncertainty, P ∈{P} is a set of possible plants and it is assumed here that the plant set is finite or can be adequately approximated by a finite set so that numerical algorithms can be developed. The combined QFT/EEAS control design task is to find Gi(s) and F(s) with proper rational and stable elements, in order to satisfy the performance specifications ∀P ∈{P}. For example, tracking specifications may require that ∀P ∈{P},

Bij(ω)≤ TY/R( jω)ij ≤ Aij(ω) (9)

y(t)

r(t)

<table>
  <tr>
    <td>P (s,α)</td>
  </tr>
</table>


<table>
  <tr>
    <td>G(s)</td>
  </tr>
</table>


<table>
  <tr>
    <td>F(s)</td>
  </tr>
</table>


+ -

Fig. 2. 2DOF MIMO-QFT Control Structure

- V1= A01 Sin (ω01 t)
- V2= A02 Sin (ω02 t)


+

Y(s) G1(s) G2(s)

N1 − N2

R(s)

<table>
  <tr>
    <td rowspan="2"> </td>
    <td colspan="2"> </td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
  </tr>
</table>


<table>
  <tr>
    <td>F(s)</td>
  </tr>
</table>


<table>
  <tr>
    <td rowspan="2">G3(s)</td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
</table>


P(s)

+

+

Fig. 3. The combined QFT/EEAS structure for 2 × 2 MIMO plants

where, Aij(ω) and Bij(ω) are the upper and lower specifications. For simplicity, this paper will concentrate on tracking performance in (9), but there may be other specifications on sensitivity, sensor noise to input sensitivity, as well as engineering considerations such as those in direct MIMO-QFT. At high frequencies the benefits of feedback are negligible. High frequency specifications will result in large bandwidth with very little closed-loop performance improvement. It is thus recommended that the specifications to be enforced to the lowest possible frequencyωh (the Horowitz frequency). In addition, an implicit design objective is the minimization of the loop bandwidths when sensor noise attenuation is concerned.

B. Development of the Design Process

In Fig.3, if the quasilinear conditions are satisfied, the closed-loop transfer of this MIMO control system could be expressed as

⎡

⎤

⎡

⎤

( ) ( ) ( ) ( )

t s t s Y s TY R R s (10) where, Y(s) is the system output, R(s) is the input vector.

r t s t s

11 12

1 21 22

## = =

⎢ ⎣

⎥ ⎦

⎢ ⎣

⎥ ⎦

/ ( ) ( )

r

2

Through an appropriate transformation, the four transfer functions in the closed-loop transfer matrix are derived as:

- For input r1 : 2 22

22 21

11

21 1 11

11 12

21 1 11 11

11 1

, 1 g q

q q

t t

g q

q q

t g q f

t

+

⎟ ⎠

⎞

⎜ ⎝

⎛ −

=

+

⎟ ⎠

⎞

⎜ ⎝

⎛ −

=

(11)

- For input r2 : 2 22


⎛ −

⎞

⎛ −

⎞

t t

t g q f

⎜ ⎝

⎟ ⎠

⎜ ⎝

⎟ ⎠

22

12 2 22 22

q q

q q

11 12

22 21

=

=

, 1 g q

t g q

12 1

21 1 11

+

+

where, q11 = ∆/p22, q12 = −∆/p12 , q21 = −∆/p21,q22 = ∆/p11, ∆= p11 p22-p12 p21 and gi = g3i g2i nf i g1i ,i =1,2 .

These four transfer functions represent the resulting four equivalent single-loop MISO control systems, as expressed by their signal flow graphs shown in Fig. 4.

cij

rj

yij fij gi qii

1

-1

t

Fig.4. 2×2MISOStructurefortij(fij=0fori≠j,cij= ∑

kj

# −

)

q

≠

k i ik

