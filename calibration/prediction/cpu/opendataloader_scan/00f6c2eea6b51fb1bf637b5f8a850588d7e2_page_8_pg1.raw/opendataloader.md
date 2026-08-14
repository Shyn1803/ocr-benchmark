- 3)   Bimodal information-based video features: The deep extracted features from visual video frames and audio modalities using the above-mentioned unimodality-based feature extraction methods are mid-fused at a concatenate layer. This produces a feature vector representation for the whole video, which is based on bimodal information.
- 4)   Temporal information extraction-based attention mechanism: Most deepfake videos are generated based on synthesizing faces frame-by-frame, cloning voices, and synchronizing lips. They suffer from flickering and discontinuity of the face frames and lack of normal emotions, breathing, pauses, and the pace at which the target subject speaks among audio segments. As a result, the GRU-based attention mechanism is applied to the three levels of the extracted features independently; visual video frames, audio, and the whole video. This aims to capture the instructive temporal information that helps to differentiate real videos from fake ones.


The GRU architecture is composed of two gates; update (   ) and reset (   ), that modulate the information flow from the previous time step to the current step. At each time step   , the update gate decides the amount of previous information that should be retained, and the reset gate determines the amount of information that needs to be forgotten [53]. The GRU hidden state   at the time   is defined by the following formulae [54]:

$$
updt = (3)
$$

$$
rest = S(WresXt + Uresht-1)
$$

$$
ht (5)
$$

$$
ht = (1 _ updt) ht + updt ht-1 (6)
$$

where   refers to the input, and   and   represent the weight matrices. The symbol ( ) represents the sigmoid function, ( ) represents the Hyperbolic Tangent,   denotes the Hadamard product, and     ́ denotes the candidate hidden state. As can be seen in Fig. 4, a single GRU is applied to the above-mentioned feature representations on the three levels. It produced a matrix of hidden state vectors at each time step   , which represents the learned temporal information per visual video, audio, or the whole video. The hidden state vector is defined as follows:

$$
[h1, h2, ht]
$$

The attention mechanism uses the weights to concentrate on the important features from the input sequence   . It is defined by the following equations [17, 55]:

$$
Ut tanh(Wht + b) ) (8)
$$

$$
alphat = softmax(ut) (9)
$$

$$
alphatht 10)
$$

$$
V = 11)
$$

where ut is result of feeding hidden vector ht into single-layer Multi-Layer   Perceptron   (MLP) with the tanh activation function: W represents the   weight   matrix;   and b refers to the   bias term. The   symbol alphat represents the normalized attention weights that are produced by applying the softmax layer to Ut: v is video representation that is formed by summing hidden vectors ht weighted by attention weights alphat:

# C.   Classification  

After the instructive temporal features are produced from the GRU-based attention mechanism, a fully connected layer is used as an output layer with two classes. Softmax function is used to decide deepfake videos from real ones. The Softmax formula is defined as follows:

$$
Softmax Zj e (12)
$$

where     denotes the values resulting from the output layer neurons.

# D.   Dataset

The proposed method has been evaluated on the FakeAVCeleb multimodal videos dataset. This dataset consisted of 490 celebrity genuine videos that were selected from the VoxCeleb2 dataset based on various ethnic groups, gender, and age. Its genuine videos are face-centered and cropped. The fake videos of the FakeAVCeleb dataset were generated using DeepFaceLab, Faceswap, and FSGAN, while fake audios were generated using a real-time voice cloning tool (SV2TTS). Additionally, the Wav2Lip was applied to the deepfake videos to re-enact these videos based on the cloned audios. Thus, the FakeAVCeleb dataset had more realistic deepfakes. The FakeAVCeleb was divided into four groups; genuine visual videos with genuine audios, genuine visual videos with deepfake audios, deepfake visual videos with genuine audios, and deepfake visual videos with deepfake audios [4].

To evaluate the proposed method, 1215 genuine and deepfake videos of the FakeAVCeleb dataset are employed. These videos are divided into three subsets: training, validation, and testing.

# IV.   E XPERIMENTAL R ESULTS AND A NALYSIS  

The proposed deepfake video detection method is evaluated by the FakeAVCeleb dataset. Its performance is assessed using the following evaluation metrics [56]:

$$
True_Positives precision True_Positives +False_Positives (13)
$$

$$
True_Positives sensitivity = recall (14) True_Positives +False_Negatives
$$

$$
2xprecisionxrecall F1 score = (15) precision+recall
$$

True_Positives+True_Negatives accuracy True_Positives+True_Negatives+False_Negatives+False_Positives (16)

$$
True_Negatives specificity True_Negatives+False_Positives (17)
$$

$$
sensitivity((1 Specificity) -1 (x) )dx AUROC = Jo (18) = p(xz > X1)
$$

