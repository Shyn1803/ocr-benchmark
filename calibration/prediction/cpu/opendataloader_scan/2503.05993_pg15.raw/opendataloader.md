Double Pendulum

Pixel Data

![](<2503.05993_pg15_images/imageFile1.png>)

(a)

(b)

Pixel Data: Pendulum Experiment

X -data

Y,-data

0.75

~data

1.00

Yz-data

X-data

Single Pendulum

y-data

0.25

0.75

0,25

0.50

lo

0.25

X

ẵ

0,00

Time (s)

Time (s)

0.50

1.5

2.0

1.0

2.5

3.0

3.5

4.0

Time

(s)

(c)

(d)

Double Pendulum

Data Requirement

SVD Analysis for Double Pendulum

k=0 (Full library)

Pendulum Algebraic

160

k=l

Pendulum Dynamic

X

algebraic

k=2

Double Pendulum

15

140

- k=3
- k=4


120

10

1

ẵ

100

15

1

=25

25

125

50

75

100

k=0

k=1

k=2

k=3

k=4

Highest monomial degree

Principal Components

Refinement Number

Figure 4. Example 3: Application to non-linear pendulum. ( a ) Schematic diagram: single pendulum ( top ) and double pendulum ( bottom ). ( b ) Scaled pixel data: single pendulum experiments ( left ) and double pendulum animation ( right ). ( c ) Data requirement: comparison between damped single pendulum and double pendulum. ( d ) SVD analysis: determining the number of algebraic constraints in the case of the chaotic double pendulum with degree 5 library.

2 that the equations we discovered after applying the transformation ( 35 ) are consistent with ( 30 ) and ( 28 ). To discover the dynamic equations in the polar coordinate system, we applied a Savitzky-Golay filter [ 48 ] with a window size of 12 to compute the first and second derivatives of the φ . The candidate library consisted of monomials of φ , ˙ φ , cos φ and sin φ : Θ ∗ = { φ , ˙ φ , cos φ , sin φ , φ 2 , φ ˙ φ ,... } . Using ( 35 ), we included x and y in the library instead of calculating cos φ and sin φ directly from φ . Similar to the algebraic finder step, we restricted the monomial degree to 3 for Case 1 and varied it between 2 and 5 for Case 2 for a comparative study. After using sparse regression, where sequential threshold with inner iterations consisting of LASSO regularization was applied, we used a curve fit package to determine the correct parameters. In both case 1 and case 2, simulated solutions based on the discovered equations were able to predict the test pixel data accurately (see supplementary Section 3 for details on discovered equations and parameter estimation). For Case 3, SODAs robustly identified the constraints ( 33 )–( 34 ) from pixel data obtained from a single video segment,

using various upper bounds on the degree of the monomial library. Note that the polar nature of the states ( x 2 , y 2 ) is not immediately evident from the pixel data of the secondary pendulum in the double-pendulum (Figure 4 b right ). This is because the secondary pendulum does not have a fixed pivot and sweeps trajectory in the 2D plane that doesn’t correspond to an identifiable pattern. Nevertheless, SODAs discovered an expanded version of ( 34 ). This algebraic discovery enables us to determine the transformation to the polar coordinate system: φ 1 = arctan y 1 x 1 and φ 2 = arctan y 1 − y 2 x 1 − x 2 , which can be further used for dynamic discovery. The dynamic discovery of equations governing the motion of the double pendulum similar to the form ( 31 ) –( 32 ) based on polar coordinates, has been successfully demonstrated using SINDy-based methods [ 27 ]. We do not repeat this work here using our pixel data because it requires addressing noisy derivatives and may require advanced smoothing filters

