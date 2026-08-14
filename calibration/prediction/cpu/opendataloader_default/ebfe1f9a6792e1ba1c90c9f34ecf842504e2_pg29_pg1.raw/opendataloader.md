29

application sets respectively. In particular, employing a reduced set of templates for template selection leads to an average area reduction of over 27%.

Finally, Table 3 reports on the efficiency that is obtained when the reduced set of templates and the full set of templates are used for template selection. The efficiency is calculated as shown in (8), where ESCS is the Effective Software Cycle Savings which accounts for the hardware execution delay of the custom instructions pi (TC(pi)), where i = 1, … , n, and is calculated as shown in (9). TC(pi) is obtained by calculating the number of clusters in the critical path of the custom instructions. For example, TC of the custom instruction in Figure 4(a) is 2. Note that we have assumed that the delay of each cluster is equivalent to two software clock cycle executions. This is a reasonable assumption as the FPGA logic can generally execute at a significantly higher clock frequency than a commercially available soft processor core which is implemented on the same fabric [55].

ESCS Efficiency = (8)

K

ARFU

n

( ) ( ( ) 2 ( )) (9)

# ∑

ESCS F pi TSW pi TC pi

= × − ⋅

i

1

=

<table>
  <tr>
    <td>Domain</td>
    <td>Reduced Templates ESCS Area Efficiency<br><br></td>
    <td>Full Templates ESCS Area Efficiency</td>
  </tr>
  <tr>
    <td>AutomotiveIndustrial Image<br><br>Network Security Telecomm Generic</td>
    <td>14664576 45182539.6 0.325 1538018 364687641.1 0.004 102859967 64546485.15 1.594 19207719 142002267.3 0.135 5823638 41955215.34 0.139 146359636 635782878.68 0.230<br><br></td>
    <td>14814576 64546485.15 0.230 1559449 416324829.2 0.004 129603704 80683106.43 1.606 22467162 264640589.1 0.085 6873517 71001133.66 0.097 176180091 761648524.7 0.231</td>
  </tr>
</table>


Table 3: Comparing the efficiency when reduced set and full set of templates are used for template selection

It can be observed in Table 3 that the efficiency of the proposed method is higher than the case when the full set of templates is used in a number of application domains (with comparable results in the remaining domains). In particular, the average efficiency gain when a reduced set of templates is used is over 25%.

