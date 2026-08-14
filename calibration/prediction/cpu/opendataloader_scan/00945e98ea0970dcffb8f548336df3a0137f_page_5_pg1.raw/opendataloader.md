This can be explained by the relative high damping in the suspension of the coil (see Figure 5) combined with the relative small force introduced into the shaker by the impact hammer, leading to a totally damped acceleration response of the table.

Table 2. Modal parameters

<table>
  <tr>
    <th> </th>
    <th> </th>
    <th colspan="2">Values</th>
  </tr>
  <tr>
    <td>Modal parameter</td>
    <td>Symbol</td>
    <td>Calculated</td>
    <td>Determined experimentally</td>
  </tr>
  <tr>
    <td>Modal mass of the body</td>
    <td> </td>
    <td>77.2 9</td>
    <td>18.2 g</td>
  </tr>
  <tr>
    <td>Modal mass of the body</td>
    <td>mz</td>
    <td>3.167 kg</td>
    <td>3.33 kg</td>
  </tr>
  <tr>
    <td>Modal damping of the suspension of the coil</td>
    <td> </td>
    <td>196.15 kg/s</td>
    <td>76 kg/s</td>
  </tr>
  <tr>
    <td>Modal damping of the isolation studs</td>
    <td>C2</td>
    <td>196.15 kgls</td>
    <td>76 kgls</td>
  </tr>
  <tr>
    <td>Modal stiffness of the suspension of the coil</td>
    <td> </td>
    <td>12.3*103 kg/sz</td>
    <td>28.02*103 kg/sz</td>
  </tr>
  <tr>
    <td>Modal stiffness of isolation studs</td>
    <td>kz</td>
    <td>1.143·10 kg/s²</td>
    <td>1.15 ·10 kg/s²</td>
  </tr>
</table>


# 4 Determination of the electrical parameters  

Looking at (1) gives us the needed electrical parameters to be defined. We find R   and L , the resistance and the inductance of the coil, µ f , the force constant, and µ bemf , the bemf (back electromagnetic force) constant of the system.

R   and L   are the intrinsic electrical properties of the   coil and are purely passive. A simple measurement on the RLC meter will allow us to get those values. These are given in Table 3. The quantities µ   and µ   are representative of the

f bemf same phenomenon – the expression of the Lorentz force – but have neither the same causes nor the same effects.

Lorentz expresses that the charge carriers of a conductor immersed in a (non-collinear) magnetic field are subjected to a force when moving and this according to the following relation:

$$

$$

With F q   the force exerted on a charge carrier of electrical charge q   subjected to an electric field E , undergoing a speed v , and immersed in a magnetic field B .

The generalized expression of this force on conductor of length l is:

$$

$$

The current i flowing in the coil generates a force F on the latter with respect to the force constant µ f . The magnitude µ   expresses the force undergone

The magnitude   Ubemf expresses the force undergone by the electrons in conductor which moves in magnetic field. The displacement of the coil generates an electric potential at the conductor terminals with respect to the bemf constant_

We study a system which on the one hand generates a force due to an applied current and on the other hand which creates an electrical potential   with respect to the speed of the coil . This approach forms the basis of the development of a two-port network model and goes beyond the scope of this work. Different authors such as York, Smallwood or Guillaume develop this aspect deeper in detail [11–13].

# 4.1 Experimental determination of the force constant

First, we used the assembly already presented in Figure 3 which blocks the vibrating table. A voltage is applied to the terminals which generates a current, which creates a force. Due to the rigid structure, the table cannot move and no bemf can settle.

A measurement of the force with respect to the current yields the force constant. The latter is shown in Figure 9 for three different drive voltages. We immediately notice a very strong structural

response at 660 Hz due to the resonance of the structure originally intended to be rigid. By performing a modal analysis of this structure, we obtained its frequency response. The synthesized curve has been superimposed on the measured curves to emphasize the response due to the resonance of the beam structure.

![](<00945e98ea0970dcffb8f548336df3a0137f_page_5_pg1_images/imageFile1.png>)

Force Constant

1

Dnve Volege

Dnve Votage

Frequency (Hz)

Fig. 9. Force Constant analysis for different drive voltages. The synthesized FRF of the beam structure is superimposed on the measured curves to emphasize the response due to the resonance of the beam structure.

Beyond this, the measurements tend to show an increase in damping with the drive voltage underlying a possible non-linearity of the system. At this point any deduction is dangerous and should

be avoided. Further analysis is required. Nevertheless, in the area below 100 Hz, the relative theoretical error due to the resonating structure with respect to the unity does not exceed 3%. Despite a relative variation in amplitude of 5% over the frequencies, the value of µ f is considered to be constant. Its average value is 7.8493 N/A against an initial value form the manufacturer of 6.4 N/A. These data are shown in Table 3.

