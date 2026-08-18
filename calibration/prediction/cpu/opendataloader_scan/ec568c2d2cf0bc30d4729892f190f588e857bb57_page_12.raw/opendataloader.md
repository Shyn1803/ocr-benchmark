Table 2. Threshold voltage assignment of the three proposed registers.

<table>
  <tr>
    <th> </th>
    <th>Register 1</th>
    <th>Register 2</th>
    <th>Register 3</th>
  </tr>
  <tr>
    <td>MI</td>
    <td> </td>
    <td>lowV th</td>
    <td> </td>
  </tr>
  <tr>
    <td>M2</td>
    <td> </td>
    <td>highV th</td>
    <td> </td>
  </tr>
  <tr>
    <td>M3</td>
    <td>low-Vth</td>
    <td>highV th</td>
    <td>th lowV th</td>
  </tr>
  <tr>
    <td>M4</td>
    <td>low-Vth</td>
    <td>low-Vth</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>M7</td>
    <td>low-Víh</td>
    <td> </td>
    <td>highV th</td>
  </tr>
  <tr>
    <td>M8</td>
    <td> </td>
    <td>th lowV th</td>
    <td> </td>
  </tr>
  <tr>
    <td>M9</td>
    <td>low-Vth</td>
    <td>Vth low-</td>
    <td>highV th</td>
  </tr>
  <tr>
    <td>MIO</td>
    <td>low-Vth</td>
    <td>low-Vth</td>
    <td>highV th</td>
  </tr>
  <tr>
    <td>MI3</td>
    <td>high-Víh</td>
    <td>low-Víh</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>MI4</td>
    <td>high-Víh</td>
    <td> </td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>MI7</td>
    <td>high-Víh</td>
    <td>Vth low-</td>
    <td> </td>
  </tr>
  <tr>
    <td>MI8</td>
    <td>high-Víh</td>
    <td>low-Vth</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>MI9</td>
    <td>high-Vth</td>
    <td>low-Vth</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>M2O</td>
    <td>high-Víh</td>
    <td>low-Víh</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>M2I</td>
    <td>high-Víh</td>
    <td>low-Vh</td>
    <td>lowV th</td>
  </tr>
  <tr>
    <td>M22</td>
    <td>high-Víh</td>
    <td> </td>
    <td> </td>
  </tr>
</table>


# 4.3. Reduction in the Leakage Current

The amount of reduction in the leakage current achieved by utilizing the proposed three registers is evaluated in this section. Four CMOS technology generations, 45 nm, 32 nm, 22 nm, and 16 nm, are considered using a predictive technology model[ 28 , 29 ].

The register illustrated in Figure 8 is simulated for each technology node where the W / L ratios of the transistors are maintained constant. The leakage current drawn from the power supply is evaluated for the three registers and the results are compared with the leakage current of the original register where only lowV th transistors are used.

The results are illustrated in Figure 9 . Note that for the ﬁrst register, the state of the clock signal does not change the results since all of the highV th transistors are within the slave latch. For the second and third registers, however, highV th transistors exist within the tristate inverters. The state of the clock signal is therefore important in evaluating the results. For example, for the second register, clock signal should be at V SS to guarantee that the initial tristate inverter is not in the high impedance state. Similarly, for the third register, clock signal should be at V DD so that the second tristate inverter located along the feedback path is not in the high impedance state. The leakage current of the original register is therefore compared with the ﬁrst two registers and third register when the clock signal is, respectively, at V SS and V DD .

The leakage current increases with technology, exhibiting a large jump in the 16 nm node. A signiﬁcant amount of reduction in the leakage current, 79% on average, is achieved by the ﬁrst register since the number of highV th transistors is higher, as listed in Table 2 . The second register also achieves a considerable amount of reduction in the leakage current, 13% on average and higher below 32 nm

