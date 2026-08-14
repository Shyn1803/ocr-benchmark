Encoding Argumentation Frameworks to Propositional Logic Systems 7

Remark 2.14. In PL[0,1]s, the evaluation of formulas with connective & is traditionally extended as a&b = T( a , b ) = a ∗ b and the evaluation of formulas with connective ∧ is extended as a ∧ b = min{ a , b }. For keeping the uniﬁcation of form of the normal encoding function, we extend the evaluation of formulas with connective ∧ as a∧b = T( a , b ) = a ∗ b , which will not cause any confusion in this paper.

2.3. Model Checking

Besnard and Doutre [12] give a method of model checking. The method aims to translate an AF as a propositional formula in the PL2, such that the models of the propositional formula are corresponding to extensions of the AF under a kind of semantics. In fact, the core of each model is an extension of the AF and vice versa. The translating functions depend on various semantics. The mainly results in the chapter “model checking” in [12] are listed as the following, where each Φ is a translating function.

Let AF = (A,R) be an argumentation framework.

1. Translating the AF to the PL2 for conﬂict-free semantics. A set S ⊆ A is conﬂict-free iﬀ S is the core of a model of any formula

below:

¬b); (2.1)

(a →

a∈A

b:(b,a)∈R

¬b); (2.2)

(a →

a∈A

b:(a,b)∈R

(¬a ∨ ¬b). (2.3)

(a,b)∈R

2. Translating the AF to the PL2 for stable semantics. A set S ⊆ A is a stable extension iﬀ S is the core of a model of the

formula below:

¬b). (2.4)

(a ↔

a∈A

b:(b,a)∈R

This formula is come up with by Creignou in [29] to characterize the kernels of a graph, and is applied in [12] to characterize the stable extensions of an AF.

3. Translating the AF to the PL2 for admissible semantics. A set S ⊆ A is a admissible set iﬀ S is the core of a model of the formula

below:

c))). (2.5)

(

¬b) ∧ (a →

((a →

a∈A

c:(c,b)∈R

b:(b,a)∈R

b:(b,a)∈R

4. Translating the AF to the PL2 for complete semantics. A set S ⊆ A is a complete extension iﬀ S is the core of a model of the

formula below:

c))). (2.6)

(

¬b) ∧ (a ↔

((a →

a∈A

c:(c,b)∈R

b:(b,a)∈R

b:(b,a)∈R

