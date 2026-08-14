![](<2503.05993_pg15_images/imageFile1.png>)

# Figure 4. Example 3: Application to non-linear pendulum. (a) Schematic diagram: single pendulum (top) and double

pendulum (bottom). (b) Scaled pixel data: single pendulum experiments (left) and double pendulum animation (right). (c) Data requirement: comparison between damped single pendulum and double pendulum. (d) SVD analysis: determining the number of algebraic constraints in the case of the chaotic double pendulum with degree 5 library.

in the absence of additional information about the system. Indeed, under the translation φ = ω + 32π , it can be easily verified that the equations we discovered after applying the transformation (35) are consistent with (30) and (28). To discover the

dynamic equations in the polar coordinate system, we applied a Savitzky-Golay filter [48] with a window size of 12 to compute the first and second derivatives of the φ. The candidate library consisted of monomials of φ,φ˙,cosφ and sinφ :

Θ∗ = {φ,φ˙,cosφ,sinφ,φ2,φφ˙,...}. Using (35), we included x and y in the library instead of calculating cosφ and sinφ directly from φ. Similar to the algebraic finder step, we restricted the monomial degree to 3 for Case 1 and varied it between 2 and 5 for Case 2 for a comparative study. After using sparse regression, where sequential threshold with inner iterations consisting of LASSO regularization was applied, we used a curve fit package to determine the correct parameters. In both case 1 and case 2, simulated solutions based on the discovered equations were able to predict the test pixel data accurately (see supplementary Section 3 for details on discovered equations and parameter estimation).

For Case 3, SODAs robustly identified the constraints (33)–(34) from pixel data obtained from a single video segment, using various upper bounds on the degree of the monomial library. Note that the polar nature of the states (x2,y2) is not immediately evident from the pixel data of the secondary pendulum in the double-pendulum (Figure 4b - right). This is because the secondary pendulum does not have a fixed pivot and sweeps trajectory in the 2D plane that doesn’t correspond to an identifiable pattern. Nevertheless, SODAs discovered an expanded version of (34). This algebraic discovery enables us to determine the transformation to the polar coordinate system: φ1 = arctan xy1

and φ2 = arctan yx1−y2

1−x2, which can be further used for dynamic discovery. The dynamic discovery of equations governing the motion of the double pendulum similar to the form (31) –(32) based on polar coordinates, has been successfully demonstrated using SINDy-based methods [27]. We do not repeat this work here using our pixel data because it requires addressing noisy derivatives and may require advanced smoothing filters

1

15/29

