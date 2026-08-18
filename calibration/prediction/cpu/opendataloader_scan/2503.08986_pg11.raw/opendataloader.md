![](<2503.08986_pg11_images/imageFile1.png>)

2.5

1

1.5

1

Phase errors, FAS

Phase errors; FAS,

Ideal phase, FAS,

|

Ideal phase, FAS, t

Phase errors, TAS, r

0.5

Phase errors, TAS, t

Ideal phase, TAS,

Ideal phase, TAS,

Simulation

20

30

40

10

average SNR

(dB)

![](<2503.08986_pg11_images/imageFile2.png>)

2.5

4

J

1.5

FAS, r, K = 30

1

FAS, r, K = 80

FAS. t,K = 80

TAS. r,K = 30

8

TAS, t,K = 30

0.5

TAS, r, K = 50

TAS

t,K = 50

1

TAS, r, K = 80

TAS, t,K = 80

Simulation

10

20

30

40

(dB)

average SNR

Fig. 8. The sum AC results of FAS-assisted STAR-RIS RSMA versus the average SNR γ with phase errors and ideal phases for K = 30 .

Fig. 9. The sum AC results of FAS-assisted STAR-RIS RSMA versus the average SNR γ with phase errors for different numbers of STAR-RIS elements K .

especially in channels with rich scattering.

The results in Fig. 8 study the impact of phase errors on the sum AC, C sum ,u = C c ,u + C p ,u . First of all, as expected, a small gap between the simulation results and the theoretical predictions is observed. This discrepancy arises from the use of a heuristic technique to approximate the expectation of the maximum of N u correlated Gamma RVs, as discussed in Remark 2 . The heuristic method, based on simplifying assumptions, provides a computationally efficient approximation that captures the essential behavior of the system, especially in cases involving moderate correlations. Despite the gap, the results indicate that this approach performs well across a range of scenarios, making it a useful approximation for evaluating the AC performance under correlated conditions. For both FAS and TAS, we see that as γ increases, the sum AC initially improves but eventually saturates. This occurs because in the RSMA scheme, rate splitting effectively manages interference and optimizes power allocation at moderate SNR levels. As γ grows, the SINR expressions in ( 8 ) and ( 11 ) converge to deterministic values, depending on the power allocation factors for the common and private streams. Beyond this threshold, further increases in SNR do not significantly improve the sum AC, resulting in saturation. Additionally, the case with ideal phase results in a higher level of sum AC compared to the scenario with phase errors. This is because with ideal phase, STAR-RIS can perfectly align the transmitted signals with the desired reflection coefficients, thereby maximizing the signal power at the receiver and minimizing interference. In contrast, phase errors introduce misalignment between the transmitter and STAR-RIS, leading to suboptimal signal reflection and increased interference. As a result, the effective channel gains are reduced in the presence of phase errors, causing a degradation in the sum AC. Noteworthy, the asymptotic behavior for the FAS and TAS schemes is independent of the phase errors, so does the performance degradation because the phase

# V. C ONCLUSION

This paper presented a comprehensive investigation of FASassisted STAR-RIS communication systems employing RSMA signaling, with a particular focus on the impact of phase errors under the ES protocol. By modeling the phase errors with a generic distribution and deriving the equivalent channel gain characterized by the multivariate t -distribution, we provided a realistic and robust analysis of the system performance. Compact analytical expressions for key performance metrics, such as outage OP and AC were derived, with the latter being

