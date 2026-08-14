<table>
  <tr>
    <th>(CQT [61] + MobileNet) [14]</th>
    <th>82.67%</th>
    <th>82.38%</th>
  </tr>
</table>


T HE P ERFORMANCE OF THE P ROPOSED M ETHOD FOR D ETECTING W HOLE M ULTIMODAL V IDEO D EEPFAKES C OMPARED TO R ECENT S TATE OF THE ART M ETHODS ON THE F AKE AVC ELEB D ATASET  

<table>
  <tr>
    <th> </th>
    <th colspan="2">Bimodal Visual video and audio</th>
  </tr>
  <tr>
    <td>Model</td>
    <td>Accuracy</td>
    <td>AUCROC</td>
  </tr>
  <tr>
    <td>Experiment 2</td>
    <td>96.04%</td>
    <td>95.49%</td>
  </tr>
  <tr>
    <td>Experiment 3 (The proposed method for the third level:</td>
    <td>97.52%</td>
    <td>97.21%</td>
  </tr>
  <tr>
    <td>Ensemble Soft/ hard voting based VGG16 [60]</td>
    <td>78.04%</td>
    <td>78.05%</td>
  </tr>
  <tr>
    <td>Two CNN blocks (one per modality) [60]</td>
    <td>67.4%</td>
    <td>67.2%</td>
  </tr>
  <tr>
    <td>Xception [7]</td>
    <td>43.94%</td>
    <td>43.73%</td>
  </tr>
</table>


TABLE IV.   T HE GRUBASED A TTENTION M ECHANISM L AYERS D ETAILS  

<table>
  <tr>
    <th>Layer (type)</th>
    <th>Output shape</th>
    <th>Parameters number</th>
  </tr>
  <tr>
    <td>main_input (Input Layer) gru (GRU)</td>
    <td>[(None; 8,4096)]</td>
    <td> </td>
  </tr>
  <tr>
    <td>gru (GRU)</td>
    <td>(None, 3572)</td>
    <td>82191720 3580</td>
  </tr>
  <tr>
    <td>attention (attention)</td>
    <td>(None, 3572)</td>
    <td>3580</td>
  </tr>
  <tr>
    <td>Total parameters: 82,195,300 Trainable parameters: 82,202,446 Non-trainable parameters: 0</td>
    <td> </td>
    <td> </td>
  </tr>
</table>


and the AUROC curve of the proposed method performance. As shown in Fig. 9, the ROC curve is extremely close to the top left ensuring the high performance of the proposed method.

The cross-entropy loss ( ) function is utilized to measure the efficiency of the suggested deepfake video detection method on three levels: video frames, audio, and the whole video. Its formula [59] is defined as follows:

Fig. 10 provides a comparison of the proposed method with contemporary state-of-the-art methods using evaluation metrics. As shown in Fig. 10, the proposed method has yielded better performance in comparison to the other methods on the three levels. It has a precision of 96.91%, recall of 100%, F1score of 98.43%, and specificity of 97.22% for detecting visual videos. Additionally, it has a precision of 100%, recall of 95.10%, F1-score of 97.49%, and specificity of 100% for detecting audios. Further, it has a precision of 98.43%, recall of 97.66%, F1-score of 98.04%, and specificity of 97.30% for detecting whole multimodal videos.

$$
1 = M ZM1(yk log(pk) + (1 - yk) log(1 pk)) (20)
$$

where   refers to the number of visual videos, audios, or whole videos. The     and     denote the actual label and predicted probability corresponding to the     video. It can be seen in Table III that the proposed method, which represents experiment 3, for whole multimodal video deepfake detection has achieved 97.52% accuracy and 97.21% AUROC. Its performance exceeds that of experiment 2 because experiment 2 is unable to learn intercorrelations between different modalities. Additionally, it outperforms recent state-of-the-art methods by an average growth of 34.4% accuracy and 34.2% AUROC as can be seen in Table III.

It can be concluded that the proposed upgraded XceptionNet generated a useful spatial hierarchical representation of faces, which contributed to distinguishing between genuine and fake videos. As well, the proposed CQTbased modified InceptionResNetV2 produced a valuable deep time-frequency representation of audio. This assisted to reveal deepfake videos and improved the detection method's effectiveness. Moreover, a concatenate layer that is applied to the features extracted from visual video and audio modalities produced an informative bimodal representation of videos. In addition, the GRU-based attention mechanism, which is applied to the visual video, audio, and bimodal features, assisted in capturing the most important temporal information of videos. This in turn helped to detect the deepfakes. Furthermore, it can be inferred that correlating features from different modalities can improve the chances of achieving accurate deepfake video detection.

The experiments are carried out using an OMEN HP laptop with a 16-gigabyte Intel (R) Core (TM) i7-9750H CPU, a 6gigabyte RTX 2060 GPU, and Windows 11. The proposed method is implemented using the Python programming language. Python libraries such as Keras, OpenCV, Random, Tensorflow, Numpy, OS, and Librosa are used during the implementation.

The accuracy and loss curves of the proposed method on the training and validation subsets of the FakeAVCeleb dataset for the three levels; visual video frames, audio, and whole multimodal videos, are shown in Fig. 7. Additionally, the proposed method confusion matrix for deepfake video detection on the three levels is depicted in Fig. 8. Furthermore, Fig. 9 shows the receiver operating characteristic (ROC) curve

