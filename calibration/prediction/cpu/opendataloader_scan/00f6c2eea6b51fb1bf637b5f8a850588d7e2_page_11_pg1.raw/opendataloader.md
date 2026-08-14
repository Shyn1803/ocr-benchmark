![](<00f6c2eea6b51fb1bf637b5f8a850588d7e2_page_11_pg1_images/imageFile1.png>)

Training Loss and Accuracy

Training Loss and Accuracy

Training Loss and Accuracy

1

1

Train_loss

Train_loss

Trainoss

Test_loss

Test_loss

Test_loss

Epoch Number

Epoch Number

Epoch Number

(a) First level (visual video)

(b) Second level (audio)

Third level (whole multimodal video)

Fig. 7.   The accuracy and loss curves of the proposed deepfake video detection method on training and validation sets.

![](<00f6c2eea6b51fb1bf637b5f8a850588d7e2_page_11_pg1_images/imageFile2.png>)

ắ

TP= 94

FP= 3

TP= 97

FP= 0

TP= 125

FP= 2

Deepfake

Deepfake

Deepfake

1

1

1

TN= 105

FN=5

TN= 100

TN= 72

FN= 3

Genuine

Gcnuinc

Gcnuinc

Actual labels

Actual labels

Actual labels

First level (visual video)

(b) Second levcl (audio)

Third levcl (whole multimodal vidco)

Fig. 8.   The confusion matrix visualization of the proposed deepfake video detection method.

![](<00f6c2eea6b51fb1bf637b5f8a850588d7e2_page_11_pg1_images/imageFile3.png>)

1

1

1

AUROC=0.9845

AUROC 0.9762

AUKOC

0,9721

0,00

0,75

100

0.00

10o

0,25

0,50

0.50

0.75

000

0,25

0,50

Specificity

1-Specificity

Specificity

(a) First lcvcl (visual vidco)

Third lcvcl (wholc multimodal vidco)

(b) Sccond lcvcl (audio)

Fig. 9.   The ROC curve and the AUROC curve of the proposed deepfake video detection method performance.

![](<00f6c2eea6b51fb1bf637b5f8a850588d7e2_page_11_pg1_images/imageFile4.png>)

100.002

80.00*

40.002

40.0026

40.00%

20.0036

Precision

Recall

F-score

Precision

Recall

F-score

Specificity

0.00*

Recall

Precision

F-scorc

Experiment 1 (The proposed method for the second level; audio)

(The proposed method for the third level: whole multimodal video)

Experiment

Mel-frequency cepstrum (MFC)+ VGG16 [60]

Ensemble Soft/ hard voting based VGG16 [60]

(The proposed method for the first level; visual videos)

Experiment

VGG16 [60]

MFC+ Xception [60]

Two CNN blocks {one per modality) [60]

Xception [7]

Xception [7]

CQT

MobileNet (14]

(a) First level (visual video)

(c) Third level (whole multimodal video)

(b) Second level (audio)

Fig. 10.   The evaluation metrics of the proposed deepfake video detection method compared to recent state-of-the-art methods on the FakeAVCeleb dataset.

# C ONCLUSION AND F UTURE W ORK  

newly smart system for detecting video deepfakes has been presented. Two methods were proposed to extract features These methods produced useful spatial information for visual video and valuable   time-frequency information for   audio; which improved  the performance of the deepfake detection method. In addition; the feature representations of both modalities were passed into mid-layer to produce an informative bimodal representation per video. It proved  that using   bimodal information   boosts   learning   during   training compared to the method that ignores intercorrelation between modalities. The GRU-based   attention mechanism was then applied to the different feature representations  to extract the most significant temporal information and detect the

