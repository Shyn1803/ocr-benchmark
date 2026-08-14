4 S. Petrovic´

and discussed. Section V concludes the paper. II. THE ANALYZED GENERATOR

We analyze the LCT attack on a noised pseudorandom sequence generator involving a primitive known as The Binary Rate Multiplier (BRM). BRM consists of 2 linear feedback shift registers (LFSRs). One of them, the clocking LFSR (LFSRs), determines the clocking sequence for the clocked LFSR (LFSRu), see Fig. 1.

clk.

<table>
  <tr>
    <td>LFSRs</td>
  </tr>
</table>


<table>
  <tr>
    <td rowspan="2">LFSRu</td>
    <td> </td>
  </tr>
  <tr>
    <td> </td>
  </tr>
</table>


k positions

integer seq.

Fig. 1. The BRM primitive

The BRM operates as follows (Fig. 2): Without clocking by LFSRs, the register LFSRu produces the binary sequence un. At the clock pulse i of LFSRs, the bits from k positions of LFSRs determine the integer si that represents the number of bits from the sequence un that are going to be discarded. The integers si, i = 1,2,... make the sequence sn. The process of discarding bits in this way is called non-uniform decimation of the sequence un. The maximum value of the integer si determines the maximum number of bits from the sequence un that can be discarded at a time. The binary sequence zn is the output sequence of the whole BRM.

un

LFSRu

<table>
  <tr>
    <td rowspan="2">Non-uniform decimation</td>
    <td>zn</td>
  </tr>
  <tr>
    <td> </td>
  </tr>
</table>


sn

<table>
  <tr>
    <td>LFSRs</td>
  </tr>
</table>


k positions

{

Fig. 2. Operation of the BRM

The BRM primitive has become popular in the design of stream ciphers since it can be shown [2] that the produced sequence zn has extremely long period and high linear complexity preserving at the same time good statistical properties of a single LFSR.

III. THE NEW LCT ATTACK

In this section, we give details of the new LCT-based attack against a noised BRM. The general description and remarks about LCT have been exposed in the Introduction. To design an LCT attack against BRM, we have to determine which part of the BRM key (which consists of the initial states of LFSRs and LFSRu, as usual) is to be guessed. It is shown in [5] that assigning a linear system to a BRM when the initial state of LFSRs is guessed is easy. Then the unknowns in the

system are the bits of the output sequence of LFSRu without decimation together with the bits of the initial state of the same LFSR and the right-hand side of any equation in the system is the corresponding bit of the intercepted sequence. In our new LCT attack on a noised BRM, we use the same approach. We guess the initial state of LFSRs and make a system of linear equations in the unknowns of the initial state of LFSRu and the unknown bits of the output sequence of LFSRu without decimation. The main point of our attack is the algorithm that eliminates the inﬂuence of the bits of the intercepted sequence complemented by noise.

# Example 1

Suppose the BRM from Fig. 1 uses 4-bit LFSRs and the primitive feedback polynomials of LFSRs and LFSRu are fs(x) = 1 + x + x4 and fu(x) = 1 + x3 + x4, respectively. Let the number of output taps of LFSRs be k = 2 and the tap positions are the ﬁrst and the second (from the left). Let the initial states of LFSRs and LFSRu be 1010 and 0110, respectively. Then the clocking sequence for LFSRu (i.e. the integer sequence sn) is 31021002333... and the output sequence of the BRM is 11010110111...

Let the cryptanalyst’s guess of the initial state of LFSRs be right, i.e. 1010. In the LCT attack against the generator without noise, the so-called decimation sequence is generated, containing the symbol ’2’ in the positions of the unknown bits. Each symbol ’2’ will correspond to a new variable in the system of equations assigned to the generator. In this case, the decimation sequence will be 2222 | 22212102212011220222122212221.... The symbol | delimits the variables of the initial state of the clocked register LFSRu from the rest of the variables. The variables to the left from the symbol | are given in the order x4, x3, x2, x1, whereas the variables to the right from the symbol | are given in the increased order of indexing, i.e. x5, x6, etc. Then the system of linear equations assigned to the given BRM is:

x3 + x4 + x5 = 0 x2 + x3 + x6 = 0 x1 + x2 + x7 = 0 x1 + x5 = 1 x5 + x6 + x8 = 0

.

The new ciphertext-only attack against a BRM is described below:

- 1. Guess the initial state of the LFSRs.
- 2. Set up a system of equations assigned to such a BRM without involving the intercepted bits. Such a system is homogeneous and always consistent.
- 3. Set up a system of equations involving only the equations containing the intercepted bits.
- 4. Join the obtained systems and check the consistency of the joint system. The following cases are possible:


4.1 There is no noise and the right initial state of LFSRs was guessed - the joint system will be consistent and

