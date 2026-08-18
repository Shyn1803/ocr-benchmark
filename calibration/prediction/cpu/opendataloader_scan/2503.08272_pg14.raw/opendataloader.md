Finally, we briefly summarise the link between local and global utility in the monotone case, which too is completely analogous to the previous subsection. The expression for maximal expected monotone quadratic utility from Proposition 2.3 and Theorem 2.16 translates to

$$
1 2uMmv (0) =
$$

  where we may interpret   K mmv = B 2 g mmv ◦ ( ˆ λ · R ) as the cumulative maximal local squared MHR. Using the conversion between the (monotone) Hansen and the (monotone) Sharpe ratio, we also obtain

$$
1 + (0)
$$

  where   K mmv = 1 1 − ∆   K mmv ·   K mmv is the cumulative local squared monotone Sharpe ratio.

# 4 ExAMPLES

Example 4.1 illustrates that the locally optimal strategy ˆ λ may not be unique even if there is no redundancy among the traded assets. Example 4.2 contrasts classical mean–variance and monotone mean–variance optimal portfolios in a continuous-time setting. Example 4.3 shows that the equivalences in Theorem 2.25 fail when R is not square integrable. Example 4.4 illustrates that ˆ Q can be equivalent to P without being a σ -martingale measure for R , again highlighting the importance of the square-integrability assumption in Theorem 2.25 . Example 4.5 constructs a model with square-integrable yield R , where the maximal Sharpe ratio available by trading is finite but the maximal monotone Sharpe ratio is infinite. Example 4.6 exhibits a complete market model with an equivalent martingale measure, where both the MV utility and the MMV utility are infinite.

Example 4.1. Consider a one-period model with four atoms and two assets, whose yield distribution is given by

<table>
  <tr>
    <th> </th>
    <th>W1</th>
    <th>W2</th>
    <th>W3</th>
    <th>W4</th>
  </tr>
  <tr>
    <td>P[{w}]</td>
    <td>] 0.2</td>
    <td>0.6</td>
    <td>0.1</td>
    <td>0.1</td>
  </tr>
  <tr>
    <td>ARI (w)</td>
    <td>ω ) -0.5</td>
    <td>0.5</td>
    <td>1</td>
    <td>1.2</td>
  </tr>
  <tr>
    <td>AR2 ()</td>
    <td>ω ) -0.5</td>
    <td>0.5</td>
    <td>1.2</td>
    <td>1</td>
  </tr>
</table>


Choosing q = (0 . 62 , 0 . 18 , 0 . 1 , 0 . 1) yields an equivalent martingale measure Q for R , hence the model is arbitrage-free. Observe that in this model, all separating measures are martingale measures for R . One easily verifies that ˆ q = (0 . 5 , 0 . 5 , 0 , 0) defines a martingale measure ˆ Q whose density satisfies

$$
2 Var dP 3
$$

The duality constraint in Proposition 2.20 and ( 2.7 ) yield that twice the maximal utility cannot exceed 1 − (1 + 2 3 ) − 1 = 0 . 4 . On the other hand, one has E [2 g mmv ( R 1 )] = E [2 g mmv ( R 2 )] = 0 . 4 hence we have two distinct optimal strategies, each investing one dollar in one of the assets, respectively, and borrowing one dollar at the zero risk-free rate. Any affine combination of these two strategies is again optimal. The wealth of all optimal strategies coincides below the bliss point of the utility function.

In this example, 2/3 is the maximal squared monotone Sharpe ratio among zero-cost strategies and 0.4 (twice the maximal expected utility) is the maximal squared monotone Hansen ratio among zero-cost strategies.

