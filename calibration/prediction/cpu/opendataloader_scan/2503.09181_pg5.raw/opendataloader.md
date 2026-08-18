x ( n ) s = { x λ : λ ∈ s ( n ) } ⊂ x ( n ) be the subset of features, which represents the selected and revealed features. Our task is to select features s ( n ) and make a final prediction about y ( n ) while s ( n ) is different for each instance. Our purpose is to find two functions, implemented as neural networks; the

policy to select features and the predictor to make predictions. The policy takes the revealed features x ( n ) s and the whole features of features z ( n ) as input. Then, it returns one index and the corresponding feature will be selected and revealed. We denote the policy as π ( x ( n ) s ,z ( n ) ) ∈ Λ ( n ) . The predictor also takes x ( n ) s and z ( n ) as input and it returns the prediction about y ( n ) . We denote the prediction and the predictor as ˆ y ( n ) = f ( x ( n ) s ,z ( n ) )

We innovate a way to select features one by one with the policy until the predetermined number of features is selected. Firstly, we determine the budget k , which is the number of selected features in the end. In the initial state, we suppose s ( n ) = ϕ and x ( n ) s = ϕ , that is, any features has not revealed. Note that, we assume that features of features z are fully revealed in the initial state and they are given as prior information. This assumption is natural because we consider features of features as the description or the property of each feature on the natural language or numerical expression and they are usually given before the feature values are revealed. Then, we select a feature with the policy π ( x s ,z ) and reveal the selected feature. (In other words, s ← s ∪ π ( x s ,z ) and the size of x s increases by one.) We repeat this process for k times and make the final prediction with the predictor f ( x s ,z ) from | x s | = k features. This procedure is shown in Fig. 1b and 1c.

Our ultimate goal is to minimize the loss of the prediction made by the predictor after selecting features by the policy. Given the loss function l (ˆ y,y ) , the objective function of our problem is

$$
min 0,0
$$

where θ and ϕ are parameters for parameterized predictor and policy respectively. In addition, s ( | s | = k ) is constructed by the iterative selection of the policy π ( x ,z ) .

# 4 Greedy Dynamic Feature Selection

This section explains the existing DFS method based on conditional mutual information (CMI) [3]. Note that this method handles the special case of our problem definition that the feature set is fixed. Namely, Λ = [ d ] and Λ ( n ) = Λ for all n = 1 ,...,N . Therefore, in this section, we note x = { x 1 ,...,x d } and x s = { x i : i ∈ s ⊂ [ d ] } . Also, the policy π ( x s ) and the predictor f ( x s ) take only revealed features x s as input.

# 4.1 Greedy Dynamic Feature Selection

This method aims to find a greedy policy based on CMI and the predictor based on the naive Bayesian, implemented as neural networks such as MLP. Concretely,

