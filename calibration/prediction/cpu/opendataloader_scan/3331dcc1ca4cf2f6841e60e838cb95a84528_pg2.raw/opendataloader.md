![](<3331dcc1ca4cf2f6841e60e838cb95a84528_pg2_images/imageFile1.png>)

Figure 1. (a). Labelled Original Image (b). Detection by F-RCNN (c). Detection by YOLO

![](<3331dcc1ca4cf2f6841e60e838cb95a84528_pg2_images/imageFile2.png>)

Performance Analysis of F-RCNN

YOLO

and

Ground Trutb

Í

1

14 15 16 17

12 13

18 19 20

Vumber of Images

stage are used as ground truths and F1 score [6] is considered as a performance metric for evaluating model performance. F-RCNN and YOLO have been evaluated for detecting tassel in the images. The 20 images are used to test the performance of models. Fig.1, shows the detection performance of F-RCNN and YOLO. In Fig. 2, tassels count by F-RCNN and YOLO are compared with ground truth. It can be observed that YOLO give count close to ground truth but YOLO has low precision accuracy compared to FRCNN as YOLO misclassify more. From Table 1, it can be observed that F-RCNN model performs better and recognizes the tassel with F 1 score of 0 . 909 compared to YOLO model which has F 1 score of 0 . 878 . Therefore, F-RCNN model used to count the tassel in images of plots and estimate dates for heading and DFPT stages of maize crop. The comparison of manually observed dates and esti-

mated dates by proposed framework for heading and DFPT stages of the maize crop is shown in Table 2. In Table 2, O HS and O DFPTS indicate the manual observation for heading(start of emergance of tassel) and the day to 50% tasseling stages where E HS and E DFPTS represent the dates estimated by proposed framework. Due to limited space, the observations of only nine plots have been included in the table. From Table 2, it can be observed that the model can provide accurate information about crop growth stages. Due to lack of data, it was difﬁcult to pin the exact date for stages. The estimation of dates for different stages have been given in Table 2 based on rate of change in count of tassels. The data should be collected daily during vegetative to reproductive growth stage to predict exact date.

Table 1. Performance Analysis of F-RCNN and YOLO for Detecting Tassels Images F1 Score RCNN F1 Score YOLO

<table>
  <tr>
    <th>Images</th>
    <th>Fl Score_RCNN</th>
    <th>Fl Score_YOLO</th>
  </tr>
  <tr>
    <td> </td>
    <td>0.909090909</td>
    <td>0.909090909</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.857142857</td>
    <td>0.857142857</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.952331063</td>
    <td>0.837209302</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.882306919</td>
    <td>0.842105263</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.823485811</td>
    <td>0.823529412</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.869565217</td>
    <td>0.846153846</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.914285714</td>
    <td>0.838709677</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.909090909</td>
    <td>0.727272727</td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td>0.916666667</td>
  </tr>
  <tr>
    <td> </td>
    <td>1 0.903225806</td>
    <td>0.909090909</td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td>0.846153846</td>
  </tr>
  <tr>
    <td> </td>
    <td>1 0.857142857</td>
    <td>0.833333333</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.857142857</td>
    <td>0.857142857</td>
  </tr>
  <tr>
    <td> </td>
    <td>0.967741935</td>
    <td>0.827586207</td>
  </tr>
  <tr>
    <td> </td>
    <td> </td>
    <td>0.916666667</td>
  </tr>
  <tr>
    <td>17</td>
    <td>1 0.818181818 0.8</td>
    <td>0.916666667</td>
  </tr>
  <tr>
    <td>19</td>
    <td>0.8</td>
    <td>0.857142857</td>
  </tr>
  <tr>
    <td>19</td>
    <td>0.857142857</td>
    <td> </td>
  </tr>
  <tr>
    <td>20</td>
    <td> </td>
    <td> </td>
  </tr>
  <tr>
    <td>FI Score</td>
    <td>0.908893877</td>
    <td>1 0.8780832</td>
  </tr>
</table>


Table 2. Performance Analysis of F-RCNN for Estimating Growth Stages Plots O HS E HS O DFPTS E DFPTS

<table>
  <tr>
    <th>Plots</th>
    <th>Ous</th>
    <th> </th>
    <th>ODFPTS</th>
    <th>EDFPTS</th>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before 17 Dec</td>
    <td>22 Dec</td>
    <td>20 Dec</td>
  </tr>
  <tr>
    <td> </td>
    <td>17 Dec</td>
    <td>Before or on 17 Dec</td>
    <td>23 Dec</td>
    <td>20 Dec+ Or 2 days</td>
  </tr>
  <tr>
    <td> </td>
    <td>17 Dec</td>
    <td>Before 17 Dec</td>
    <td>27 Dec</td>
    <td>1 or 2 days</td>
  </tr>
  <tr>
    <td> </td>
    <td>17 Dec</td>
    <td>Before 17 Dec</td>
    <td>Dec</td>
    <td>20 Dec+ Or 2 days</td>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before 17 Dec</td>
    <td>21 Dec</td>
    <td>Dec</td>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before 17 Dec</td>
    <td>22 Dec</td>
    <td>Dec</td>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before 17 Dec</td>
    <td>21 Dec</td>
    <td>Dec</td>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before or on 17 Dec</td>
    <td>21 Dec</td>
    <td>20 Dec</td>
  </tr>
  <tr>
    <td> </td>
    <td>15 Dec</td>
    <td>Before 17 Dec</td>
    <td>29 Dec</td>
    <td>20 Dec+ days</td>
  </tr>
</table>


# 4. Conclusion

In this study, we have proposed a UAV based remote sensing framework to monitor and estimate growth of tassel which gives information about different growth stagesheading(start of emergence of tassel), DFPT of the maize crop. A CNN based F-RCNN and YOLO models are evaluated for tassel detection from it’s emergence to reproduction stage. F-RCNN with F1 score 0 . 909 provides better detection compared to YOLO which has F1 score of 0 . 878 . Hence, F-RCNN has been used to estimate the heading and DFPT stages of maize crop. From the performance analysis it can be concluded that a UAV based remote sensing framework using F-RCNN can be an alternative way for manual observation of different growth stages of maize crop.

# References

- [1] Kurtulmus¸, Ferhat, and Ismail Kavdir., ”Detecting corn tassels using computer vision and support vector machines.”, Expert Systems with Applications , vol. 41, no. 16, pp. 7390-7397, 2014.
- [2] Lu, H., Cao, Z., Xiao, Y., Li, Y. and Zhu, Y., ”Regionbased colour modelling for joint crop and maize tas-


