With b = α − 2 + , it holds that

$$
n exp log n { exp = log n 2 log n log n
$$

Thus, n log n exp {− g n } → ∞ for n → ∞ , which is a contradiction to (20), so the statement is true.

For a kink Now we set 1og1/3 n Then; it holds n1/3 Q+

$$
bn2/3 log1/3 82 In 2 (263n2 +362n4/3 n + bn2/3 n) 12n2 = 8263 4 6 4n2/3 12n4/3 'log 1/3 , log n log n
$$

~2/3 For b = 8+ we get

$$
n exp 4n2/3 12n4/3 log2/3 bl0g1/3
$$

and

$$
exp = exp n 6 n n n1/3 n1/6 n1/3 log1/3 log1/3
$$

Thus,   n 1 / 3   log 1 / 3   exp {− g n } → ∞ , for n → ∞ , which is a contradiction to (20).

# Discussion

We have studied the online detection of changes in segmented linear models with additive i.i.d. Gaussian noise. Our focus is on the minimax rate optimality in estimating the change point as well as computational and memory efficiency. We introduce the online detector FLOC, which offers several practical advantages, including ease of implementation as well as constant computational and memory complexity for every newly incoming data point crucial attributes for effective online algorithms. From a statistical perspective, FLOC achieves minimax optimal rates for detecting changes in both function values (i.e. jump) and slopes (i.e. kink). We believe that this is of particular practical benefit, as in many applications the type of change is not always clear beforehand. Notably, our results reveal a phase transition between the jump and kink scenarios, which echo the understanding in the offline setup (Goldenshluger et al., 2006, Frick et al., 2014b, Chen, 2021; see also Table 1). The FLOC detector is specifically designed to achieve asymptotically minimax optimal rates. While the constants involved have not been fully optimized and could likely be improved, we preliminary guidance for tuning FLOC to improve its empirical performance in finite-sample settings. Alternative approaches for parameter tuning could further enhance the performance of FLOC. For instance, theoretical insights, such as the limiting distribution of detection delay provided by Aue et al. (2009), could guide the selection of thresholds to satisfy specified bounds on type II error, and bootstrapping methods, as introduced by Huˇskov´ and Kirch (2012), could be adapted to improve performance, particularly in small-sample scenarios. The current implementation of FLOC relies on sufficient historical data to accurately estimate the pre-change signal. As a practical extension, an adaptive approach could be developed to incrementally update the signal estimate as new observations become available.

Monitoring simultaneously jumps and kinks can enhance detection power compared to conventional approaches that focus solely on mean changes, as demonstrated in our analysis of excess mortality data. However, practitioners should be aware that the Gaussian noise and linear signal assumptions may be strongly violated in certain real-world applications. Enhancing the robustness of FLOC to accommodate broader noise distributions and signal structures, represents a promising direction for future research. For example, in the application

