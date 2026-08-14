With b = α+−2, it holds that

α+2 b 2

n log n

exp −

n log n

log n =

- 1

- 2


exp −

√n log n → ∞, for n → ∞.

log n =

Thus, lognn exp{−gn} → ∞ for n → ∞, which is a contradiction to (20), so the statement is true.

- For a kink Now we set α+ = 0, |β+| ≥ δ0 and ψn = n1/3 log1/3 n. Then, it holds

gn =

- 1

- 2


bn2/3 log1/3 n

i=1

β+

i n

2

=

β+2 12n2

(2b3n2 log n + 3b2n4/3 log2/3 n + bn2/3 log1/3 n)

=

β+2 b3 log n 6

+

β+2 b2 log2/3 n 4n2/3

+

β+2 blog1/3 n 12n4/3

.

- For b = β+−2/3, we get


β+2 blog1/3 n

β+2 b2 log2/3 n 4n2/3 −

12n4/3 → 1, for n → ∞, and

exp −

β+2 b3 log n 6

n1/3 log1/3 n

n1/3 log1/3 n

n1/6 log1/3 n

1 6

→ ∞, for n → ∞.

exp −

exp −

log n =

=

Thus, n1/3 log1/3 exp{−gn} → ∞, for n → ∞, which is a contradiction to (20).

<table>
  <tr>
    <td> </td>
  </tr>
</table>


# 6 Discussion

We have studied the online detection of changes in segmented linear models with additive i.i.d. Gaussian noise. Our focus is on the minimax rate optimality in estimating the change point as well as computational and memory efficiency. We introduce the online detector FLOC, which offers several practical advantages, including ease of implementation as well as constant computational and memory complexity for every newly incoming data point — crucial attributes for effective online algorithms. From a statistical perspective, FLOC achieves minimax optimal rates for detecting changes in both function values (i.e. jump) and slopes (i.e. kink). We believe that this is of particular practical benefit, as in many applications the type of change is not always clear beforehand. Notably, our results reveal a phase transition between the jump and kink scenarios, which echo the understanding in the offline setup (Goldenshluger et al., 2006, Frick et al., 2014b, Chen, 2021; see also Table 1). The FLOC detector is specifically designed to achieve asymptotically minimax optimal rates. While the constants involved have not been fully optimized and could likely be improved, we preliminary guidance for tuning FLOC to improve its empirical performance in finite-sample settings. Alternative approaches for parameter tuning could further enhance the performance of FLOC. For instance, theoretical insights, such as the limiting distribution of detection delay provided by Aue et al. (2009), could guide the selection of thresholds to satisfy specified bounds on type II error, and bootstrapping methods, as introduced by Huˇskov´ and Kirch (2012), could be adapted to improve performance, particularly in small-sample scenarios. The current implementation of FLOC relies on sufficient historical data to accurately estimate the pre-change signal. As a practical extension, an adaptive approach could be developed to incrementally update the signal estimate as new observations become available.

Monitoring simultaneously jumps and kinks can enhance detection power compared to conventional approaches that focus solely on mean changes, as demonstrated in our analysis of excess mortality data. However, practitioners should be aware that the Gaussian noise and linear signal assumptions may be strongly violated in certain real-world applications. Enhancing the robustness of FLOC to accommodate broader noise distributions and signal structures, represents a promising direction for future research. For example, in the application

21

