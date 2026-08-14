arXiv:2503.07447v1 [math.CO] 10 Mar 2025

A new density limit for unanimity in majority dynamics on random graphs

Jeong Han Kim and BaoLinh Tran June 2022

Abstract

Majority dynamics is a process on a simple, undirected graph G with an initial Red/Blue color for every vertex of G. Each day, each vertex updates its color following the majority among its neighbors, using its previous color for tie-breaking. The dynamics achieves unanimity if every vertex has the same color after ﬁnitely many days, and such color is said to win.

When G is a G(n,p) random graph, L. Tran and Vu (2019) found a codition in terms of p and the initial diﬀerence 2∆ beteween the sizes of the Red and Blue camps, such that unanimity is achieved with probability arbitrarily close to 1. They showed that if p∆2 ≫ 1, p∆ ≥ 100, and p ≥ (1 + ε)n−1 log n for a positive constant ε, then unanimity occurs with probability 1 − o(1). If p is not extremely small, namely p > log−1/16 n, then Sah and Sawhney (2022) showed that the condition p∆2 ≫ 1 is suﬃcient.

If n−1 log2 n ≪ p ≪ n−1/2 log1/4 n, we show that p3/2∆ ≫ n−1/2 log n is enough. Since this condition holds if p∆ ≥ 100 for p in this range, this is an improvement of Tran’s and Vu’s result. For the closely related problem of ﬁnding the optimal condition for p to achieve unanimity when the initial coloring is chosen uniformly at random among all possible Red/Blue assignments, our result implies a new lower bound p ≫ n−2/3 log2/3 n, which improves upon the previous bound of n−3/5 log n by Chakraborti, Kim, Lee and T. Tran (2021).

# 1 Introduction

1.1 Majority Dynamics

Consider a parliamentary election with two parties. The election season begins with Day 0, where each voter supports one side. At the end of every day, each voter polls their friends, then supports the majority side the next morning, or keeps their aﬃliation in case of a tie. On election day, everyone votes for the party they currently supports and the parliament will be divided proportionally with each side’s number of votes.

This process can be modeled with a graph process, where vertices represent voters and edges represent friendships. We let Red and Blue, or R and B, stand for the two parties. The state of aﬃliations at any time is simply a coloring on the graph. This process on a graph is called Majority Dynamics in literature, due to the majority-based updating rule.

1

