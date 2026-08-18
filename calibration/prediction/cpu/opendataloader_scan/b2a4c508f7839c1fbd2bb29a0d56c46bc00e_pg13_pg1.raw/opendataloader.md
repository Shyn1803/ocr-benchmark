Table 6. Number of detected ciseQTLs in transcript-wise analysis of three harmonized RNA NGS datasets.

<table>
  <tr>
    <th> </th>
    <th colspan="2">Number of unique genes with cis-eQTLs</th>
  </tr>
  <tr>
    <td> </td>
    <td>Without principal component</td>
    <td>With principal component</td>
  </tr>
  <tr>
    <td>Montgomery et al. (paired-end RNA-seq)</td>
    <td>94</td>
    <td>145</td>
  </tr>
  <tr>
    <td>Pickrell et al. (single-end RNA-seq)</td>
    <td>94 199</td>
    <td>438</td>
  </tr>
  <tr>
    <td>NTR-NESDA transcript-wise (DeepSAGE)</td>
    <td>292</td>
    <td>579</td>
  </tr>
  <tr>
    <td>Meta-analysis</td>
    <td>651</td>
    <td>1,207</td>
  </tr>
</table>


doi:10.1371/journal.pgen.1003594.t006

and environmental effects. As such, compensating for these nongenetic effects would increase the power to detect cis -eQTL effects. To mitigate the effects of non-genetic sources of variability, we first log 2 transformed the data and centered and scaled each tag, and subsequently applied PCA on the sample correlation matrix. We then used the first PCs as covariates, and re-did the nonparametric cis-eQTL mapping on the residual expression data (using the procedure described by [6]).

# Validation of genotype-dependent alternative polyadenylation in RNA-seq datasets The genomic coordinates of the 3 9 -UTR, obtained

The genomic coordinates of the 3'-UTR, obtained from UTRs) according to the position of the DeepSAGE tags with and the Refseq split opposite Expression of short and variants of HPSI and IRF5 was quantified by qRT-PCR, which was performed on a subset of RNA used for the DeepSAGE sequencing: cDNA was synthesized from 400 ng of total RNA using BioScript MMLV Jong samples

position of reported and predicted polyadenylation sites from polyA_DB database. To calculate the coverage in proximal and distal regions in RNA-seq datasets, we created a coverage histogram from each .bam alignment file using coverageBed tool from BEDTools package (version 2.17.0) [39]. Subsequently, a custom Python script was used to convert the histogram in number of nucleotides mapped per region, normalized by the length of the region. The ratio between the number of counts in the proximal region and the distal region was then calculated.

# qPCR validation of alternative polyadenylation

Table 7. Trait-associated SNPs detected in the sequencing-based transcript-wise meta-analysis, but not detected in array-based eQTL dataset of 1,469 peripheral blood samples.

<table>
  <tr>
    <th>SNP name</th>
    <th>Chr.</th>
    <th>Transcript position (midpoint)</th>
    <th>Cis-regulated gene</th>
    <th>Associated trait</th>
  </tr>
  <tr>
    <td>rs1052501</td>
    <td> </td>
    <td>41963564</td>
    <td>ULK4</td>
    <td>Multiple myeloma</td>
  </tr>
  <tr>
    <td>rs347685</td>
    <td> </td>
    <td>141782879</td>
    <td>TFDP2</td>
    <td>Chronic kidney disease</td>
  </tr>
  <tr>
    <td>rs4580814</td>
    <td> </td>
    <td>1081324</td>
    <td>SLC12A7</td>
    <td>Hematological and biochemical traits</td>
  </tr>
  <tr>
    <td>rs4947339</td>
    <td> </td>
    <td>28911984</td>
    <td>C6orf10o</td>
    <td>Platelet aggregation</td>
  </tr>
  <tr>
    <td>rs2517532</td>
    <td> </td>
    <td>31024818</td>
    <td>HCG22</td>
    <td>Hypothyroidism</td>
  </tr>
  <tr>
    <td>rs2844665</td>
    <td> </td>
    <td>31024818</td>
    <td>HCG22</td>
    <td>Stevens-Johnson syndrome and toxic epidermal necrolysis (SJS-TEN)</td>
  </tr>
  <tr>
    <td>rs6457327</td>
    <td> </td>
    <td>31024818</td>
    <td>HCG22</td>
    <td>Follicular lymphoma</td>
  </tr>
  <tr>
    <td>rs3130501</td>
    <td> </td>
    <td>31324124</td>
    <td>HLA-B</td>
    <td>Stevens-Johnson syndrome and toxic epidermal necrolysis (SJS-TEN)</td>
  </tr>
  <tr>
    <td>rs2858870</td>
    <td> </td>
    <td>32434437</td>
    <td>HLA-DRB9</td>
    <td>Nodular sclerosis Hodgkin lymphoma</td>
  </tr>
  <tr>
    <td>rs3129889</td>
    <td> </td>
    <td>32434437</td>
    <td>HLA-DRB9</td>
    <td>Multiple sclerosis</td>
  </tr>
  <tr>
    <td>rs3135388</td>
    <td> </td>
    <td>32434437</td>
    <td>HLA-DRB9</td>
    <td>Multiple sclerosis</td>
  </tr>
  <tr>
    <td>rs477515</td>
    <td> </td>
    <td>32434437</td>
    <td>HLA-DRB9</td>
    <td>Inflammatory bowel disease</td>
  </tr>
  <tr>
    <td>rs9271100</td>
    <td> </td>
    <td>32524134</td>
    <td>HLA-DRB6</td>
    <td>Systemic lupus erythematosus</td>
  </tr>
  <tr>
    <td>rs9273349 6</td>
    <td> </td>
    <td>32632106</td>
    <td>HLA-DQB1</td>
    <td>Asthma</td>
  </tr>
  <tr>
    <td>rs3807989 7</td>
    <td> </td>
    <td>116183034</td>
    <td>CAVI</td>
    <td>PR interval</td>
  </tr>
  <tr>
    <td>rs12680655 8</td>
    <td> </td>
    <td>135604552</td>
    <td>ZFAT</td>
    <td>Height</td>
  </tr>
  <tr>
    <td>rs4929923 11</td>
    <td> </td>
    <td>8642408</td>
    <td>TRIM66</td>
    <td>Menarche (age at onset)</td>
  </tr>
  <tr>
    <td>rs12785878 11</td>
    <td>11</td>
    <td>71161461</td>
    <td>RPI1-660L16.2</td>
    <td>Vitamin insufficiency</td>
  </tr>
  <tr>
    <td>rs12580100 12</td>
    <td>12</td>
    <td>56436876</td>
    <td>RPS26</td>
    <td>Psoriasis</td>
  </tr>
  <tr>
    <td>rs4924410 15</td>
    <td>15</td>
    <td>40329664</td>
    <td>SRP14</td>
    <td>Ewing sarcoma</td>
  </tr>
  <tr>
    <td>rs7364180 22</td>
    <td>22</td>
    <td>42184613</td>
    <td>MEI1</td>
    <td>Alzheimer's disease biomarkers</td>
  </tr>
</table>


doi:10.1371/journal.pgen.1003594.t007

