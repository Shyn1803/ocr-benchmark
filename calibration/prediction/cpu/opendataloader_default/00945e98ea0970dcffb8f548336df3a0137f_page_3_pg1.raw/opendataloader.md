MATEC Web of Conferences 148, 05003 (2018) https://doi.org/10.1051/matecconf/201814805003 ICoEV 2017

- 3.2 Mechanical parameters identification

Figure 4 and Figure 5 show the plotted response curves as a least square estimation of the measurements for both blocked table and free table configurations.

![](<00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1_images/imageFile1.png>)

- Fig. 4. Response curve of the isolation studs and the one DOF estimation in the blocked table configuration. With fn the natural frequency and ξ the damping ratio.

![](<00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1_images/imageFile2.png>)

- Fig. 5. Response curve of the vibrating table and the one DOF estimation in the free table configuration. With fn the natural frequency and ξ the damping ratio.


The responses of the system correspond to 1DOF oscillators and using a least square estimation we obtained the values of the mechanical parameters. Those values are given in Table 1 with respect to the parameters given by the manufacturer.

- 3.3 Modal parameters


The developed method requires an external possibility of making the shaker vibrate and is quite difficult to apply to larger shakers. In this case, modal analysis is an alternative since the mechanical parameters and the modal ones are equivalent to characterize the system.

In this section, a short review of the modal theory will be presented to sufficiently master this equivalence as the relationship between movement, global coordinates, modal coordinates, and modal parameters.

Table 1. Mechanical parameters

<table>
  <tr>
    <td rowspan="2">Parameter</td>
    <td rowspan="2">Symbol<br><br></td>
    <td colspan="2">Values</td>
  </tr>
  <tr>
    <td>Given by the manufacturer[6]</td>
    <td>Determined experimentally</td>
  </tr>
  <tr>
    <td>Mass of the vibrating table</td>
    <td>mT</td>
    <td>60 g</td>
    <td>76 ga</td>
  </tr>
  <tr>
    <td>Mass of the body</td>
    <td>MB</td>
    <td>8.3 kg</td>
    <td>8.375 kg</td>
  </tr>
  <tr>
    <td>Damping of the suspension of the coil</td>
    <td>cT</td>
    <td>–</td>
    <td>35.43 Ns/m</td>
  </tr>
  <tr>
    <td>Damping of the isolation studs</td>
    <td>cB</td>
    <td>–</td>
    <td>564.3 Ns/m</td>
  </tr>
  <tr>
    <td>Stiffness of the suspension of the coil</td>
    <td>kT</td>
    <td>12·103 N/m</td>
    <td>11.95·103 N/m</td>
  </tr>
  <tr>
    <td>Stiffness of the isolation studs</td>
    <td>kB</td>
    <td>–</td>
    <td>3.06·105 N/m</td>
  </tr>
</table>


aFor testing purposes, the original vibrating table is equipped with an extra 16 g fastening bolt.

3.3.1 Theoretical aspects

If we only consider the purely mechanical system as depicted in Figure 2(a), the global equations (1) can be generalized by:

MzCz  Kz  F (2) Where M, C, and K are respectively the mass,

damping, and stiffness matrices of the system.

Solving the eigenvalues problem for the free undamped system yields the transformation matrix P between the modal coordinates q and the global coordinates z according [7]:

z  Pq (3)

The premultiplication by PT allows to diagonalize M and K since both are symmetrical. Despite that C is also symmetrical, the damping matrix cannot be diagonalized and we can consider a linear combination of M and K [8]. Considering this, we now can express (2) as:

miqi  ciqi  kiqi  Qi (i 1,2) (4)

The modal parameters mi, ci, and ki are respectively the modal mass, damping and stiffness of the ith mode. Qi is the modal force and qi is the modal coordinate of the ith mode.

Whereas the system described by (2) is coupled, the system described by (4) is uncoupled since all the matrices have been diagonalized.

The solutions qi to the decoupled equations are given by:

Q q

Q k m jc

 i Pk

   

i i i i

i

( 1,2) ( 2 )

i  

i

(5)

Pki is the characteristic polynomial of mode i and j is the complex constant.

3

