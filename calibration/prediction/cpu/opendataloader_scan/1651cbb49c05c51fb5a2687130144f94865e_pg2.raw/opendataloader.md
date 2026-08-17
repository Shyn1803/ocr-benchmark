$$
0.262 _K1 1+ 28.17
$$

$$
Dso2_ 0.374 esoz_to 16.74 1+ DsOz
$$

       In agreement with experimental data [10], the mathematical relationship between the concentration of NO x and the blocking of the current I Na is the following:  

$$
bno_Na 6.8 523 1+(Do
$$

     where D NO is the NO x concentration in nM. To simulate the effect of the NO x on the I CaL current, the Michaelis-Menten equation was implemented as follows:  .   (      )

$$
0.59(Dvo) 8 eNo_CaL DNo+0.007
$$

       .    where the values 0.59 nM and 0.007 nM are the values of e max and half-maximal effective concentration (EC 50 ) respectively. This equation was fitted using human atrial myocyte data from [11]. The blocking and increasing factors were introduced to the I CaL , I Na , I K1, and I to equations in the cell model, as follows:

$$
IcaL (1 bco_caL)(1 CaL)(1 + evo_caL)gcaLdf fca (Vm 65) INa (1 + _Na)(1 ENa) (10) EK1) IK1 e0.07( + 80) (10) 1 + Ito = (1 + to )gtooa?oi(Vm - Eto) = (11) bsoz esoz (Vm esoz
$$

        _           The modified model was incorporated into a 3D model of human atria to evaluate the dynamics of propagation.  

# 2.2. 3D model of human atrial

A 3D virtual model of human atria was implemented [12]. The model comprises the main anatomical structures, it is composed of 515010 hexahedral elements with a spatial resolution of 300 μm. It includes realistic fiber orientation, electrophysiological heterogeneity, and anisotropy. To simulate the cardiac action potential propagation

through the 3D model, the monodomain model described by the following reaction-diffusion equation was used:       

$$
(DVVm) = Cm + Iion Iest, (12) Sv dt dVm 1V.C
$$

       where V m is the transmembrane voltage, C m is the specific membrane capacitance (100 pF), I ion is the total ionic current that crosses the membrane, I stim is the stimulus current, S v is the surface/volume ratio and D stands for the conductivity tensor. This equation was numerically solved using the finite element method implemented in the EMOS® software, with a temporal resolution of 0.001 ms.  

# 2.3. Simulation protocol

For single-cell an S1-S1 stimulation protocol was applied, which consists of train of rectangular pulses of 2 ms duration and -2,000 pA to generate action potentials at a base length (BCL) of 1000 ms. The APD at 90% of the repolarization (APDgo) and the different currents were measured on the 1Oth beat. cycle To simulate arrhythmias in the 3D model, an S1-S2-53 stimulation protocol was applied, where SI simulates the sinus rhythm as train of stimuli in the sinoatrial node at a BCL of 500 ms. S2 and S3 simulate two ectopic foci  composed of 6 stimuli each S2 is located at the interatrial septum near the coronary sinus and S3 at the posterior wall of the left atrium; in the base of the right pulmonary   veins. The first S2 and S3 were applied at coupling intervals that generated unidirectional block; with lengths selected such that the second stimulus from each focus also generated a unidirectional block. The simulations ran for 5 seconds. To calculate the number of reentries; reentry is defined as the propagation activity that presents 2 or more consecutive turns. applied cycle Table 1 shows the concentrations   defined for each polluting gas, where the high concentration corresponds to an approximate value of the ICso; the medium is half of the high concentration and the low corresponds to 20% of the high concentration.

  Table 1. Gaseous air pollutants concentrations.  

<table>
  <tr>
    <th>Concentration</th>
    <th>[CO]</th>
    <th>[SO 2 ]</th>
    <th>[NO x ]  </th>
  </tr>
  <tr>
    <td>level Control</td>
    <td> </td>
    <td> </td>
    <td>0 nM</td>
  </tr>
  <tr>
    <td>Low</td>
    <td> </td>
    <td> </td>
    <td>0.002 nM</td>
  </tr>
  <tr>
    <td>Medium</td>
    <td>625 uM</td>
    <td> </td>
    <td>0.005 nM</td>
  </tr>
  <tr>
    <td>High</td>
    <td>1250 μM</td>
    <td> </td>
    <td>0.01 nM</td>
  </tr>
</table>


# 3. Results

The results of single-cell simulations indicate that individual gaseous pollutants exhibit pro-arrhythmic effects in a concentration-dependent manner by altering the action potential. Under healthy conditions, as the CO concentration

Under   healthy   conditions; as the CO concentration increased, a reduction in the magnitude of the maximum peak of the IcaL current was observed and consequently, a reduction in APD9o of 23.6% (Figure IA).

2 90 up to 38.8%, also presenting a loss of the dome of the plateau phase (Figure 1B). The above is a consequence of the alterations in the ionic currents, which include a reduction in the magnitude of the maximum peak of the I CaL current, and an increase in the maximum peaks of the

Na to K1 Finally, as the NO x concentration increased, an increase in the magnitude of the maximum peak of the I Na and I CaL   currents was observed, an effect opposite to what was observed in the other two gases. This generated a more

