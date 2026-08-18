<table>
  <tr>
    <th> </th>
    <th>the time the kth packet on session 1 begins service under the S server</th>
  </tr>
  <tr>
    <td> </td>
    <td>the time the kth packet on session 1 departs_under_the s server</td>
  </tr>
  <tr>
    <td>Bs</td>
    <td>departs s server</td>
  </tr>
  <tr>
    <td>Qi s</td>
    <td>the queue size of session at time under the s server</td>
  </tr>
  <tr>
    <td>Wis</td>
    <td>the amount of work received by session during the time interval [t1 , t 2 under the S server</td>
  </tr>
  <tr>
    <td> </td>
    <td>size of the kth packet on session i in number of bits</td>
  </tr>
  <tr>
    <td>Limas</td>
    <td>maximum packet size of session</td>
  </tr>
  <tr>
    <td>Lmar</td>
    <td>maximum packet size among aTTsessions</td>
  </tr>
  <tr>
    <td> </td>
    <td>Tink speed</td>
  </tr>
  <tr>
    <td> </td>
    <td>guaranteed rate Tor session</td>
  </tr>
</table>


Table 1: Notation Used in this Paper

bucket   constrained at the source He also proposed packet   approximation algorithm for GPS which he called  Packet-by-Packet   Generalized Processor SharOI PGPS. It turns out that PGPS is identical to the weighted version of Fair Queueing OI WFQ. Parekh has established several important relationships between fluid   GPS system and it's corresponding packet  WFQ system: ing

in terms of delay packet . will finish service in WFQ system later than in the corresponding GPS system by 1o more than the transmission time of one maximum size packet;

2 . in terms of total number of bits served for each session WFQ system does not fall behind a corresponding GPS system by more than one maximum size packet .

The above result can easily be mis-interpreted to say that the packet WFQ discipline and the fluid GPS discipline provide almost identical service except for difference of one packet ; Contrary to this popular (but incorrect we will demonstrate that there could be large discrepancies between the services provided by WFQ and GPS. In fact, what has been proven is size packet. However WFQ can be far ahead of GPS in terms of number of bits served for a session_ Since many congestion control algorithms_ [9, 14] were designed with the  assumption that WFQ will provide almost identical service with GPS, large discrepancies between the two disciplines and the lack of knowledge that such   discrepancies exist will result in unstable and less eflicient  network control algorithms .

To overcome the limitation of WFQ, we propose new better packet approximation algorithm of GPS called Worst-case Fair Weighted Fair Queueing OI Q We show that WF? provides almost iden tical service to GPS with a maximum difference of one packet size; and it shares both the bounded-delay and fairness properties of GPS. and WF?

# 2 GPS and WFQ

In this section; we first   define GPS and its most popular packet  approximation algorithm WFQ, then describe the important  difference between these two disciplines .

A GPS server serving N sessions is characterized by N positive real numbers; 01 , 02, 0N The server operates at a fixed rate and IS work-conserving traffic served in the interval [t1 , t2], then a GPS server is defined as one for which

$$
2 j = 1,2, Wj (t1 , t2) 0j
$$

holds for any session that is backlogged throughout From the definition, it immediately follows that if 'BGPs(-) the set of backlogged sessions at time T remains unchanged during any time interval [t1 , t2], the service rate of session during the interval will be exactly

$$
= (2) 0j ZjeBGrs(t)
$$

(t1 ) is a subset of all the sessions at the server, it is easy to see that BGPs(

holds where

$$
(3)
$$

$$
Ti =
$$

Therefore, session i is guaranteed minimum service rate of ri_during any interval  when it is backlogged . Let   the time interval length go to zero we the instantaneous service rate of the session_ get

Notice that GPS is an idealized server that does not transmit packets as entities. It assumes that the server can serve all backlogged sessions simultaneously and that the traffic is infnitely divisible. In more realistic packet   system; only one session can receive service at a time and an entire packet_must be served before another packet can be served There are differ ent ways of emulating GPS service in a packet system The most popular one is the Weighted Fair Queueing discipline (WFQ) [4], also known as Packet Generalized Processor Sharing or PGPS [13].

1 A server is work-conserving if it is never idle whenever there are packets to be transmitted. Otherwise; it is non-workconserving.

