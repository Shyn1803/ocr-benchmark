![](<2503.05886_pg3_images/imageFile1.png>)

FIG. 1. Quantum analog of Schro¨dinger’s 1931 bridge problem.

# 3

initial state |xi0⟩ is subjected to the prescribed Markovian dynamics (4). Finally, our assistant performs the fi-

nal projective measurement with respect to states {|y1j⟩}, leading to a certain final state |y1j⟩. In other words, our assistant realizes an experiment in which the states are pre- and post-selected.

After a large number of such experiments, say N, our assistant reports to us the fraction α˜i of experiments that started with state |xi0⟩ and the fraction β˜j of experiments that ended on state |y1j⟩, without telling us which combination of states was chosen in each realization. That is, without reporting the joint distribution p˜ij. Thus, from our point of view, the experiment starts and concludes with the system in the mixed states

ρ˜0 =

i

α˜i|xi0⟩⟨xi0| and ρ˜1 =

j

β˜j|y1j⟩⟨y1j|, (7)

respectively, which do not align with our expectation ρ0 and ρ1. Moreover, the reported states are such that

Likj(1,0)˜ρ0Likj(1,0)†.

ρ˜1 ̸=

i,k,j

See Figure 1 for a schematic representation of the experiment.

The discrepancy between the expected and the reported initial and final states may be due to large deviations, i.e., obtaining an unlikely ensemble from a collection of measurements due the finite size of the experimental record, or due to pre- and post-selection, where our assistant might have chosen a sub-ensemble of realizations to cook up some desired α˜i and β˜j probabilities. Either way, in the spirit of Schr¨dinger’s original gedanken experiment, we pose the following question: what is the most likely joint probability p˜ij that led to the outcomes ρ˜0 and ρ˜1? In other words, if the outcomes were postselected, what is the most likely way this post-selection was achieved?

B. A large deviations solution

The question raised above reduces to a classical large deviations problem of the same nature as the one that Schr¨dinger answered in [1]. In modern terms, we seek to

quantify the likelihood of unexpected outcomes through Sanov’s theorem, which states that the probability P of drawing an atypical distribution from a finite collection of N realizations decays exponentially as N → ∞. Specifically,

P ∼ e−IN,

where the decay rate is given by the large deviations rate function I that quantifies the distance between P and the typical probability distribution. Thereby, the most likely atypical distribution that is consistent with given outcomes is the one that minimizes the rate function.

Although the experiment we consider involves a quantum evolution, the measurement at the two sites where pre- and post-selection takes place, render the probabilistic model of the experimental setting classical. As a result, the rate function is the relative entropy

p˜ij pij

p˜ij log

,

i,j

between the atypical observed distribution p˜ij, and the expected (i.e., typical) one pij, which would have been obtained if no rare events or selection took place.

Hence, we now seek the most likely (classical) joint probability distribution p˜ij between initial and final states |xi0⟩ and |y1j⟩ that is in agreement with the observation record, i.e.,

j

p˜ij = α˜i and

i

p˜ij = β˜j. (8)

This is nothing but a classical one-time-step Schr¨dinger bridge problem, to find the minimizer

arg min

p˜ij

i,j

p˜ij pij

p˜ij log

so that (8) holds. (9)

To solve this problem, we consider the augmented Lagrangian

L =

i,j

p˜ij pij

p ˜ij log

+ λi(˜pij − α˜i) + γj(˜pij − β˜j) ,

where λi and γj are Lagrange multipliers. Setting its first variation with respect to p˜ij to zero, we obtain that the

