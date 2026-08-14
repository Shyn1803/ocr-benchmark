28 Florent Ouabo Kamkumo, Ibrahim Mbouandi Njiasse, Ralf Wunderlich

vaccinated compartment, we can document individuals receiving the vaccine, but the timing of immunity loss remains uncertain. To make better use of the available information, we propose to divide each compartment into two distinct groups: an observable part and an unobservable part. The unobservable part, called the hidden compartment with waning immunity, represents those individuals within the recovered and vaccinated compartments whose status cannot be directly observed. On the other hand, for the observable part, we want to divide it into LG sequential or cascade compartments. We assume perfect immunity for a known period of time, which is divided into LG sub-periods. These cascading compartments are used to model the progressive loss of immunity over time for both recovered and vaccinated individuals.

In certain epidemic models with hidden states, some compartments may have one or more observable incoming transitions, while their outgoing transitions may be partially or completely unobservable. As a result, these compartments are treated as hidden. To extract useful information from the observed incoming transitions, the compartment can be divided into a sequence of generic sub-compartments, denoted as Gi, for i = 1,...,LG. Each subcompartment Gi groups individuals based on their time since entering the compartment, effectively tracking their Gi age. The number of sub-compartments LG is typically chosen to match the period during which no outgoing transitions occur, such as the duration of full immunity following recovery or vaccination.

# 4.5.1 Continuous-time Dynamics

Consider the diagram in Figure 4.4 where we assume a random observable inflow into the first generic compartment, G1, and a non-observable outflow from the last compartment, denoted by G−. Between these two compartments, we introduce LG −1 additional compartments, representing different G-ages within the overall compartment G. Additionally, except for the random inflow and outflow, all transitions between compartments are deterministic. Let τ1,...,τLG represent the accounting dates, times at which individuals in each Gi compartment transition to the next. If the time spent in each compartment Gi is ∆τ = τi+1 −τi, the dynamics from G1 to G can be described as in Figure 4.4.

Now, we assume that the state process X can be decomposed into (Xe,G), where Xe con-

![](<2503.07251_pg28_images/imageFile1.png>)

Fig. 4.4: Cascade state illustration with 8 compartment (Gl,l = 1...,LG = 8); observed inflow : random inflow in the compartment 1 (G1) with G-age, 1∆τ, non-observed outflow : random outflow from the compartment G− with G-age, ≥ 9∆τ

Between G1 and G−, only deterministic transition.

tains the de < d traditional states with random inflow or outflow, and G contains the LG new states with deterministic transitions.

Let us consider the microscopic CTMC model given in Equation (2.1) but restrict this point of view to the time intervals [0,T]. To account for transitions between cascade states,

