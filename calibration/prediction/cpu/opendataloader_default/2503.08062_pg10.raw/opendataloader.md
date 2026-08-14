in Fig. 9. With the sensing procedures shown in Fig. 4, the sensing peak has a gain proportional to the number of subcarriers N and the number of OFDM symbols M. With the sensing gain, the expected sensing power is increased by 10log10(MN) dB, which brings the sensing power to −20.40 dBm, as shown by the black dashed line in Fig. 9.

-10

Range Profile

-20

Rx Signal power

Sensing Power

-30

Sensing processing gain

Range Profile (dBm)

-40

-50

-60

-70

-80

-90

-100

0 50 100 150 200 250 300 350

Range (meters)

Fig. 9: Sensing profile for a target within the ISI-free range.

Next, we consider the sensing of a single target beyond the ISI-free range, with d = 304.96m, shown in Fig. 10. According to (37). The expected signal power is degraded by the factor (1 − Nτ−NNcp )2, corresponding to 1.65 dB, and the expected ISI and ICI in the range profile is about −109.96 dBm, which is negligible as compared with the noise level. Hence, the observed noise level is similar to the case in Fig. 9, which is PN = −87.17 dBm. On the other hand, the received signal y[n] has the average power -104.97 dBm at d = 304.96m and the sensing power is equivalent to -62.05 dBm after considering sensing processing gain and power degradation due to incomplete OFDM symbol. Fig. 10 shows that the simulation is consistent with the analysis.

-50

Range Profile

Expected noise power

Expected signal Power

-60

Range Profile (dBm)

-70

-80

-90

-100

0 50 100 150 200 250 300 350

Range (meters)

Fig. 10: Sensing profile for a target beyond the ISI-free range.

When multiple targets coexist, as shown in Fig. 11(a), the resultant ISI and ICI from targets beyond the ISI-free range adds up, which may lift the noise level up. However, according to (39), the total ISI/ICI resultant by all the 6 targets beyond

the ISI-free distance is only −98dBm, which slightly lifts the noise level from −87.17dBm to −86.83dBm. In general, when the number of subcarriers is sufficiently large, the impact of ISI and ICI caused by CP limitation is negligible for sensing. According to the specifications in 5G NR, the bandwidth allocated for each user ranges from 34.56MHz to 396MHz when the subcarrier spacing is 120kHz, which corresponds to 288 to 3300 subcarriers. If the number of subcarriers in the simulation reduces from 2048 to 288 in Fig. 11(b), the interference power will increase to −97.86dBm, which is still negligible as compared with the noise level.

Target 8

300

BS

Targets

200

ISI-free distance

Target 4

100

Target 1

Target 7

Target 3

0

Target 2

-100

-200

Target 6

Target 5

-400 -300 -200 -100 0 100 200

(a) Target distribution

-10

<table>
  <tr>
    <td>Range Profile<br><br>Noise+Interference power</td>
  </tr>
</table>


-20

-30

Range Profile (dBm)

-40

-50

-60

-70

-80

-90

-100

0 100 200 300 400 500 600

Range (meters)

(b) Range profile with ISI/ICI

Fig. 11: The sensing of multiple targets.

Consider a sensing detection threshold ρ in (42), the maximum sensing range of an OFDM-ISAC system can be obtained by solving γ(d) = ρ, since the sensing SINR γ(d) is a monotonically decreasing function of d. Let ρ = 10, the maximum sensing range is calculated to be 610m for the default CP length in Table I, which is much larger than the ISI free range 88.44m. Fig. 12 plots the change of the maximum sensing range with CP length. It is observed that if the CP is totally removed, i.e., Tcp = 0, the maximum sensing range can still reach about 590m for M = 14. Besides, the maximum sensing range increases from 610m to 800m when the CP length increases from 0.59µs to 5.3µs, due to the reduced power degradation and ISI/ICI. For d > 800m, the received

