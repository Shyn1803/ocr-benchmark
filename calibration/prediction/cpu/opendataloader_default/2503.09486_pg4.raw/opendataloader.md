where eγ,ρ(x1,t1,x2,t2) = −∞ for any other choice of x1,x2. Then the metric e arising from planting measures along a finite or countable set of curves is the smallest metric which is bounded below by satisfying e ≥ d, and for each curve γi and planted measure ρi, e ≥ eγ

i,ρi. All metrics not of this form have infinite rate.

For each such planted measure, the contribution to the rate function is Ii =

3 2

4 3 ρ

i dt, so that the rate function I of a metric e is the sum over all planted

measures I = i Ii. Our goal in this paper is to find the lowest rate metric for which a geodesic F from (0,0) to (0,1) passes through the point (1,a).

Our metrics will generally have a measure planted along just one curve, which will be the geodesic from (0,0) to (0,1). Any measure planted outside of this geodesic will not increase its length, but may increase the length of paths other than F, which only reduces the possibility of F being a geodesic, all while increasing the rate.

We can then define e or e(F,ρ) as the metric arising from planting ρ along F, which will be our geodesic.

We will in fact prove a result about e: Suppose Mε is a metric sampled from the conditional law of Lε, given that the rightmost geodesic γ of e from (0,0) to (0,1) satisfies γ(a) ≥ 1.

Theorem 1.3. As ε → 0, Mε → e(F,ρ) in probability with respect to uniform convergence on bounded sets, with F as in Theorem 1.2 and ρ as given by:

ρ(t) =

- 1

a2(3−

√8a)2, if t ≤ 2a

- 2


√8a)2 , if 2a ≤ t ≤ 1.

at(3−

# 2 Solution of a relaxed problem

One possible candidate for F is two straight line segments, from (0,0) to (1,a) and from (1,a) to (0,1), with ρ just sufficient to compensate d, such that e(0,0,F(t),t) = 0,∀t ∈ [0,1]. However, for a < 21, this will not be a geodesic: instead, there will be straight lines from (0,0) to a point beyond (1,a) whose Dirichlet length is greater than the length of F to that point. As a result, the geodesic will skip the steeper line segment to (1,a) and take such a straight line as a shortcut to F, and then follow part of the other line segment to (0,1). Similarly, if a > 12, it will follow part of the line segment from (0,0) to (1,a) and then shortcut the steep segment to proceed directly to (0,1).

This suggests that we should try to solve for a metric where the segment from (0,0) to (1,a) is not skipped by such a shortcut. In other words, we should ask what is the lowest rate metric for which there is a geodesic candidate F, so that the distance from (0,0) along F to any point on F is greater than the distance of a shortcut from (0,0) to that point.

Inspired by this intuition, we will first solve an intermediate optimization problem: fix F0 and ρ0 (and therefore e(F0,ρ0)) for t ∈ [0,t1]. Consider pairs (F,ρ) that agree with (F0,ρ0) on [0,t1]. Which pair minimizes the rate of the

4

