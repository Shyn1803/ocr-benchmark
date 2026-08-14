# 3.2 Mechanical parameters identification

Figure 4 and Figure 5 show the plotted response curves as a least square estimation of the measurements for both blocked table and free table configurations.

![](<00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1_images/imageFile1.png>)

Isolation Studs Characterization

Blocked Table Configuration

Experimental Data

Fitted Curve

1

Estimated values

30,41 Hz

0.1763

Frequency (Hz)

Fig. 4. Response curve of the isolation studs and the one DOF estimation in the blocked table configuration. With f n   the natural frequency and ξ the damping ratio.

![](<00945e98ea0970dcffb8f548336df3a0137f_page_3_pg1_images/imageFile2.png>)

Coil Suspension Characterization

Free Table Configuration

Experimental Data

Fitted Curve

Estimated YAlues:

0.5879

1

150

100

Frequency (Hz)

Fig. 5. Response curve of the vibrating table and the one DOF estimation in the free table configuration. With f n   the natural frequency and ξ the damping ratio.

The responses of the system correspond to 1DOF oscillators and using a least square estimation we obtained the values of the mechanical parameters. Those values are given in Table 1 with respect to the parameters given by the manufacturer.

# 3.3 Modal parameters

The developed method requires an external possibility of making the shaker vibrate and is quite difficult to apply to larger shakers. In this case, modal analysis is an alternative since the mechanical parameters and the modal ones are equivalent to characterize the system. In this section, a short review of the modal theory

will be presented to sufficiently master this equivalence as the relationship between movement, global coordinates, modal coordinates, and modal parameters.  

Table 1. Mechanical parameters

<table>
  <tr>
    <th> </th>
    <th> </th>
    <th colspan="2">Values</th>
  </tr>
  <tr>
    <td>Parameter</td>
    <td>Symbol</td>
    <td>Given by the manufacturer[6]</td>
    <td>Dctermined experimentally</td>
  </tr>
  <tr>
    <td>Mass of the vibrating table</td>
    <td> </td>
    <td>60 g</td>
    <td> </td>
  </tr>
  <tr>
    <td>Mass of the body</td>
    <td>MB</td>
    <td>8.3 kg</td>
    <td>8.375 kg</td>
  </tr>
  <tr>
    <td>Damping of the suspension of the coil</td>
    <td>CT</td>
    <td> </td>
    <td>564.3 Ns/m</td>
  </tr>
  <tr>
    <td>Damping of the isolation studs</td>
    <td>B</td>
    <td> </td>
    <td>564.3 Ns/m</td>
  </tr>
  <tr>
    <td>suspension of the coil</td>
    <td> </td>
    <td>12·10 3 N/m</td>
    <td>11.95·10 3 N/m</td>
  </tr>
  <tr>
    <td>Stiffness of the isolation studs a For testing</td>
    <td>kB</td>
    <td> </td>
    <td>3.06105 Nlm</td>
  </tr>
</table>


aFor purposes; the original vibrating table is equipped with an extra 16 g fastening bolt. testing

# 3.3.1 Theoretical aspects

If we only consider the purely mechanical system as depicted in Figure 2(a), the global equations (1) can be generalized by:

$$
Mz +Cz + Kz = F
$$

Where M , C , and K   are respectively the mass, damping, and stiffness matrices of the system. Solving the eigenvalues problem for the free

undamped system yields the transformation matrix P   between the modal coordinates q   and the global coordinates z according [7]:

$$
2 = (3 Pq
$$

The premultiplication by P T   allows to diagonalize M   and K since both are symmetrical. Despite that C is also symmetrical, the damping matrix cannot be diagonalized and we can consider a linear combination of M   and K [8]. Considering this, we now can express (2) as:

$$

$$

i i i the modal mass, damping and stiffness of the i th   mode. Q i   is the modal force and q i   is the modal coordinate of the i th mode.

Whereas the system described by (2) is coupled, the system described by (4) is uncoupled since all the matrices have been diagonalized. The solutions q to the decoupled equations are given

The solutions qi to the decoupled equations are given by:

$$
9 (i =1,2) + jc;@) Pk;
$$

Pk i is the characteristic polynomial of mode i and j is the complex constant.  

