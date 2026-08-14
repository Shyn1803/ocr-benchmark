where the total number of parameters is 1 + m with m ≥ 1. Alternatively, we can express wde as

w(zn) − w(zn−1) zn − zn−1

wde(zn−1 < z ≤ zn) = w(zn−1) +

(z − zn−1) , (1 ≤ n ≤ m) (6)

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile1.png>)

Now the parameters become w(zn)’s, which are values of wde at the divided points and boundaries zn (0 ≤ n ≤ m) . In this case we have

3w(zn−1)(1+zznn−)−zw(zn)(1+zn−1)

(z−zn−1)} 1 + z 1 + zn−1

w(zn)−w(zn−1) zn−zn−1

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile2.png>)

n−1

F(zn−1 < z ≤ zn) = e3{[w(zn−1)−w(0)]+

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile3.png>)

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile4.png>)

3w(zi−1)(1+zzi)−w(zi)(1+zi−1)

n−1

1 + zi 1 + zi−1

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile5.png>)

i−zi−1

×(1 + z)3

, (1 ≤ n ≤ m) (7)

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile6.png>)

i=1

where we have used z0 = 0. For wde in the last bin z ∈ (zm, ∞), we set it to be a constant wL, and

1 + z 1 + zm

L) (8) Now the formula for H(z) is ready.

)3(1+w

F(z > zm) = F(zm)(

![](<e0a0e81c809de5de9bf34d2e15aea9e8726bc5e6e578a0ef14b28c897a27542d_images/imageFile7.png>)

There is one more thing to be mentioned: once we have ﬁtted our model with the data introduced in the next section, errors of w(zi) are correlated, i.e., the errors of w(zi) are dependent on each other. New parameters can be deﬁned by transforming the covariance matrix of w(zi), so that errors of new parameters are decorrelated and do not entangle with each other. The new uncorrelated parameters are referred to as the principal components [10, 23], and they are directly related to their own locations (unlike the correlated case). So errors of the uncorrelated parameters are more interpretable and meaningful. For more discussions and implications of the uncorrelated parameters, we refer to the references [11, 14, 24]. In section IV, we will show both errors of correlated and uncorrelated parameters of wde. The uncorrelated technique we adopt from [11] is as follows.

1. Get the covariance matrix

<table>
  <tr>
    <th>C = WWT − W WT</th>
    <th>(9)</th>
  </tr>
  <tr>
    <td>where W is the vector of w(zi). The Fisher matrix F is deﬁned by 2. Diagonalize the Fisher matrix by an orthogonal matrix O</td>
    <td>F = C−1.</td>
  </tr>
  <tr>
    <td>F = OTΛO,</td>
    <td>(10)</td>
  </tr>
</table>


5

