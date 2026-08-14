# 11.9.9 Starting a remote copy Consistency Group

When a remote copy consistency group is created, the remote copy process can be started, for all the relationships that are part of the consistency groups.

To start a consistency group, open the Copy Services → Remote Copy panel, right-click the consistency group to be started, and select Start, as shown in Figure 11-140.

<table>
  <tr>
    <td>![](<ab4eb9e6b71229e3b7de4d76ffe161c18dcf548d1717a4ff6e33b03e13ab3c11_images/imageFile1.png>)</td>
  </tr>
</table>


- Figure 11-140 Starting a remote copy Consistency Group

11.9.10 Switching a relationship copy direction

When a remote copy relationship is in the Consistent synchronized state, the copy direction for the relationship can be changed. Only relationships that are not a member of a Consistency Group, or the only relationship in a Consistency Group, can be switched. In any other case, consider switching the Consistency Group instead.

To switch the direction of a remote copy relationship, complete the following steps:

- 1. Open the Copy Services → → Remote Copy panel.
- 2. Right-click the relationship to be switched and select Switch, as shown in Figure 11-141.


- Figure 11-141 Switching remote copy relationship direction


Important: When the copy direction is switched, it is crucial that no outstanding I/O exists to the volume that changes from primary to secondary because all of the I/O is inhibited to that volume when it becomes the secondary. Therefore, careful planning is required before you switch the copy direction for a relationship.

<table>
  <tr>
    <td>![](<ab4eb9e6b71229e3b7de4d76ffe161c18dcf548d1717a4ff6e33b03e13ab3c11_images/imageFile2.png>)</td>
  </tr>
</table>


Chapter 11. Advanced Copy Services 591

