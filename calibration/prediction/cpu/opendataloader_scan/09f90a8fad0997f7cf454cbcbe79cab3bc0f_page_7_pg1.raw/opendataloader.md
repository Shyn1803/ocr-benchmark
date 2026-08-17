# 5 Evaluation

Both qualitative and quantitative evaluation of the integration of surface text-based and knowledgebased methods for Q/A is imposed. Quantitatively; Table 3 summarizes the scores obtained when only shallow methods were employed, in contrast with the results when knowledge-based methods were integrated. We have separately measured the effect of the integration of the knowledge-based methods at question processing and answer processing level. We have also evaluated the precision of the SyS tem when both integrations were implemented. The results were the first five answers returned within 250 bytes of text, when approximatively half million TREC documents are mined. We have used the 200 questions from TREC-8, and the correct answers provided by NIST. The performance was measured both with the NIST scoring method employed in the TREC-8 and by simply assigning a score of 1 for the question having a correct answer, regardless of its position.

<table>
  <tr>
    <th> </th>
    <th>Percentage of correct answers in top 5 returns</th>
    <th>NIST score</th>
  </tr>
  <tr>
    <td>Text-surface-based</td>
    <td>77.79</td>
    <td>64.59</td>
  </tr>
  <tr>
    <td>Knowledge-based Question Processing (only</td>
    <td>83.29</td>
    <td>71.59</td>
  </tr>
  <tr>
    <td>Test-surface-based only with Answer Justification</td>
    <td>77.7%</td>
    <td>739</td>
  </tr>
  <tr>
    <td>Knowledge-based Question Processing with Answer Justification</td>
    <td>89.59</td>
    <td>84.759</td>
  </tr>
</table>


Percentage of

NIST score

correct answers

in top

5 returns

Text-surface-based

77.79

64.59

Knowledge-based

83.29

71.59

Question Processing

(only

![](<09f90a8fad0997f7cf454cbcbe79cab3bc0f_page_7_pg1_images/imageFile1.png>)

739

Test-surface-based

77.7%

Answer

only with

Justification

Knowledge-based

89.59

84.759

Question Processing

with Answer

Justification

Table 3: Accuracy performance

When   using the NIST scoring method to evaluate an individual answer , we only six answer $ question obtains. If the first answer is correct, it obtains a score of 1, if the second one is correct, it is scored with .5 if the third one is correct, the score becomes   .33, if the fourth is correct; the score is 25 and if the fifth one is correct, the score is 2 . Otherwise; it is scored with 0. No credit is given if multiple answers are correct_ Table 3 shows that both knowledge-based methods enhanced the precision; regardless of the scoring method. used

To further evaluate the contribution of the justification option; we evaluated separately the precision of the prover for those questions for which the surface-text-based methods of our system, when op erating alone; cannot find correct answers. We had 45 TREC-8 questions for which the evaluation of the prover was performed. Table 4 summarizes the accuracy of the prover Qualitatively; we find that the integration of knowledge-based methods is very beneficial . Table 2 illustrates   the correct answer  obtained  with these methods; in contrast to the incorrect answer provided when only the shallow techniques are applied.

<table>
  <tr>
    <th> </th>
    <th>Proven correct</th>
    <th>Proven incorrect</th>
    <th>Precision</th>
  </tr>
  <tr>
    <td>Incorrect answers (no knowledge)</td>
    <td>3</td>
    <td>210</td>
    <td>98.59</td>
  </tr>
  <tr>
    <td>Correct answers (KB-based)</td>
    <td>127</td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td>Incorrect answers KB-based)</td>
    <td> </td>
    <td>38</td>
    <td>90.04%</td>
  </tr>
</table>


Table 4: Prover performance

# 6 Conclusions

We believe that the performance of a Q/A system depends on the knowledge sources it employs. In this paper we have presented the effect of the integration of knowledge derived from   question taxanswer justifications on the Q/A precision. Our knowledge-based methods are lightweight, since we do not generate precise semantic representations of questions or answers; but mere approximations   determined by syntactic de pendencies. Furthermore; our prover   operates on very simple logical representations; in which syntactic and semantic ambiguities are completely ignored. Nevertheless; we have shown that these approximations are functional, since we implemented a prover that justifies answers with high precision. Similarly; our knowledge-based question processing is a mere combination of word class information and syntactic dependencies.

# References

Michael Collins. New Statistical Parser Based on Bigram Lexical   Dependencies_ In Proceedings of the 34st Annual Meeting of the Association for Computational Linguistics , ACL-96, pages 184-191, 1996.

Christiane Fellbaum (Ed) WordNet An Electronic Lexical Database_ MIT Press, 1998

Hobbs_ Discourse and Inference Unpublished manuscript, 1986 Jerry

R Hobbs. Overview of the TACITUS Project _ In Computational Linguistics; 12:(3) , 1986 Jerry

Jerry   Hobbs, Mark Stickel Doug   Appelt, and Paul Mar tin. Interpretation as abduction Artificial Intelligence; 63, pages 69-142, 1993.

Wendy LehnertThe processing of question answering. Lawrence Erlbaum Publishers, 1978.

Marius Pasca, Rada Mi halcea; Richard Goodrum; Roxana and Vasile Rus_ Lasso: a tool for the answer net. In Proceedings of TREC-8. 1999 Girju surfing

Ellen Riloff and Rosie Jones.  Learning Dictionaries for Infor mation Extraction by Multi-Level Bootstrapping In Proceedings of the telligence; AAAI-99, 1999.

