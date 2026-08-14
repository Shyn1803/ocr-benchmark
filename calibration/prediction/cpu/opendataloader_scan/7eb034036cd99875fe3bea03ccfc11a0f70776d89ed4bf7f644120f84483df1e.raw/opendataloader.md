A thin-provisioned volume feature that is called zero detect provides clients with the ability to reclaim unused allocated disk space (zeros) when they are converting a fully allocated volume to a thin-provisioned volume by using volume mirroring.

# 3.12 Host attachment planning

The typical FC host attachment to the Storwize V7000 is done through SAN fabric. However, the system allows direct attachment connectivity between its 8 Gb or 16 Gb Fibre Channel ports and host ports. No special configuration is required for host systems that are using this configuration. However, the maximum number of directly attached hosts is severely limited by the number of FC ports on Storwize V7000’s nodes.

The Storwize V7000 imposes no particular limit on the distance between the Storwize V7000 nodes and host servers. However, for host attachment, the Storwize V7000 supports up to three ISL hops in the fabric. This capacity means that the server to the Storwize V7000 can be separated by up to five FC links, four of which can be 10 km long (6.2 miles) if long wave Small Form-factor Pluggables (SFPs) are used.

Figure 3-9 shows an example of a supported configuration with Storwize V7000 nodes using shortwave SFPs.

![](<7eb034036cd99875fe3bea03ccfc11a0f70776d89ed4bf7f644120f84483df1e_images/imageFile1.png>)

Host

Host

2

10 km

10 km

10 km

10 km

10 km

Fibre

Fibre

Fibre

Fibre

Channel

Channel

Channei

Channei

Switch

Switch

Switch

Switch

up to

300 m

Long-wave SFP

Short-wave SFP

Figure 3-9 Example of host connectivity

In Figure 3-9, the optical distance between Storwize V7000 Node 1 and Host 2 is slightly over 40 km (24.85 miles).

To avoid latencies that lead to degraded performance, avoid ISL hops whenever possible. In an optimal setup, the servers connect to the same SAN switch as the Storwize V7000 nodes.

Note: Before attaching host systems to Storwize V7000, review the Configuration Limits and Restrictions for the IBM System Storage Storwize V7000 at this IBM Support web page .

