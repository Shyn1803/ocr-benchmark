776 A.B. Bjorkegren et al. / Atmospheric Environment 122 (2015) 775e790

transport out of the volume) and fully turbulent conditions with negligible storage. In urban environments during stable atmospheric conditions the DCS term will be non-negligible (Helfter et al., 2011); for example, DCS was found to be ﬁve times the magnitude of the turbulent vertical ﬂux term (FCO2) close to dawn and dusk in suburban Vancouver, Canada (Crawford and Christen, 2014). Other urban studies found DCS to be smaller, but still signiﬁcant, with maximum DCS values 11% and 22% of the magnitude of FCO2 in Edinburgh, Scotland (Nemitz et al. 2002) and Basel, Switzerland (Feigenwinter et al. 2012), respectively. Similarly, in rural environments horizontal advection may be non-negligible (e.g., Aubinet et al., 2003). This paper focuses on the methodological considerations when assessing DCS from a vertical proﬁle in an urban environment. Future manuscripts will address horizontal variation and advection.

Of three studies discussed above (Vancouver, Edinburgh, Basel) with reported urban CO2 storage values, only one (Vancouver, Crawford and Christen, 2014) presented values derived from a dataset of longer than one month; however, both these values and those reported for Edinburgh by Nemitz et al. (2002) were calculated based on the assumption of a constant relation between carbon dioxide concentration ([CO2]) measured above the blending height and the concentration in the street canyon. In contrast, for Basel, Feigenwinter et al. (2012) did not make this assumption and reported DCS calculated from [CO2] at ten levels; however, the results are only for one month (15th June to 15th July 2002). There is therefore scope to improve not only the understanding of the processes affecting CO2 storage over a greater range of meteorological and anthropogenic conditions, but also to develop recommendations for future measurement programmes.

The objective of this paper is to evaluate potential approaches for such studies, illustrated with examples from, and analysis of, high temporal resolution data collected at 10 locations from 6.5 to 46.4 m above ground level between 2011 and 2014 at King's College London, in Central London, UK. The paper is organized as follows. In the rest of this Section 1 we provide a brief background of how CO2 storage is calculated and then (Section 2) a discussion of the methods used in this paper. This is followed by an exploration of the temporal variation of CO2 storage (Section 3) and the relation between measured CO2 storage and anthropogenic and natural factors in a highly urbanised environment (Section 4). The required number and placement of sample points for CO2 storage measurements in a deep urban street canyon is addressed (Section 5) and the effect of sensor response and sampling interval on calculated CO2 storage is tested (Section 6). At the processing stage, three different temporal and spatial interpolation methods are evaluated against measured data (Section 7). Finally, the impact of CO2 storage calculated by two different methods on the turbulent vertical CO2 ﬂux is assessed. The Supplementary material (noted by S.1 to S.9), includes the notation with corresponding units (S.1) used in the text, further information on CO2 storage calculation (S.2), previous CO2 storage studies (S.3), equipment (S.4), meteorological characteristics (S.5), example time series (S.6), variations of CO2 with friction velocity, wind direction and height above ground level (S.7, S.8) and further references (S.9). The online version of this paper provides the ﬁgures in colour.

1.1. Calculation of CO2 storage

There are two main approaches to calculating CO2 storage ﬂux density, i.e., the rate of change of CO2 per unit area below the Eddy Covariance (EC) measurement height. Here they are referred to as the ‘single height’ and the ‘proﬁle’ approaches. For a brief discussion of the theory and some reported results, see Supplementary material S.2 and S.3, respectively. For a more in depth discussion

of the theoretical considerations regarding CO2 storage the reader is referred to Finnigan (2006) and subsequent discussion (Kowalksi, 2008; Finnigan, 2009).

The approach to calculate CO2 storage depends upon the number of vertical locations at which CO2 concentration ([CO2], the symbol [ ] is used to indicate concentration) data are collected. In the ﬁrst approach, ‘single height’ CO2 storage (DCSS) is calculated from [CO2] data at one location, usually by eddy covariance equipment in the inertial sub-layer (Nemitz et al., 2002; Crawford and Christen, 2014). In the second approach, the ‘proﬁle’ method, DCS is calculated from data collected at multiple heights (DCSP). The proﬁle method uses a vertical [CO2] proﬁle at heights zi, which is generally measured by cycling through all the sample locations within a set time period with a data-logger controlled valve array (Xu et al., 1999; Molder€ et al., 2000; Vogt et al., 2006; Hutyra et al., 2008). This cycle period may not be the same as the averaging period used in the DCSP calculation. For example, measurements collected with a sampling interval, ts, of 2 Hz for 75 s at 8 heights, giving a full proﬁle cycle every 10 min, may be used to calculate DCSP with an averaging period (T) of 30 min. The storage is calculated as the sum of the changes in time averaged concentration ([CO2]i) between time t ¼  T/2 and t ¼ T/2 for each location (i) in the proﬁle, weighted by the vertical span, Dzi, over which each proﬁle measurement is considered to be representative and divided by the averaging period (T), which can be expressed as (modiﬁed from Aubinet et al., 2005):

DCSP ¼

1 T X

i

[CO2]i; t¼T

2

[CO2]i; t¼ T

2

Dzi (1)

If the measurements at each height are not made concurrently, [CO2] at each height may ﬁrst be interpolated in time to generate instantaneous proﬁles from which DCSP can be calculated, though this is neglected in some cases (Iwata et al., 2005). The impact of interpolation on calculated DCSP is discussed further in Section 7.

The single height method is a simpliﬁcation of the proﬁle method to one height, which is usually the height of the eddy covariance equipment. The change in [CO2] with time at zh (D[CO2]/Dt) is weighted by the vertical distance from the ground to the measurement point (zh). The single height CO2 storage (DCSS) is given by (modiﬁed from Nemitz et al., 2002):

D[CO2] Dt

zh (2)

DCSS ¼

As the data are continuous, the change in the instantaneous CO2 concentration with time (D[CO2]/Dt) can be used instead of the change in the time averaged CO2 concentration with time ([CO2]/Dt), though it may still be advisable to average in time to reduce measurement noise (Finnigan, 2006).

The DCSS calculation assumes any change in [CO2] below the measurement height results in a change of equivalent magnitude at the measurement height. This assumption appears not to be supported by any evidence in the literature; reported diurnal cycles of CO2 mixing ratios in the roughness sub-layer over both rural (e.g., Xu et al., 1999) and urban (e.g., Lietzke and Vogt, 2013) surfaces are known to vary with height. This problem is particularly acute during periods of low turbulence, such as at night or during cold weather, where measurements above the surface layer may become decoupled from processes near ground level (Helfter et al., 2011).

If temporal variability is large compared to the spatial variability, the single height method may provide a more accurate measure of storage than the proﬁle method as the maximum data availability at each sample location for the latter may be 1/k of the total time

