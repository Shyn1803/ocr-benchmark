1

A Gap Penalty Reformulation for Mathematical Programming with Complementarity Constraints: Convergence Analysis

Kangyu Lin and Toshiyuki Ohtsuka

arXiv:2503.05181v1 [math.OC] 7 Mar 2025

Abstract—Our recent study [1] proposed a new penalty method to solve the mathematical programming with complementarity constraints (MPCC). This method reformulates the MPCC as a parameterized nonlinear programming (NLP) called gap penalty reformulation and solves a sequence of gap penalty reformulations with an increasing penalty parameter. This letter studies the convergence behavior of the new penalty method. We prove that it converges to a strongly stationary point of MPCC, provided that: (1) The MPCC linear independence constraint qualiﬁcation holds; (2) The upper-level strict complementarity condition holds; (3) The gap penalty reformulation satisﬁes the second-order necessary conditions in terms of the second-order directional derivative. Since the strong stationarity is used to identify the local minimum of MPCC, our convergence analysis indicates that the new penalty method is capable of ﬁnding an MPCC solution.

I. INTRODUCTION A. Background

This study considers a special yet common class of nonlinear programming (NLP), known as mathematical programming with complementarity constraints (MPCC). Discrete variables deﬁning logical decisions can be represented by continuous variables with complementarity constraints. Thus, MPCC can model various optimization problems with combinatorial characteristics originating from engineering and economics, such as process optimization with discrete events, trajectory optimization with contacts, and bilevel optimization [2].

However, complementarity constraints also pose signiﬁcant challenges for solving the MPCC, where almost all constraint qualiﬁcations (CQs) are violated at any feasible point of MPCC. The lack of constraint regularity leads to two difﬁculties: First, MPCC solutions can not be characterized by the optimality conditions for a standard NLP problem; Second, MPCC cannot be solved using standard NLP solution methods. To characterize the MPCC solution, various MPCC-tailored concepts have been proposed [3], where some of which are reviewed in Section II-A. To solve the MPCC efﬁciently, many MPCC-tailored solution methods, such as relaxation methods and penalty methods, have been proposed (Chapter 11 in [2]). These methods do not solve the MPCC directly. Instead, they reformulate the complementarity constraints as parameterized costs or constraints, solve a sequence of well-deﬁned parameterized NLP, and then present a rigorous convergence analysis showing that the sequence of solutions to the parameterized

This work was supported in part by the JSPS KAKENHI Grant Number JP22H01510 and JP23K22780. Kangyu Lin was supported by the CSC scholarship (No. 201906150138). The authors are with the Systems Science Course, Graduate School of Informatics, Kyoto University, Kyoto, Japan. Corresponding author: Kangyu Lin. Email: k-lin@sys.i.kyoto-u.ac.jp, ohtsuka@i.kyoto-u.ac.jp.

NLP can ﬁnally converge to an MPCC solution. These MPCCtailored solution methods are practical because they are easy to implement using state-of-the-art NLP software.

Our recent study [1] proposed a new penalty method called gap penalty method, which reformulates the MPCC as a parameterized NLP called gap penalty reformulation and solves a sequence of gap penalty reformulations with an increasing penalty parameter. Compared to other penalty methods, gap penalty reformulation exhibits certain convexity structures that can be exploited by a dedicated Hessian regularization method. Gap penalty method has been shown to be practically effective in [1], but its theoretical convergence has not been analyzed.

- B. Contribution

This study builds upon the work in [1] by providing a rigorous convergence analysis for the gap penalty method. The contributions of this study are mainly in two aspects.

First, since gap penalty reformulation involves a Lipschitz continuously differentiable function, we characterize its solutions using second-order directional derivatives rather than the Hessian matrix as in standard NLP theory. These results are critical for the subsequent convergence analysis.

Second, we prove that the gap penalty method converges to a strongly stationary point of MPCC under certain standard MPCC-tailored assumptions. Our convergence analysis theoretically conﬁrms that the gap penalty method is capable of ﬁnding an MPCC solution.

- C. Outline and notation


The remainder of this study is organized as follows: Section II reviews some MPCC-tailored concepts and the gap penalty reformulation; Section III presents the optimality conditions of the gap penalty reformulation; Section IV presents a detailed convergence analysis; and Section V concludes this study.

Given two variables x,y ∈ Rn, we denote the element-wise complementarity conditions between x and y by 0 ≤ x ⊥ y ≥ 0, i.e., x,y ≥ 0 and x⊙y = 0, with ⊙ the Hadamard product. The complementarity problem is to ﬁnd a pair (x,y) that satisﬁes 0 ≤ x ⊥ y ≥ 0. Given a differentiable function f(x), we denote its Jacobian by ∇xf ∈ Rm×n with f : Rn → Rm, and its Hessian by ∇xxf ∈ Rn×n with f : Rn → R. We say that function f(x) is k-th Lipschitz continuously differentiable (LCk in short) if its k-th derivative is Lipschitz continuous.

II. MATHEMATICAL PROGRAMMING WITH COMPLEMENTARITY CONSTRAINTS

A. MPCC-tailored concepts

We review some MPCC-tailored concepts that are relevant to our subsequent convergence analysis. Consider the MPCC

