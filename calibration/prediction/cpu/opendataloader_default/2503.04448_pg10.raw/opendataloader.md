Lemma 3. The average number of waiting customers in the polling model under the exhaustive service discipline is given by:

λE[K] 2(1 − ρ)

E[L] =

E[B2] E[B]

α + ρ

E[B]E[K(K − 1)] E[K]

+

. (16)

Proof. We consider the related FCFS system, and denote the variables related to this system with a superscript FCFS. Remark that the waiting time of a tagged customer under the FCFS model is given by the sum of: (i) the travel time, T, to the tagged customer; (ii) the residual service time of the customer in service, if any, at the arrival instant of the tagged customer; (iii) the service time of all waiting customers present at the time of arrival and (iv) the service time of all customers arriving in the same batch, who are served before the tagged customer. Hence:

E[B2] 2E[B]

E WFCFS = E[T] + ρ

E[B]E[K(K − 1)] 2E[K]

+ E LFCFS E[B] +

.

One can now apply Little’s law, E[LFCFS] = λE[K]E[WFCFS] to find a first expression for the mean number of waiting customers in the system. It remains to find the average travel time E[T] to a waiting customer. The travel time under the FCFS service policy is hard to analyse, as this depends on the state of the system at the arrival instant, as well as future arrivals. Instead, we remark that the average travel time to a tagged customer is the same for the FCFS model and polling model. This is due to the fact that the sum of the travel times to all customers is the same. We can therefore focus on the original system to derive E[T]. Recall (1), stating that the server is within a small interval [x,x + dx] with probability [ρπ(x) + 1 − ρ]dx . Therefore, we have:

E[T] = α

1

x=0

ρπ(x) + 1 − ρ]E[d(x,X1)]dx = αρE[d(X2,X1)] + α(1 − ρ)E[d(U,X1)],

where X1,X2 denote the locations of two arbitrary customers and U denotes a Uniform[0,1] random variable. As the average distance from a uniform point on the circle to any point equals 1/2, also E[d(U,X1)] = 1/2 by the independence of X1 and U. Due to the symmetry, we further have E[d(X1,X2)] = E[d(X2,X1)]. Combined with the fact that d(X1,X2) + d(X2,X1) = 1, we find: E[d(X2,X1)] = 1/2. The proof is now finished by substituting E[T] = α/2 in the expression for the waiting time.

<table>
  <tr>
    <td> </td>
  </tr>
</table>


Remark 4. The mean number of waiting customers in the system is not affected by the arrival location distribution. Using Eliazar’s limit argument (Eliazar, 2005), this is a consequence of the pseudo-conservation law for discrete polling models, cf. Equation (3.21) of Boxma (1989), stating that the weighted (by load of queue) sum of expected waiting times is indifferent to the arrival location distribution, λi/( j λj).

# 4.2 Integral equation for spread of customers

We now turn to f(x,y), see (14), describing the average spread of customers on the circle. This characteristic is essential to the mean-value analysis of polling models on a circle and

10

