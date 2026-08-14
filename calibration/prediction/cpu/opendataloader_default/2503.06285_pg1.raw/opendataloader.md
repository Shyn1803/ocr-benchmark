# arXiv:2503.06285v1 [math.OC] 8 Mar 2025

## Modified Bregman Golden Ratio Algorithm for Mixed Variational Inequality Problems

#### Gourav Kumara and V. Vetrivela

aDepartment of Mathematics, Indian Institute of Technology Madras, Chennai, 600036, India

ARTICLE HISTORY Compiled March 11, 2025

ABSTRACT

In this article, we provide a modification to the Bregman Golden Ratio Algorithm (B-GRAAL). We analyze the B-GRAAL algorithm with a new step size rule, where the step size increases after a certain number of iterations and does not require prior knowledge of the global Lipschitz constant of the cost operator. Under suitable assumptions, we establish the global iterate convergence as well as the R-linear rate of convergence of the modified algorithm. The numerical performance of the proposed approach is validated for the matrix game problem and the sparse logistic regression problem in machine learning.

KEYWORDS Variational inequality; Bregman distance; KL divergence; Sparse logistic regression; Matrix games

MSC 47J20, 49J40, 65K15, 65Y20

### 1. Introduction

Let H be a real finite dimentional Hilbert space. A mixed variational inequality problem (MVIP) is a problem to find w∗ ∈ H such that

⟨A(w∗),w − w∗⟩ + g(w) − g(w∗) ≥ 0 ∀w ∈ H, (1)

where A : H → H is the cost operator, and g : H → R ∪ {+∞} is an extended real-valued function. We denote the set of solutions of (1) by S. Mixed variational inequality problems (MVIPs) of the form (1) generalize various optimization problems encountered in nonlinear programming and variational analysis, including minimization problems, linear complementarity problems, and variational inequalities, see [1,3,11,33]. These problems have widespread applications in diverse fields, such as data science, image processing, mechanics, control theory, economics, structural engineering, and many more; see [1,9,14,15,21,23–25], and the references therein.

Many algorithms solving the variational inequality (1) (for example; see [11,29,31]), need the exact value of the global Lipschitz constant of the cost operator A. This

Gourav Kumar, Email: ma24r001@smail.iitm.ac.in; V.Vetrivel, Email:vetri@iitm.ac.in

