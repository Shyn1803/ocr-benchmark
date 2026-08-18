![](<2503.05886_pg3_images/imageFile1.png>)

hidden realizations performed by the assistant

pre-select

post-select

reported initial state

reported final state

()Ltkj

Likj

i,k,j

Po

FIG. 1. Quantum analog of Schro¨dinger’s 1931 bridge problem.

initial state | x i 0 ⟩ is subjected to the prescribed Markovian dynamics (4). Finally, our assistant performs the final projective measurement with respect to states {| y j 1 ⟩} , leading to a certain final state | y j 1 ⟩ . In other words, our assistant realizes an experiment in which the states are preand post-selected . After a large number of such experiments, say N , our

assistant reports to us the fraction ˜ α i of experiments that started with state | x i 0 ⟩ and the fraction ˜ β j of experiments that ended on state | y j 1 ⟩ , without telling us which combination of states was chosen in each realization. That is, without reporting the joint distribution ˜ p ij . Thus, from our point of view, the experiment starts and concludes with the system in the mixed states

$$
Ão = and =
$$

respectively, which do not align with our expectation ρ 0 and ρ 1 . Moreover, the reported states are such that

$$
i,k,j
$$

See Figure 1 for a schematic representation of the experiment.

The discrepancy between the expected and the reported initial and final states may be due to large deviations, i.e., obtaining an unlikely ensemble from a collection of measurements due the finite size of the experimental record, or due to preand post-selection, where our assistant might have chosen a sub-ensemble of realizations to cook up some desired ˜ α i and ˜ β j probabilities. Either way, in the spirit of Schr¨dinger’s original gedanken experiment, we pose the following question: what is the most likely joint probability ˜ p ij that led to the outcomes ˜ ρ 0 and ˜ ρ 1 ? In other words, if the outcomes were postselected, what is the most likely way this post-selection was achieved?

# B. A large deviations solution

The question raised above reduces to a classical deviations problem of the same nature as the one that large quantify the likelihood of unexpected outcomes through Sanov's theorem; which states that the probability P of drawing an atypical distribution from a finite collection of N realizations decays exponentially as N Specifi cally;

$$
~IN P ~ e
$$

where the decay rate is given by the large deviations rate function I that quantifies the distance between P and the typical probability distribution. Thereby, the most likely atypical distribution that is consistent with given outcomes is the one that minimizes the rate function.

Although the experiment we consider involves a quantum evolution, the measurement at the two sites where preand post-selection takes place, render the probabilistic model of the experimental setting classical. As a result, the rate function is the relative entropy

$$
Ẽij Pij i,j log
$$

between the atypical observed distribution ˜ p ij , and the expected (i.e., typical) one p ij , which would have been obtained if no rare events or selection took place.

Hence; we now probability distribution between initial and final states with the observation record,

$$
= and Ẽij Bj(8)
$$

This is nothing but a classical one-time-step Schr¨dinger bridge problem, to find the minimizer

$$
arg min so that (8 9 Pij i,j log
$$

To solve this problem, we consider the augmented Lagrangian

$$
Ẽij i,j Pij log
$$

variation with respect to Ẽij to zero, we obtain that the

