A closely related concept is the proximal-point operator [31], which plays a fundamental role in the definition of the Moreau envelope and in developing proximal-based iterative schemes for minimizing the cost function φ , which is defined as

$$
=arg min 2 (1.2) yeRn
$$

The proximal operator enjoys several favorable properties under convexity, contributing to its popularity for developing numerical methods: (i) prox γφ is single-valued at each x ∈ R n ; (ii) it is Lipschitz continuous with the constant 1; (iii) it satisfies the identity

$$
arg min p(x) = Fix(prox-p)
$$

€ arg P(s) under the convexity. For convex 4, it holds that minr€Rn

$$
) (1.3)
$$

implying that the proximal method can be interpreted as a gradient descent with constant step-size γ ; cf. [36]. Thanks to the simple structure and low memory requirements, proximal-point methods have received increasing attention, following the seminal works by Martinet [26, 27]; see, e.g., [3, 18, 24, 35, 36, 42] and references therein. In the nonconvex setting, the fundamental properties of the proximal operator and Moreau envelope require involved assumptions such as prox-regularity and calmness of the cost in the local or global setting for which we invite the readers to study [37, 39].

Recent studies of proximal-point methods and the Moreau envelope have uncovered the further potential of these approaches in the presence of high-order regularization terms; see, e.g., [2, 3, 20–22, 34, 35, 47]. In these developments, as opposed to the classical case, the quadratic regularization in (1.1) and (1.2) is replaced by the term 1 p ∥ x − y ∥ p for p > 1, leading to a much more flexible setting. In particular, in [20] an inexact two-level smoothing optimization framework (ItsOPT) is introduced for general nonsmooth and nonconvex optimization problems. This framework consists of two levels: (i) at the lower level, the high-order proximal auxiliary problems are solved inexactly to produce an inexact oracle for HOME; (ii) at the upper level, an inexact zero-, firstor second-order method is developed to minimize HOME. Additionally, the framework has been adapted for solving nonsmooth weakly convex optimization problems in [21]. The crucial role of the basic properties of HOME, its differentiability, and its weak smoothness in these methodologies motivates the quest to study fundamental and differential properties of HOME in the nonconvex setting.

# 1.1 Contribution

Our contributions are threefold:

- (i) Fundamental properties of HOPE and HOME. We derive several fundamental properties of the high-order Moreau envelope (HOME) and the corresponding proximal operator (HOPE), including coercivity and sublevel set relationships between φ and φ γ (cf., Propositions 9 and 10, Corollary 11), facilitating to design algorithms on φ γ . Further, we introduce the notion of p -calmness , a key condition for deriving the differentiability of HOME, and characterize its relationships with classical reference points (cf., Theorem 15).
- (ii) Differentiability and weak smoothness of HOME. We comprehensively analyze the differentiability and weak smoothness of HOME for nonsmooth and nonconvex functions under p -calmness and q -prox-regularity assumptions (see Definitions 13 and 18), with p > 1. It is shown that HOME is continuously differentiable when q ≥ 2 and p ∈ (1 , 2] or 2 ≤ p ≤ q (cf. Theorems 25 and 26), and weakly smooth with H¨lder-continuous gradients under broader conditions (cf. Theorems 29 and 30). However, for p ≤ q the differential properties of HOME remain open to us, which is summarized in Subfigure (a) of Figure 1. Furthermore, the relationship among reference points of φ and φ γ are clarified (cf. Corollary 27 and Remark 28.), as emphasized in Subfigure (b) of Figure 1. (iii) The high-order proximal-point algorithm (HiPPA). The HiPPA algorithm is introduced and a very


simple convergence analysis to proximal fixed points using properties of HOME is studied (cf. Theorem 31). Preliminary numerical tests of HiPPA on Nesterov-Chebyshev-Rosenbrock functions demonstrate its promising potential for solving nonsmooth and nonconvex optimization.

