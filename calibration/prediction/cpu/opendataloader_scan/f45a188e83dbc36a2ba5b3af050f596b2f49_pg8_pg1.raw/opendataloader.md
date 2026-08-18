member of New Right political party from Germany

![](<f45a188e83dbc36a2ba5b3af050f596b2f49_pg8_pg1_images/imageFile1.png>)

classiﬁer: N

classiﬁer:

R

-0.048

0.014

0.029

+0.10

-0.10

-0.013

0.025

Figure 2: Continuous ranking of differential proﬁles ( cf. Section 4.1 ). Position on the scale indicates the ranking score as given in Equation ( 3 ), based on optimal parameters k =4 and   =5. The marked data point is assigned different categories by ranking and classiﬁcation models ( cf. discussion in Section 4.2.2 ).

<table>
  <tr>
    <th> </th>
    <th colspan="3">Lexical Features</th>
    <th colspan="3">Emotion Features</th>
    <th colspan="3">Pattern Features</th>
  </tr>
  <tr>
    <td> </td>
    <td>P</td>
    <td> </td>
    <td> </td>
    <td>P</td>
    <td>R</td>
    <td>F1</td>
    <td> </td>
    <td>R</td>
    <td>F 1</td>
  </tr>
  <tr>
    <td>discrete unbalanced discrete</td>
    <td>0.79</td>
    <td>0.85</td>
    <td>0.85</td>
    <td>0.81</td>
    <td>0.38</td>
    <td>0.62</td>
    <td>1.00</td>
    <td>0.08</td>
    <td>0.14</td>
  </tr>
  <tr>
    <td>discrete decoding balanced (k=10, 0=10)</td>
    <td>0.80</td>
    <td>0.62</td>
    <td>0.62</td>
    <td>0.70</td>
    <td>0.20</td>
    <td> </td>
    <td>0.00</td>
    <td>0.00</td>
    <td>0.00</td>
  </tr>
  <tr>
    <td>discrete balanced</td>
    <td>0.69</td>
    <td>0.69</td>
    <td>0.69</td>
    <td>0.69</td>
    <td>0.48</td>
    <td>0.85</td>
    <td>0.63</td>
    <td>0.38</td>
    <td>0.48</td>
  </tr>
</table>


Table 2: Results of analyzing the impact of individual feature groups in the ranking model when being used in isolation (on test set)

First, higher degrees of emotion in language use are clearly associated with category R proﬁles. Individual emotions most strongly associated with one of the categories are surprise, trust and disgust (for right-wing extremists), and love and sadness (for non-extremist users). Second, the most highly weighted pattern features for category R are GEGEN Masseneinwanderung (’mass immigration’), UNSER Politiker (’politicians’), UNSER Fahne (’banner’), GEGEN Syrien (’Syria’) and GEGEN Merkel, whereas UNSER Land (’country’), GEGEN Rechts (’Right-wing’), GEGEN Gebietsreform (’territorial reform’), PRO Aufkl¨ arung (’information’) and UNSER Jugendkandidat*innen (’youth contestants’) are the most indicative patterns of category N.

# 5 Conclusions and Outlook

In this paper, we have presented a ranking model to identify Twitter proﬁles which display traits or attitudes of right-wing extremism. Our work is motivated by the goal of supporting human experts in their monitoring activities which are currently carried out purely manually.

Similarly to standard nearest-neighbour classifi cation approaches, the model is based on estimat - the relative proximity of an unseen profile to a limited number of manually annotated groups of seed profiles in high-dimensional vector space. We apply this model in the two settings of discrete decoding and continuous ranking. Our evaluation shows a significant advantage of the ranking model over a binary classification approach (Har et al., 2017). At the same time, the ranking model is found to deliver plausible predictions for a sample of borderline cases which specifically address actors from New Right political movements in Germany; whose categorization as right-wing ex tremists is currently debated in the social sciences (cf. Zick et al., 2016). ing tung The latter finding clearly deserves a more thor ough investigation based on larger sample of cases, which we would like to address in future work. Additionally; we aim at developing this method further into a learning-to-rank approach in order to enable the comparison of profiles based on development of features that are based on deeper methods of natural language analysis in order to be able to address more fine-grained aspects in the conceptualization of right-wing extremism.

