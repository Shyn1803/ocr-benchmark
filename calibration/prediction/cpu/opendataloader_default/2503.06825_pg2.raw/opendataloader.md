In presence of outliers, traditional estimation algorithms based on quadratic cost function can be overly influenced by outliers resulting in overall poor performance. In such cases estimation algorithms with Huber type cost functions ([9], [6] and [5]) may be more appropriate as the cost function switches from quadratic to linear when errors become sufficiently large as is the case with outliers. The second cost function considered in this paper is a hybrid of Huber loss function and ϵ-insensitive loss function as the one considered in [16] for ARMA system identification. The proposed cost function a) ignores small measurement errors (is ϵ-insensitive), and b) has linear instead of quadratic penalty for large errors making the estimates less sensitive to small noises as well as outliers. For linear dynamical systems, various other algorithms for handling outliers have also been proposed in [1], [3] and [8]. At a general level, Aravkin et al. [4] have considered estimation problems with such convex non-quadratic cost functions and drawn links to machine learning.

There are instances when additional information is available about the system beyond the description of the the dynamical model. Examples of such additional information are maximum or minimum value of certain states (for example price of an asset can never be negative or physical constraints that limit movement of an object) or knowledge about the magnitude of disturbances and measurement noises such as an upper bound on measurement noise. Incorporating such additional information can be helpful not only in identification of outliers but can also lead to improved estimates as such information puts constraints on exogenous signals and possible trajectories of states. One approach for estimation under such constraints is to obtain sets constraining possible state values (see for example [12] and [8]). At a more general overarching level, convex constraints with convex cost functions for smoothing problem have been considered by Aravkin et al. [4]. In this paper we assume the additional information about the system can be described in terms of inequality constraints that are linear with respect to states and exogenous signals and develop estimation algorithms that satisfy the constraints as well as minimize the two cost functions considered in this paper (ϵ insensitive quadratic as well as Huber).

In this paper we extend results from Nagpal [13] where optimal smoothing algorithms were developed for ϵ-insensitive ϵ insensitive Huber M loss function. The algorithms in this paper apply those results for one step horizon to develop recursive algorithms that are easily implemented and where complexity does not grow with the number of observations. Remarkably, the algorithms bear strong structural resemblance to Kalman Filter with the primary difference being that the update based on the new information ("innovation term") is based on solution of a quadratic optimization problem with linear constraints.

This paper is organized as follows. In the next section we describe the the two objective functions and the background results from Nagpal [13] which form the basis of the results presented here. Main results are described in Section 3 and the last section concludes with a summary of the results.

# 2 Problem Formulation and Background Results

Throughout the paper, N represents a positive integer which will be used to describe the number of measurements available for estimation. For vectors v,w ∈ Rn, v ≥ w implies that all the components of the vector v − w are non-negative. In particular for a real valued vector, v ≥ 0 would imply that all elements of the vector v are non-negative. For a matrix C ∈ Rm×n, C′ will indicate its transpose. For a vector xk ∈ Rn, xk

denotes the j′th element of xk.

j

For all the estimation problems we will assume that the underlying system is known and finite dimensional linear system of the following form:

xk+1 = Axk + Bwk, initial condition x0 is not known with x¯0 its best estimate yk = Cxk + vk (1)

where xk ∈ Rn is the state, yk ∈ Rm are the noisy measurements, wk and vk are unknown exogenous signals and measurement noises respectively. Given measurements {y1,...,yN}, the filtering problem involves estimating xN. The proposed algorithms described in this paper are applicable for linear time varying systems as well (when A,B and C depend on time index k in equation (1)) but for ease of transparency, we will assume the system parameters A ∈ Rn×n, B ∈ Rn×l and C ∈ Rm×n are known constant matrices.

For any k ≥ 0, xˆk will denote the estimate of xk based on the given measurements {y1,...,yk}. Im will denote identity matrix of dimension m. Given a sequence of vectors xk and matrices Rk, we will use the following vector and

2

