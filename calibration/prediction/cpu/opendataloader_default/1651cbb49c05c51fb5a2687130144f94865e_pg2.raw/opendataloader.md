𝑒 _   =  .   

, (5)

  .  

𝑒 _   =  .   

, (6)

  .  

In agreement with experimental data [10], the mathematical relationship between the concentration of NOx and the blocking of the current INa is the following:

𝑏  _   =  .  , (7)

where DNO is the NOx concentration in nM. To simulate the effect of the NOx on the ICaL current, the Michaelis-Menten equation was implemented as follows:

𝑒  _    =  .     .   ( ) , (8) where the values 0.59 nM and 0.007 nM are the values of emax and half-maximal effective concentration (EC50) respectively. This equation was fitted using human atrial myocyte data from [11]. The blocking and increasing factors were introduced to the ICaL, INa, IK1, and Ito equations in the cell model, as follows:

𝐼 =  1 − 𝑏  _    (1 − 𝑏 _   )(1 + 𝑒  _   )𝑔 𝑑𝑓𝑓 (𝑉 − 65) , (9)

𝐼 =  1 + 𝑒 _    1 − 𝑏  _   𝑔 𝑚 ℎ𝑗(𝑉 − 𝐸 ) , (10)

𝐼 = (  _    .  ( )  (    ) ) , (10) 𝐼 =  1 + 𝑒 _   𝑔 𝑜𝑎 𝑜𝑖(𝑉 − 𝐸 ) , (11) The modified model was incorporated into a 3D model

of human atria to evaluate the dynamics of propagation.

- 2.2. 3D model of human atrial

A 3D virtual model of human atria was implemented [12]. The model comprises the main anatomical structures, it is composed of 515010 hexahedral elements with a spatial resolution of 300 μm. It includes realistic fiber orientation, electrophysiological heterogeneity, and anisotropy.

To simulate the cardiac action potential propagation through the 3D model, the monodomain model described by the following reaction-diffusion equation was used:

∇. (𝐷∇𝑉 ) = 𝐶 + 𝐼 − 𝐼 , (12)

where Vm is the transmembrane voltage, Cm is the specific membrane capacitance (100 pF), Iion is the total ionic current that crosses the membrane, Istim is the stimulus current, Sv is the surface/volume ratio and D stands for the conductivity tensor. This equation was numerically solved using the finite element method implemented in the EMOS® software, with a temporal resolution of 0.001 ms.

- 2.3. Simulation protocol For single-cell simulations, an S1-S1 stimulation


protocol was applied, which consists of a train of rectangular pulses of 2 ms duration and -2,000 pA to generate action potentials at a base cycle length (BCL) of 1000 ms. The APD at 90% of the repolarization (APD90) and the different currents were measured on the 10th beat.

To simulate arrhythmias in the 3D model, an S1-S2-S3 stimulation protocol was applied, where S1 simulates the sinus rhythm as a train of stimuli applied in the sinoatrial node at a BCL of 500 ms. S2 and S3 simulate two ectopic foci composed of 6 stimuli each. S2 is located at the interatrial septum near the coronary sinus and S3 at the posterior wall of the left atrium, in the base of the right pulmonary veins. The first S2 and S3 were applied at coupling intervals that generated a unidirectional block, with cycle lengths selected such that the second stimulus from each focus also generated a unidirectional block. The simulations ran for 5 seconds. To calculate the number of reentries, reentry is defined as the propagation activity that presents 2 or more consecutive turns.

Table 1 shows the concentrations defined for each polluting gas, where the high concentration corresponds to an approximate value of the IC50, the medium is half of the high concentration and the low corresponds to 20% of the high concentration.

Table 1. Gaseous air pollutants concentrations.

Concentration level

[CO] [SO2] [NOx] Control 0 μM 0 μM 0 nM

Low 250 μM 8 μM 0.002 nM Medium 625 μM 20 μM 0.005 nM

High 1250 μM 40 μM 0.01 nM

3. Results

The results of single-cell simulations indicate that individual gaseous pollutants exhibit pro-arrhythmic effects in a concentration-dependent manner by altering the action potential.

Under healthy conditions, as the CO concentration increased, a reduction in the magnitude of the maximum peak of the ICaL current was observed and consequently, a reduction in APD90 of 23.6% (Figure 1A).

As the SO2 concentration increased, APD90 was reduced up to 38.8%, also presenting a loss of the dome of the plateau phase (Figure 1B). The above is a consequence of the alterations in the ionic currents, which include a reduction in the magnitude of the maximum peak of the ICaL current, and an increase in the maximum peaks of the INa, Ito, and IK1 currents.

Finally, as the NOx concentration increased, an increase in the magnitude of the maximum peak of the INa and ICaL currents was observed, an effect opposite to what was observed in the other two gases. This generated a more

# Page 2

