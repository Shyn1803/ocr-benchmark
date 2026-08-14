tion of P is left up to the user. Recent work has shown that P must be chosen carefully when one applies modularity maximization to correlation matrices. One possible choice is to set P = I. where I is the identity matrix (MacMahon and Garlaschelli, 2015; Bazzi et al., 2014). This deﬁnition corresponds to a null model where time series are uncorrelated with one another. Thus, community detection amounts to placing as many positive correlation coeﬃcients within each community as possible.To normalize Q so that it is bounded between 0 and 1, we scale Q(t) by 1/2m, where 2m = ij |Wij|.

It is worth noting that the modularity function used here diﬀers from most standard approaches for dealing with signed networks. Traditionally, signed networks are sub-divided into two separate networks: one containing just positive connections:

and

Wij+ =

 

Wij, if Wij > 0 0, otherwise



 

−Wij, if Wij < 0 0, otherwise

Wij− =



Modularity functions are then deﬁned for both the positive and negative components as: Q± = ij[Wij± − Pij±]δ(gi,gj). The choice of how to combine the two components to obtain the total modularity is left up to the user, though a number of weighting schemes have been proposed (G´mez et al., 2009; Rubinov and Sporns, 2011). In general, the total modularity is of the form: Q = c+Q+ − c−Q−, where c± are constants. Thus, modularity maximization for signed networks can be viewed as an attempt to maximize the modularity of positive connections while penalizing negative connections when they fall within

12

