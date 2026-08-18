![](<2503.05752_pg4_images/imageFile1.png>)

0.05

0.05

-0.05

-0.05

-0.05

0.05

"0.1

0.1

"0.1

-0.05

0.05

Interpolation nodes

(b) Center evaluation nodes

Figure 1: Distribution of interpolation and evaluation nodes within a circle of radius 0.1.

0.1, f(x,y)

![](<2503.05752_pg4_images/imageFile2.png>)

0.1, fx (x,y)

R

R

100

Classic HRBF (deg

Classic HRBF (deg

MHRBF (deg

MHRBF (deg

10~2

102

1

1

10

10

Ẳ

10

10

Ệ 10

1010

10-12

10-12

10-14

10-16

101

101

10-3

10-1

10-2

Shape Parameter € (GA)

Shape Parameter € (GA)

shape parameter

Error in f

shape parameter

Error in f x

VS.

VS.

0.1, Condition Number

R = 0.1, fy(x,y)

(deg

10"

Classic HRBF

Classic HRBF

1025

MIRBF

MIIRBF

1

10

1

1023

10

10

Ẳ

1021

1

1019

10

1

10-12

1017

10-14

1015

10

10

10

1o0

101

10

10

100

10'

10

Shape Parameter

(GA)

Shape Parameter € (GA)

shape parameter

shape parameter

Error in f y

Condition number

VS.

VS.

Figure 2: Comparison of Accuracy and Numerical Stability for HRBF and MHRBF: The errors (function, f , and its first derivatives, f x and f y ) and condition number computed in double precision for GA kernel, as functions of shape parameter ε , with polynomial degree of 6 and n = 4 for MHRBF.

The results in Figure 2 reveal significant accuracy improvements with MHRBF compared to HRBF. Since the error trends for ∇ f closely follow that of f , the subsequent analysis focuses primarily on the function interpolation. Figure 2a demonstrates that the MHRBF achieves low error over a large range of ε values, with the error ∼ 10 − 14 for all ε ≳ 0 . 5, despite the fact that the condition number of the MHRBF being

