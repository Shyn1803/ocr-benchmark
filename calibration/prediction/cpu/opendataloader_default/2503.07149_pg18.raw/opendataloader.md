REC, both entities stop charging and start exporting their energy production once the ﬁrst DR request horizon begins (see Fig. 3). During this period, Entity 1 exports 294 kWh, while Entity 2 exports 126 kWh. After the ﬁrst DR request ends, entities resume charging due to low energy price and later export to the grid during the period with highest energy price. Between 15:15 and 17:00 both entities start charging again, so that their storage systems can be discharged during the second DR request, as expected. During the second DR request, this strategy enables Entities 1 and 2 to provide 729 kWh and 318 kWh, respectively.

From Fig. 4 it is apparent that both δ1 and δ2 are higher when the objective function is set to HE compared to HM. This result is expected, as HE is designed to maximize the total revenue for the entities, whereas HM focuses on maximizing the revenue of the REC manager, which naturally leads to lower extra proﬁts for the entities. Fig. 4 also demonstrates a fair redistribution of rewards among the entities, such that the additional proﬁt be proportional to their respective individual revenuse when operating independently, i.e., outside the REC. This ensures that the additional proﬁts δ1 and δ2 are allocated equitably, reﬂecting the contribution provided by each entity to the REC. Notice that, when the objective function HM is used, there are some days such that δ1 = δ2 = 0, that is, the proﬁt of the entities joining the REC equals the proﬁt they would gain if acting individually outside the REC.

Regarding the DR rewards assigned to the entities, Fig. 5 shows that when optimizing HM the total community reward is no less than that obtained by using HE, as expected. However, even if optimizing HM, the REC is in general unable to provide the upper DR request energy bounds (i.e., γ1∗ + γ2∗ < γ1 + γ2). Clearly, the sum of the rewards assigned to the two entities is less than the total reward received by the community, since a fraction of it is retained by the REC manager according to (30).

![](<2503.07149_pg18_images/imageFile1.png>)

![](<2503.07149_pg18_images/imageFile2.png>)

The sensitivity of the proposed method with respect to the DR reward bound γj is explored in Table 4. When the DR reward bound γj is increased from 40 to 100e, the achieved DR rewards γ1∗ + γ2∗ under both objectives HE and HM are the same. This basically means that the DR reward is large enough to make fulﬁllment of DR requests always advantageous regardless of all costs and energy losses arising when operating storage. So, any further increase in γj will provide the same BESS control commands and consequently the same amount of energy injected into the grid.

![](<2503.07149_pg18_images/imageFile3.png>)

![](<2503.07149_pg18_images/imageFile4.png>)

![](<2503.07149_pg18_images/imageFile5.png>)

Concerning Example 2, in Fig. 7 one can observe that during the DR periods entities discharge their storage systems to increase the injected energy into the grid. Thanks to this operation, the REC receives a monetary reward which can be shared among entities, allowing them to substantially increase their proﬁt compared to their baseline, see Tables 6 and 7. Regarding the two considered objective functions HE and HM, they yield behaviors similar to those in Example 1, favouring the entity proﬁt and the total DR reward, respectively.

18

