14 I. Mbouandi Njiasse, F. Ouabo Kamkumo, R. Wunderlich

- 1. Economic costs: At a given time t, individuals who are primarily concerned by social distancing measures are susceptible individuals. Besides asymptomatic people, namely non-detected infectious (I−) and non-detected recovered (R−) are concerned as well since their infection status is not known. Furthermore, since the social distancing measures usually apply even to recovered individuals, we define those who are directly affected by restrictive measures at time n

as Xnwork = Sn +In− +R−n +R+n . Using the normalization, Xnwork = N −In+ −Hn becomes observable and represents the labor force within the population which are not in quarantine (I+). When restrictive measures with strength uL > 0 are implemented, the proportion uLXwork of individuals is unable to fulfill their role in the social economy as a labor force. Consequently, the loss of productivity due to restriction measures will depend on the number of people concerned by the lock-down. In the literature, as in Charpentier et al. [10], Federico et al. [13], Federico and Ferrari [12] a quadratic function or more generally, a convex function is commonly used to describe the socio-economic cost because of its mathematical tractability. Therefore, we define the social distancing running cost at time n by

CL uLnXnWork,0 ,

where the threshold is taken to be 0 which allows to penalize any additional number of people affected by restrictive measures.

- 2. Detection costs: Decision-makers must design detection policies for individuals who are infected and ignore their status, and eventually for those who have recovered from the disease but also ignore their status. In this regard, they must also plan a testing strategy that will provide more information about the current state of the epidemic and reduce some uncertainties about the current and future course of the epidemic. Those who can be tested at a given time n are susceptible S, non-detected infectious I− and non-detected recovered R−. Then, the number of individuals who can be tested is XTest = I− +R− +S. Hence, the running cost for the testing control variable uT is as follows :

CT uTn XnTest,xTest ,

where xTest >0 represents the maximum capacity for testing that can be reached. Note that in a model with constant population size, as in our case, it holds that XTest = N −(I+ +R+ +H) which makes XTest observable.

- 3. Vaccination costs: Large-scale vaccination programs require significant human and financial resources. We assume that this vaccination cost depends on the number of vaccinated persons per unit of time, which is a portion of XTest. Therefore, the running cost corresponding to the vaccination strategy uV is given as


CV uVn XnTest,xVacc .

