# EFFICIENT ROBUST ADAPTIVE BEAMFORMING BASED ON SPATIAL SAMPLING WITH VIRTUAL SENSORS

Saeed Mohammadzadeh Rodrigo C. de Lamare

University of York, UK and CETUC/PUC-Rio, Rio de Janeiro, Brazil

# ABSTRACT

Robust adaptive beamforming (RAB) based on interference-plusnoise covariance (IPNC) matrix reconstruction can experience serious performance degradation in the presence of look direction and array geometry mismatches, particularly when the input signal-tonoise ratio (SNR) is large. In this work, we present a RAB technique to address covariance matrix reconstruction problems. The proposed method involves IPNC matrix reconstruction using a lowcomplexity spatial sampling process (LCSSP) and employs a virtual received array vector. In particular, we devise a power spectrum sampling strategy based on a projection matrix computed in a higher dimension. A key feature of the proposed LCSSP technique is to avoid reconstruction of the IPNC matrix by integrating over the angular sector of the interference-plus-noise region. Simulation results are shown and discussed to verify the effectiveness of the proposed LCSSP method against existing approaches.

Index Terms Covariance matrix reconstruction, Robust adaptive beamforming, Spatial spectrum process, Virtual Sensors.

# 1. INTRODUCTION

Many adaptive beamforming methods have been applied in wireless communications, sonar, and radar due to their superior interference mitigation capability [1]. However, under non-ideal conditions such as finite data samples and mismatches between the presumed and true steering vector (SV) the performance of adaptive beamformers degrades substantially. Several RAB techniques have been proposed to enhance robustness against the aforementioned mismatches, such as the linearly constrained minimum variance (LCMV) beamformer [2], diagonal loading (DL) [3, 4, 5, 6, 7, 8], the eigenspace-based beamformer [9, 10], the worst case-based technique [11, 12], the probabilistically constrained approach in [13, 14] and the modified robust Capon beamformer in [15]. Hence, the development of lowcomplexity RAB approaches has been a very active research topic in recent years. Nevertheless, a major cause of performance degradation in adaptive beamforming is the presence of the desired signal component in the training data, especially at high SNR. To address this issue, many works tried to remove the signal-

To address this issue, many works tried to remove the signalof-interest (SOI) components by reconstruction of the interferenceplus-noise covariance (IPNC) matrix instead of the sample covariance matrix (SCM). In [16], the IPNC matrix is reconstructed by integrating the nominal SV and the corresponding Capon spectrum over the entire angular sector except the region near the SOI. Several categories of IPNC matrix-based beamformers were then proposed, such as the beamformer in [17], which relies on a correla tion coefficient method, the computationally efficient algorithms via low complexity reconstruction in [18, 19,20], subspace-based algorithms [21,22,23,24], an approach based on spatial power spectrum sampling (SPSS) [25], and the algorithm in [26] which constructs using an IPNC matrix directly from the signal-interference subspace.  The robust beamformer in [27] utilizes the orthogonal subspace (OS) to eliminate the component of the SOI from the angle-related bases while in [28] a robust beamformer is proposed based on the ple of maximum entropy power spectrum (MEPS) to reconstruct the IPNC and the desired signal covariance matrices princi - This paper is structured as follows. Section 2 introduces the system model and states the problem: Section 3 presents the proposed LCSSP method. Section depicts and discusses the simulation results, whereas Section 5 draws the conclusions In this   paper; we develop an effective RAB approach that achieves nearly optimal performance by addressing the inaccurate covariance matrix construction   problems with less  computations than other approaches in the literature . The essence of the idea is based on IPNC matrix reconstruction using low-complexity spatial sampling process (LCSSP) and employing virtual sensors.  The power spectrum sampling is realized by a proposed projection matrix in higher dimension In contrast to previously reported works with IPNC construction; we avoid the reconstruction and estimation of the IPNC matrix by integrating over the angular sector of the interference-plus-noise region Simulation results are presented to verify the effectiveness of the proposed method while requiring less computational complexity.

# 2. PROBLEM BACKGROUND

Consider a linear antenna array of M sensors with interelement spacing d . The data received at the t th snapshot depicted as x ( t ) = x s ( t ) + x i ( t ) + x n ( t ) which is modeled by

$$
p=1
$$

where P is the number of interfering signals. s ( t ) , i p ( t ) and x n ( t ) denote the desired signal, interference signal waveform and noise components, respectively. Assume that the desired signal, interference, and noise are statistically independent from each other. θ s , θ p denotes the direction of the desired signal and the p th interference, respectively. The vector a ( · ) is the corresponding SV, which has the form a ( θ ) = 1 √ M   1 , e j 2 π ¯ d sin θ , · · · , e j 2 π ( M − 1) ¯ d sin θ   T , where ¯ d = d/λ =1/2, λ is the wavelength, and ( · ) T denotes the transpose. Assuming that the SV a ( θ s ) is known, then for a given beamformer weight vector w , the beamformer performance is measured by the output signal-to-interference-plus-noise ratio (SINR) as follows

$$
SINR 02|wHa(0s)12 /wHRi+nW,
$$

where σ 2 s is the desired signal power, R i+n = R i + R n is the IPNC matrix and ( · ) H stands for Hermitian transpose. Assuming that the

