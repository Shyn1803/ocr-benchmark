interspike interval σ as

$$
N N (zk V = zk (79) N k=l N k=l ~v)2
$$

The normalized standard deviation of the interspike interval is then simply

$$
80)
$$

If a spike train is exactly periodic then ¯ σ = 0. If it is instead a Poisson process, then ¯ σ = 1. We have computed 1 / ¯ σ for Y ⋆ ( t ) at various values of κ . The results are shown in Fig. 8 as purple dots [joined for ease of visualization, and colored differently for (a), (b), and (c)]. The data indicates a resonance effect of Υ( t ) on Y ⋆ ( t ). This refers to the existence of an optimal value of κ at which Y ⋆ ( t ) oscillates most regularly. The same can also be seen in X ⋆ ( t ) (the results for which are not shown). Starting at point (a) ( κ = 0 . 050), the spike train can be seen to be more and more periodic as κ increases, until we reach (b) ( κ = 0 . 243) when the period is optimized. Adding more noise thereafter only reduces the regularity of the spike train, which can be seen to level off around point (c) ( κ = 1 . 178).

The manner in which Y ⋆ ( t ) changes with noise is reminiscent of coherence resonance in excitable systems [ 23 ]. The effect is well known for classical systems [ 164 – 168 ], but has appeared only relatively recently in quantum systems [ 121 , 169 ]. A notable difference between our results in Fig. 8 and coherence resonance is that we have not operated the noise-free quantum Fitzhugh–Nagumo system in the excitable regime (defined classically by having a stable fixed point in the system while being close to the supercritical Hopf bifurcation). If we define quantum excitability based on the classical theory, then the excitable regime of the noise-free quantum Fitzhugh– Nagumo model should look something like Fig. 7 (a). We have in fact calculated ¯ σ ( κ ) using such a state for W Υ ( x,y, 0). The resonance effect of Υ( t ) on Y ⋆ ( t ) is retained, i.e. we get a similar ¯ σ − 1 ( κ ) as in Fig. 8 , but the mode of W Υ ( x,y,t ) is also a lot noisier for such a W Υ ( x,y, 0), so the spikes are no longer apparent. A more careful study is required to understand the noise-driven quantum Fitzhugh–Nagumo model in this regime. This is beyond the scope of this paper as our goal here is simply to illustrate the range of systems amenable to cascade quantization. There is however a separate note to this end that is worth mentioning, and that is—excitable systems come in different flavors, depending on the bifurcation that gives rise to their excitability. In the case of the Fitzhugh–Nagumo model, it is a supercritical Hopf bifurcation that facilitates its excitability. Another commonly used mechanism is the infinite-period bifurcation, an example of which was considered in Sec. IVE (and recall that this is the same as a saddle-node bifurcation on an invariant circle). In this case, ( 59 ) and ( 60 ) become

# 2. Average effect of noise

We can also get an understanding of how Υ( t ) affects the system by considering its effect on average. Suppose we are interested in how a function s (ˆ a, ˆ a † ) might change. Then in principle we could use ( 75 ) to obtain many runs of ⟨ s (ˆ a, ˆ a † ) ⟩ Υ = Tr[ s (ˆ a, ˆ a † ) ρ Υ ] and calculate their ensemble average E[ ⟨ s (ˆ a, ˆ a † ) ⟩ Υ ]. This approach works, but is rather indirect. It does not provide a simple way to capture the average effect of Υ on the system. Here we derive an equation that propagates the quantum state of the noise-driven system while averaging over Υ. That is, we seek the evolution of a state ρ such that, for any s (ˆ a, ˆ a † ) and any time,

$$
Ir{s(â,ât) p} = E[(s(â,ât))r] (81)
$$

Such a state can be found by noting that

$$
E[(s(â,ât))r] = dv gr(v,t) Tr [s(â,ât) pr(t)] = Tr | s(â,â*) (t) | (82)
$$

bility that T(t) e [v,v + dv] Comparing (81) to (82), we see that

$$
p(t) = Elpr(t)] = (83)
$$

Equation ( 83 ) implies that an equation of motion for ρ ( t ) can be obtained by averaging ( 75 ). One way to calculate the ensemble average of ( 75 ) is to convert it to its Itˆ

$$
K2 dpr Lo pr dt + 2 D[â + â*Jpr dt +i [â + ât, pr] dW (84) V2
$$

As ( 84 ) is now an Itˆ stochastic differential equation, it obeys Itˆ calculus for which dW has zero mean and

