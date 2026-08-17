Lemma 3. The average number of waiting customers in the polling model under the exhaustive service discipline is given by:

$$
AE[K] E[B?] E[BJE[K(K = 1)] E[L] (Q + p (16) 2(1 E[B] E[K]
$$

Proof. We consider the related FCFS system, and denote the variables related to this system with a superscript FCFS . Remark that the waiting time of a tagged customer under the FCFS model is given by the sum of: (i) the travel time, T , to the tagged customer; (ii) the residual service time of the customer in service, if any, at the arrival instant of the tagged customer; (iii) the service time of all waiting customers present at the time of arrival and (iv) the service time of all customers arriving in the same batch, who are served before the tagged customer. Hence:

$$
E[B?] E[BJE[K(K 1)] E [wFCFS] E[T] + p +E [LFCFS] E[B] + 2E[B] 2E[K]
$$

One can now apply Little’s law, E [ L FCFS ] = λ E [ K ] E [ W FCFS ] to find a first expression for the mean number of waiting customers in the system. It remains to find the average travel time E [ T ] to a waiting customer.

The travel time under the FCFS service policy is hard to analyse, as this depends on the state of the system at the arrival instant, as well as future arrivals. Instead, we remark that the average travel time to a tagged customer is the same for the FCFS model and polling model. This is due to the fact that the sum of the travel times to all customers is the same. We can therefore focus on the original system to derive E [ T ]. Recall (1), stating that the server is within a small interval [ x,x + d x ] with probability [ ρπ ( x ) + 1 − ρ ]d x . Therefore, we have:

$$

$$

where X 1 ,X 2 denote the locations of two arbitrary customers and U denotes a Uniform[0 , 1] random variable. As the average distance from a uniform point on the circle to any point equals 1 / 2, also E [ d ( U,X 1 )] = 1 / 2 by the independence of X 1 and U . Due to the symmetry, we further have E [ d ( X 1 ,X 2 )] = E [ d ( X 2 ,X 1 )]. Combined with the fact that d ( X 1 ,X 2 ) + d ( X 2 ,X 1 ) = 1, we find: E [ d ( X 2 ,X 1 )] = 1 / 2. The proof is now finished by substituting E [ T ] = α/ 2 in the expression for the waiting time.

Remark 4. The mean number of waiting customers in the system is not affected by the arrival location distribution. Using Eliazar’s limit argument (Eliazar, 2005), this is a consequence of the pseudo-conservation law for discrete polling models, cf. Equation (3.21) of Boxma (1989), stating that the weighted (by load of queue) sum of expected waiting times is indifferent to the arrival location distribution, λ i / (   j λ j ) .

# 4.2

This characteristic is essential to the mean-value analysis of polling models on a circle and

