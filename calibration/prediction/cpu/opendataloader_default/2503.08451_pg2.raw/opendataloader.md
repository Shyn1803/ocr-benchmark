10x slower to train [10]. Therefore, subsequent works focused on convolutional neural network based blocks, which are faster to train. However, recently there is renewed interest in efficient RNNs and state space models both of which aim to address the inefficiencies of traditional RNNs. These newer developments aim to combine the sequential processing capabilities of RNNs with improved computational and memory efficiency, making them viable for longer sequences and higher throughput requirements. Key advancements include: 1.) State Space Models (SSMs): Recent models like S4 (Structured State Space for Sequence Modeling) [16] and its variants propose replacing traditional recurrent operations with structured linear systems that can process sequences in parallel while retaining the ability to model long-range dependencies. By leveraging the mathematical properties of state space representations, these models reduce the need for sequential backpropagation, offering significant speed and memory improvements. These efforts culminated in the recently introduced S6 model [17], which uses a specific Mamba block around the SSM core, gaining considerable attention due to its strong performance on sequential tasks. 2.) Work on parallelization of RNNs: where [18] linearized and diagonalized the recurrence; whereas [19] built on improving the LSTM model; and [20] introduced a new minimal version of GRUs and LSTMs, called minLSTM and minGRU.

In this work, we analyze the minGRU model for its use in the Turbo autoencoder structure. For that we combine it with the Mamba block for SSMs and integrate it into the parallel Turbo structure of the encoder. We will show that it matches and at times outperforms the convolutional network performance, while being as fast to train as the convolutional networks for smaller sequence length, and having significant advantages at long block lengths.

a) Notation: In this work, we distinguish between random vectors in the communication model and deterministic vectors in the neural network: an n-dimensional random vector is denoted by an uppercase letter with a superscript, e.g. Xn, whose components are X1,X2,..., and whose realized value is xn. In contrast, neural-network vectors are written in bold lowercase with a time subscript, e.g. xt, to represent the input at time t in a recurrent model. For example, Xn corresponds to a random codeword of length n transmitted over the channel (Section III), whereas xt is the deterministic input signal at time t in the MinGRU-based block (Section II).

II. MINGRU-BASED BLOCK

A. Introduction to Recurrent Neural Networks and Gated Recurrent Units

Recurrent Neural Networks (RNNs) are a class of neural networks designed to process sequential data by maintaining a hidden state that captures information about previous inputs. Unlike feedforward neural networks, RNNs share parameters across time steps, enabling them to model temporal dependen-

cies effectively. Formally, given an input sequence {xt}Tt=1, the hidden state ht at time t is computed as:

# ht = f(ht−1,xt;θ), (1)

where f is a non-linear function (e.g., a combination of matrix multiplications and activation functions), ht−1 is the hidden state from the previous time step, xt is the input at time t, and θ are the network parameters.

One of the key challenges in training RNNs is the vanishing/exploding gradient problem, which limits their ability to capture long-term dependencies. Gated architectures like the Gated Recurrent Unit (GRU) were introduced to address this limitation.

B. Gated Recurrent Unit (GRU)

The GRU is a simplified yet effective variant of the Long Short-Term Memory (LSTM) network. It uses gating mechanisms to control the flow of information, which helps in preserving long-term dependencies and mitigating the vanishing gradient issue. The GRU maintains a single hidden state ht, updated as follows:

- 1) Update Gate: The update gate zt determines how much of the past hidden state ht−1 should be retained:

zt = σ(Wzxt + Uzht−1 + bz),

where σ is the sigmoid activation function, and Wz,Uz,bz are learnable parameters.

- 2) Reset Gate: The reset gate rt controls how much of the past hidden state should influence the current computation:

rt = σ(Wrxt + Urht−1 + br).

- 3) Candidate Hidden State: A candidate hidden state h˜t is computed using the reset gate:

h˜t = tanh(Whxt + Uh(rt ⊙ ht−1) + bh), where ⊙ denotes the element-wise product.

- 4) Final Hidden State: The final hidden state ht is a convex combination of the previous hidden state and the candidate hidden state, weighted by the update gate:


# ht = (1 − zt) ⊙ ht−1 + zt ⊙ h˜t.

Neglecting the bias terms, and streamlining the matrices as linear operations Lineard

with a certain matching hidden dimension dh, a GRU cell has the following simplified form:

h

# zt = σ(Lineard

# ([xt,ht−1])) rt = σ(Lineard

h

# ([xt,ht−1])) h˜t = tanh(Lineard

h

# ([xt,rt ⊙ ht−1])) ht = (1 − zt) ⊙ ht−1 + zt ⊙ h˜t.

h

