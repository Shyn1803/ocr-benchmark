that 𝐼𝑡 is surjective. Suppose 𝑍∈𝐿2(𝑌,𝑡,𝑑′) so that ‖𝑍𝑛−𝑍‖2 →0 for some 𝑍𝑛 ∈ (𝑌,𝑡,𝑑′). By isometry we conclude that 𝐻𝑛 ∶=𝐼𝑡−1(𝑍𝑛) is a Cauchy sequence converging to some 𝐻∈𝐿2(𝑋,𝑡,𝑑′). Finally ‖𝐼𝑡𝐻−𝑍‖= lim𝑛→∞ ‖𝑍𝑛 −𝑍‖= 0 and therefore 𝐼𝑡(𝐻) =𝑍.

Equation (3.11) is evident in the case that 𝛾 is a simple function. For general 𝛾∈𝐿𝑡(𝑋,𝑑′), choose a sequence of simple 𝛾(𝑛) with ‖𝛾(𝑛)−𝛾‖2 →0. By (3.9) and Ito’s isometry we have¯

𝑡

𝑡

𝑡

𝑡

→0

𝛾(𝑛)(𝑠) d𝑌(𝑠) − ∫

𝛾(𝑠) d𝑌(𝑠)

→0,

𝛾(𝑛)(𝑠) d𝑋(𝑠) − ∫

𝛾(𝑠) d𝑋(𝑠)

‖∫

‖∫

‖2

‖2

0

0

0

0

as 𝑛→∞. The claim then follows because the continuity of the operator 𝐼𝑡 yields

𝑡

𝑡

𝑡

𝑡

𝐼𝑡 ∫

𝛾(𝑠) d𝑋(𝑠) = lim

𝐼𝑡 ∫

𝛾(𝑛)(𝑠) d𝑋(𝑠) = lim 𝑛→∞∫

𝛾(𝑛)(𝑠) d𝑌(𝑠) = ∫

𝛾(𝑠) d𝑌(𝑠).

𝑛→∞

0

0

0

0

<table>
  <tr>
    <td> </td>
  </tr>
</table>


# 4 Filtering, smoothing, and prediction

This section is devoted to optimal linear filtering, prediction and smoothing of partially observed polynomial processes. We let either 𝐼∶=ℕ or 𝐼∶=ℝ+ and fix a probability space (Ω,F,(F𝑡)𝑡∈𝐼,ℙ) as well as an ℝ𝑑-valued adapted process 𝑋= (𝑋(𝑡))𝑡∈𝐼. If 𝐼=ℝ+, we assume (F𝑡)𝑡∈𝐼 to be right-continuous. Suppose that the components 𝑋𝑚+1(𝑡),…,𝑋𝑑(𝑡) are observable whereas 𝑋1(𝑡),…,𝑋𝑚(𝑡) are not. We let the subscript o stand for the observable part of a vector 𝑥∈ℝ𝑑 and let 𝐻∶= (𝛿𝑚+𝑖,𝑗)𝑖=1,…,𝑑−𝑚;𝑗=1,…,𝑑, i.e. 𝑥o ∶=𝐻𝑥= (𝑥𝑚+1,…,𝑥𝑑). For Σ ∈ℝ𝑑×𝑑 we set Σ∶,o ∶= Σ𝐻⊤ = Σ1∶𝑑,𝑚+1∶𝑑, Σo,∶ ∶=𝐻Σ = Σ𝑚+1∶𝑑,1∶𝑑 as well as Σo ∶=𝐻Σ𝐻⊤ = Σ𝑚+1∶𝑑,𝑚+1∶𝑑. The subscript u standing for the unobservable part of a vector is treated in the same manner.

We suppose that 𝔼(‖𝑋(𝑡)‖2)<∞ for 𝑡∈𝐼 and consider the following general filtering problem for fixed 𝑡∈𝐼. The goal is to minimise the mean square error 𝔼(‖𝑋(𝑡) −𝑌‖2) over all random variables 𝑌 that are measurable with respect to the observable information

{

}

G𝑡 ∶=𝜎(

𝑋o(𝑠) ∶𝑠∈𝐼, 𝑠≤𝑡

). (4.1)

We call the minimiser of (4.1) the optimal filter for . Regardless of any specific model the optimal filter is then given by the conditional mean 𝑋(𝑡,𝑡)̂ ∶=𝔼(𝑋(𝑡)|G𝑡).

## 4.1 Discrete-time linear filtering problems

Let 𝐼=ℕ. For Gaussian state space models, the optimal filter can be computed recursively:

Proposition 4.1 (Kálmán filter). Suppose that 𝑋 is a linear Gaussian state space model as in Definition 3.1 and set 𝐶(𝑡) ∶=𝐵(𝑡)𝐵(𝑡)⊤. Let 𝑋(0,−1)̂ ∶=𝔼(𝑋(0)), Σ(0,−1)̂ ∶= Cov(𝑋(0)) and

𝑋(𝑡+̂ 1,𝑡 𝑎(𝑡+ 1) +𝐴(𝑡+ 1)𝑋(𝑡,𝑡),̂

𝑋(𝑡,𝑡̂ 𝑋(𝑡,𝑡−̂ 1) + Σ̂∶,o(𝑡,𝑡− 1)Σ̂o(𝑡,𝑡− 1)+(𝑋o(𝑡) − 𝑋̂o(𝑡,𝑡− 1)), Σ(𝑡+̂ 1,𝑡 𝐴(𝑡+ 1)Σ(𝑡,𝑡)𝐴(𝑡+̂ 1)⊤ +𝐶(𝑡+ 1),

Σ(𝑡,𝑡)̂ ∶= Σ(𝑡,𝑡−̂ 1) − Σ̂∶,o(𝑡,𝑡− 1)Σ̂o(𝑡,𝑡− 1)+Σ̂o,∶(𝑡,𝑡− 1)

16

