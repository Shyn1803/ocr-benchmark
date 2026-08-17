and discussed. Section V concludes the paper.

# II. T HE ANALYZED GENERATOR

We analyze the LCT attack on a noised pseudorandom sequence generator involving a primitive known as The Binary Rate Multiplier (BRM). BRM consists of 2 linear feedback shift registers (LFSRs). One of them, the clocking LFSR (LFSR s ), determines the clocking sequence for the clocked LFSR (LFSR u ), see Fig. 1 .

![](<0853d8a05fd1e839887d4bc3004a6770cb7b_page_2_pg1_images/imageFile1.png>)

clk.

LFSR u

LFSR s

positions

k

integer seq.

# Example 1

Fig. 1. The BRM primitive

The BRM operates as follows (Fig. 2 ): Without clocking by LFSR s , the register LFSR u produces the binary sequence u n . At the clock pulse i of LFSR s , the bits from k positions of LFSR s determine the integer s i that represents the number of bits from the sequence u n that are going to be discarded. The integers s i , i = 1 , 2 ,... make the sequence s n . The process of discarding bits in this way is called non-uniform decimation of the sequence u n . The maximum value of the integer s i determines the maximum number of bits from the sequence u n that can be discarded at a time. The binary sequence z n is the output sequence of the whole BRM.

Un

![](<0853d8a05fd1e839887d4bc3004a6770cb7b_page_2_pg1_images/imageFile2.png>)

LFSR u

Non-uniform

Zn

Sn

decimation

LFSR s

{ k positions

Fig. 2. Operation of the BRM

The BRM primitive has become popular in the design of stream ciphers since it can be shown [ 2 ] that the produced sequence z n has extremely long period and high linear complexity preserving at the same time good statistical properties of a single LFSR.

# III. T HE NEW LCT ATTACK

In this section, we give details of the new LCT-based attack against noised BRM. The general description and remarks about LCT have been exposed in the Introduction.  To design an LCT attack BRM, we have to determine   which part of the BRM (which consists of the initial states of LFSRs and LFSRu, as usual) is to be guessed. It is shown in [5] that assigning linear system to BRM when the initial state of LFSRs is guessed is easy. Then the unknowns in the against key system are the bits of the output sequence of LFSRu   without decimation together with the bits of the initial state of the same LFSR and the right-hand side of any equation in the system is the corresponding bit of the intercepted sequence. In our new LCT attack on noised BRM, we use the same approach. We the initial state of LFSRs and make a system of linear equations in the unknowns of the initial state of LFSRu  and the unknown bits of the output sequence of LFSRu   without decimation. The main point of our attack is the algorithm that eliminates the influence of the bits of the intercepted sequence complemented by noise guess Suppose the BRM from Fig. 1 uses 4-bit LFSRs and the primitive   feedback   polynomials  of LFSRs and LFSRu are = 1 + 23 + respectively. Let the number of output of LFSRs be k = 2 and the tap   positions are the first and the second (from the   left) states of   LFSRs be 1010 and 0110, respectively. Then the clocking sequence for LFSRu (ie. the integer sequence Sn and the output sequence of the BRM is 11010110111 taps

s be right, i.e. 1010. In the LCT attack against the generator without noise, the so-called decimation sequence is generated, containing the symbol ’2’ in the positions of the unknown bits. Each symbol ’2’ will correspond to a new variable in the system of equations assigned to the generator. In this case, the decimation sequence will be 2222 | 22212102212011220222122212221 ... . The symbol | delimits the variables of the initial state of the clocked register LFSR u from the rest of the variables. The variables to the left from the symbol | are given in the order x 4 , x 3 , x 2 , x 1 , whereas the variables to the right from the symbol | are given in the increased order of indexing, i.e. x 5 , x 6 , etc. Then the system of linear equations assigned to the given BRM is:

$$
0 0 0 1 0 13
$$

The new ciphertext-only attack against a BRM is described below:

1 . Guess the initial state of the LFSRs.

Set up a system of equations assigned to such a BRM without involving the intercepted bits. Such a system is homogeneous and always consistent.

Set up a system of equations involving only the equations containing the intercepted bits.

4 Join the obtained systems and check the consistency of the joint system. The following cases are possible:

4.1 There is no noise and the right initial state of LFSR s was guessed the joint system will be consistent and

