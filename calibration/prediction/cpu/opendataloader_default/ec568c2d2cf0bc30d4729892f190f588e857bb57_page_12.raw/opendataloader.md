J. Low Power Electron. Appl. 2011, 1 142

Table 2. Threshold voltage assignment of the three proposed registers.

Register 1 Register 2 Register 3 M1 low-Vth low-Vth low-Vth M2 low-Vth high-Vth low-Vth M3 low-Vth high-Vth low-Vth M4 low-Vth low-Vth low-Vth M7 low-Vth low-Vth high-Vth M8 low-Vth low-Vth high-Vth M9 low-Vth low-Vth high-Vth M10 low-Vth low-Vth high-Vth

- M13 high-Vth low-Vth low-Vth
- M14 high-Vth low-Vth low-Vth


- M17 high-Vth low-Vth low-Vth
- M18 high-Vth low-Vth low-Vth
- M19 high-Vth low-Vth low-Vth
- M20 high-Vth low-Vth low-Vth
- M21 high-Vth low-Vth low-Vth
- M22 high-Vth low-Vth low-Vth


4.3. Reduction in the Leakage Current

The amount of reduction in the leakage current achieved by utilizing the proposed three registers is evaluated in this section. Four CMOS technology generations, 45 nm, 32 nm, 22 nm, and 16 nm, are considered using a predictive technology model[28,29].

The register illustrated in Figure8 is simulated for each technology node where the W/L ratios of the transistors are maintained constant. The leakage current drawn from the power supply is evaluated for the three registers and the results are compared with the leakage current of the original register where only low-Vth transistors are used.

The results are illustrated in Figure9. Note that for the ﬁrst register, the state of the clock signal does not change the results since all of the high-Vth transistors are within the slave latch. For the second and third registers, however, high-Vth transistors exist within the tristate inverters. The state of the clock signal is therefore important in evaluating the results. For example, for the second register, clock signal should be at VSS to guarantee that the initial tristate inverter is not in the high impedance state. Similarly, for the third register, clock signal should be at VDD so that the second tristate inverter located along the feedback path is not in the high impedance state. The leakage current of the original register is therefore compared with the ﬁrst two registers and third register when the clock signal is, respectively, at VSS and VDD.

The leakage current increases with technology, exhibiting a large jump in the 16 nm node. A signiﬁcant amount of reduction in the leakage current, 79% on average, is achieved by the ﬁrst register since the number of high-Vth transistors is higher, as listed in Table2. The second register also achieves a considerable amount of reduction in the leakage current, 13% on average and higher below 32 nm

