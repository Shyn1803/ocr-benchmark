# arXiv:2503.04876v1 [stat.ME] 6 Mar 2025

Estimation of relative risk, odds ratio and their

logarithms with guaranteed accuracy and controlled sample size ratio

Luis Mendo*

*Information Processing and Telecommunications Center, Universidad Polit´ecnica de Madrid, Avenida Complutense, 30, Madrid, 28040, Spain.

Abstract Given two populations from which independent binary observations are taken with parameters p1 and p2 respectively, estimators are proposed for the relative risk p1/p2, the odds ratio p1(1− p2)/(p2(1− p1)) and their logarithms. The estimators guarantee that the relative mean-square error, or the mean-square error for the logarithmic versions, is less than a target value for any p1, p2 ∈ (0,1), and the ratio of average sample sizes from the two populations is close to a prescribed value. The estimators can also be used with group sampling, whereby samples are taken in batches of fixed size from the two populations. The efficiency of the estimators with respect to the Cram´er–Rao bound is good, and in particular it is close to 1 for small values of the target error.

Keywords: Estimation, sequential sampling, group sampling, relative risk, odds ratio, log odds ratio, mean-square error, efficiency.

MSC2010 Classification:: 62F10 , 62L12

## 1 Introduction

Let p1, p2 ∈ (0,1) denote the probabilities of occurrence of a given dichotomous attribute in two different populations. The problem of estimating the relative risk (RR) or risk ratio,

- p1

- p2


θ =

, (1)

from binary observations of the two populations arises frequently in medical and social sciences, as well as in other fields. For example, in a phase-III clinical trial of a vaccine (Armitage et al, 2002, chapter 18) the relevant attribute is the presence of a disease, and the two populations are vaccinated and non-vaccinated people. The odds ratio (OR),

- p1(1− p2)

- p2(1− p1)


ψ =

, (2)

1

