The above substitution emphasizes the fact that we are now dealing directly with the exponential distribution of the squared magnitudes 𝑋1 and 𝑋2, rather than with the complex fields 𝑍1 and 𝑍2 because 𝜎2 and 𝜌 are, respectively, the variance and the correlation coefficient of 𝑋1 and 𝑋2, as shown in the previous section. We now seek to extend this result to the sum of 𝑘 independent correlated exponential variables, leading to correlated Gamma-distributed variables.

Following an approach analogous to that used in deriving the Nakagami distribution [1], we make use of the following two-dimensional Laplace transform formula:

∫ ∞

∫ ∞

1 Γ(𝑘)𝑏𝑘−1

2 𝑒−𝛼(𝑥1+𝑥2)𝐼𝑘−1 2𝑏√𝑥1𝑥2 𝑒−𝑧1𝑥1−𝑧2𝑥2 𝑑𝑥1𝑑𝑥2

(𝑥1𝑥2) 𝑘−1

0

0

1

. (20)

=

(𝑧1 + 𝑎)(𝑧2 + 𝑎) − 𝑏2 𝑘

This formula, reported as equation (79) in [12], holds for ℜ(𝑘) > 0. By setting the parameters to match our exponential distribution, 𝑘 = 1, 𝛼 = 𝜎(11−𝜌) , 𝑏 =

√𝜌

𝜎(1−𝜌) , we obtain the joint characteristic function of the exponential distribution:

1 𝜎2(1 − 𝜌) (𝑧1 + 𝑎)(𝑧2 + 𝑎) − 𝑏2

. (21)

𝜑exp(𝑧1, 𝑧2) =

Since the sum of 𝑘 independent exponential variables follows a Gamma distribution, the characteristic function of two correlated Gamma variables can be directly deduced:

1 𝜎2𝑘(1 − 𝜌)𝑘 (𝑧1 + 𝑎)(𝑧2 + 𝑎) − 𝑏2 𝑘

𝜑Gamma(𝑧1, 𝑧2) = 𝜑exp(𝑧1, 𝑧2) 𝑘 =

. (22)

To invert this characteristic function and recover the probability density function, we use the two-dimensional Mellin inversion formula [13]:

2 ∫ 𝑐+𝑖∞

∫ 𝑐+𝑖∞

- 1

- 2𝜋𝑖


1

𝑒𝑧1𝑥1+𝑧2𝑥2 𝑑𝑧1𝑑𝑧2

(𝑧1 + 𝑎)(𝑧2 + 𝑎) − 𝑏2 𝑘

𝑐−𝑖∞

𝑐−𝑖∞

1

2 𝑒−𝛼(𝑥1+𝑥2)𝐼𝑘−1 2𝑏√𝑥1𝑥2 . (23)

Γ(𝑘)𝑏𝑘−1 (𝑥1𝑥2) 𝑘−1

=

Applying this inversion formula to the characteristic function in (22), we finally obtain the joint PDF of two correlated Gamma-distributed variables:

2√𝜌𝑥1𝑥2 𝜎(1 − 𝜌)

𝑓Gamma(𝑥1, 𝑥2) = (𝑥1𝑥2) 𝑘2−1

𝑥1 + 𝑥2 𝜎(1 − 𝜌)

exp −

. (24)

𝐼𝑘−1

Γ(𝑘)𝜎𝑘+1(1 − 𝜌)𝜌 𝑘2−1

This expression generalizes the previous result for the exponential PDF with 𝑘 = 1 and agrees with results reported in the literature (see [14,15]).

# 4. Probability Density Function of the Ratio of two correlated Gamma-distributed random variables

In this section, we derive the PDF of the ratio 𝑍 = 𝑋1/𝑋2, where 𝑋1 and 𝑋2 are two correlated Gamma-distributed random variables with the same shape and scale parameters.

By definition, the PDF of the ratio 𝑍 for two non-negative random variables 𝑋1 and 𝑋2 is given by:

