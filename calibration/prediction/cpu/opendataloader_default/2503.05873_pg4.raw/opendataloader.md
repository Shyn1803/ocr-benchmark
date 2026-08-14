4

scheme as well. After the encryption, the size of the seed used to compress each of files is 3.27[KB]. The encrypted seed is stored on the second server. The rest of the files are stored over the rest of the servers, s.t. each server stores one file. This hybrid scheme is secured against both IT and CryptoEve’s. The overall data rate of the proposed scheme is 0.79.

4) Finally, we assess the computational complexity of the proposed communication scheme. Complexity is measured in this paper, as the number of binary operations required to perform encoding and decoding of all the messages. We show that NU-HUNCC, which encrypts only a subset of links using McEliece, exhibits a more efficient run-time complexity compared to NUM. NU-HUNCC’s efficiency makes it a promising candidate for practical applications.

The remainder of this paper is structured in the following manner. Sec. II presents NU-HUNCC setting, while Sec. III provides the comprehensive security definitions for IS and ISS-CCA1. In Sec. V, we introduce the encoding/decoding algorithm for NU-HUNCC. In Sec. VI, we provide the key findings and theorems of this paper. Sec. VII offers numerical results demonstrating the performance of NU-HUNCC. The proofs of the theorems provided in the paper are given in Sec. VIII, IX, X, and Appendixes A and B. We conclude the paper is Sec. XI.

II. SYSTEM MODEL

We consider a communication system where Alice wishes to transmit ℓ non-uniform confidential message3 over ℓ noiseless links, L = {1,...,ℓ}, to Bob, in the presence of an eavesdropper, Eve. The messages are taken from a DMS (V,pV ) s.t. V ∈ {0,1}. We denote the source message matrix by V L ∈ Fℓ2×n when n is the size of each source message.

Bob’s observations are denoted by Y L. Those observations, provide Bob reliable decode V L with high probability. That is, P(VˆL(Y L) ̸= V L) ≤ ϵe, where VˆL(Y L) is the estimation of V L. We consider two types of Eve: 1) IT-Eve, which observes any subset W ⊂ L of the links s.t. |W| ≜ w < ℓ, but is computationally unbounded, and 2) Crypto-Eve which observes all the links, but is bounded computationally. We denote IT-Eve’s observations by ZW and Crypto-Eve’s observations by ZL.

III. SECURITY DEFINITIONS

In this section, we provide the formal security definitions used throughout this paper.

A. Security against IT-Eve

Against IT-Eve, we consider information-theoretic security. For any subset of ks < ℓ − w source messages, we use the notion of ks individual security (ks-IS). We measure the leakage of information to the eavesdropper using nonnormalized variational distance, denoted by V(·,·). Additionally, we require the code to be reliable where the reliability is measured by the decoding error probability at Bob’s. For a

3In this paper, we assume the messages are independent to focus on the key methods and results. However, our proposed solution can be easily shown to be valid for dependent sources by using joint source coding schemes [54].

code to be ks-IS we require the information leakage and error probability to be negligible. We now formally define ks-IS:

Definition 1. (ks Individual Security) Let V L ∈ Fℓq×n be a set of ℓ confidential source messages Alice intends to send, Y L be Bob’s observations of the encoded messages, and ZW be IT-Eve’s observations of the encoded messages. We say that the coding scheme is ks-IS if:

# 1) Security: ∀ϵs > 0, ∀W ⊂ L s.t. |W| = w < ℓ, and ∀V K

⊂ V L s.t. |Ks| = ks < ℓ − w, it holds that V(pZ

s

) ≤ ϵs.

W|V Ks=vKs,pZ

W

# 2) Reliability: ∀ϵe > 0 it holds that P(VˆL(Y L) ̸= V L) ≤

ϵe, where VˆL(Y L) is the decoding estimation of the message matrix from Bob’s observations.

Thus, IT-Eve that observes any subset of w links in the network can’t obtain any information about any set of ks < ℓ− w individual messages, V K

. However, IT-Eve might be able to obtain some insignificant information about the mixture of all the messages. Yet, this negligible information is controlled [12], [55], [56]. Bob can reliably decode the message matrix from his observations of the encoded messages.

s

B. Security against Crypto-Eve

Crypto-Eve may perform passive/active attacks against Alice and the ciphertexts she produces, to obtain information about confidential messages. Two of the most common attacks given in the literature are the chosen-plaintext attack (CPA) and the chosen-ciphertext attack (CCA) [57]. In both attacks, Crypto-Eve is given a ciphertext from which she tries to obtain information about the plaintext. In CCA Crypto-Eve is active and prior to receiving the ciphertext, she can question a decryption oracle to provide her the plaintexts for a limited number of ciphertexts of her choice. However, she can’t use this decryption oracle after receiving the test ciphertext [57]. The information leakage is measured by Crypto-Eve’s ability to distinguish between plaintexts given the test ciphertext provided by Alice. There are two ways in which this leakage is measured: 1) indistinguishability (IND) - by observing a ciphertext created from one of two possible plaintexts, CryptoEve can’t distinguish between the two plaintexts better than a uniform coin-toss, 2) semantic security (SS) - by observing a ciphertext, Crypto-Eve can’t obtain any information about the original plaintext or some function applied on it, that is more significant than the information she obtains from the plaintexts original probability distribution. Those two definitions are equivalent, i.e. a cryptosystem that is IND is also SS and vice versa [1]. The security level of a cryptosystem is defined by the combination of Crpyto-Eve’s attack model and its information leakage.

In this paper, we introduce a new notion of security, individual semantic security against a chosen ciphertext attack (ISS-CCA1). This notion of security is based on SS-CCA1 cryptographic security [1], [57], and usually requires the encryption scheme to be probabilistic4. To properly define ISS-

4 To focus on our main contributions, we choose to work with public key encryption schemes, but any other PQ probabilistic encryption schemes would have achieved similar results.

