(100 ms) along the whole speech signal. This process results in a graph of distances with respect to time. The graph is smoothed by a low-pass ﬁltering operation, and then all the signiﬁcant local maxima are searched because they represent potential speaker change points. A local maximum is regarded as signiﬁcant when the differences between its value and those of the minima surrounding it are above a certain threshold, and when there is no higher local maximum in its vicinity. Thus, the local maximum has to fulﬁll the following condition to be signiﬁcant:

|max − minl| > ασ and |max − minr| > ασ,

(2)

where α is a real number, σ is the standard deviation of the distances along the plot, and minl and minr are the left and the right minima, respectively, around the peak max.

# 2.2. Second step: BIC reﬁnement

A ∆BIC value is computed for each potential speaker change point detected in the ﬁrst step to validate or discard this point. The ∆BIC value is given by [3]

∆BIC = −R + λP, (3) where

N 2

log |Σ| −

R =

N1 2

log |Σ1| −

N2 2

log |Σ2| , (4)

λ is a penalty factor which has to be experimentally tuned in order to reduce the number of false alarms without increasing the number of missed detections,

- 1

- 2


P =

- 1

- 2


d(d + 1) log N, (5)

d +

N1 and Σ1 are the number and the covariance matrix of the feature vectors in the window W1, respectively, N2 and Σ2 are the number and the covariance matrix of the feature vectors in the window W2, respectively, N = N1 + N2, Σ is the covariance matrix of the feature vectors of both windows together, and d is the dimension of the feature vectors.

A potential speaker change point is regarded as a true speaker change if the ∆BIC value for this point is negative.

3. Modiﬁed DISTBIC algorithm

The DISTBIC algorithm allows to obtain good speaker change detection results, nonetheless it has some weak points. We have focused on these points and suggest some improvements of the algorithm in order to obtain even better results. The improvements are speciﬁed in next subsections.

# 3.1. Silence and breathing elimination

Silence and breathing may cause a lot of false alarms in speaker change detection tasks. Therefore we used a simple but efﬁcient silence detector before the speaker change detection process. The speech signal was divided into segments the length of which was 10 ms. Short-time energy and the number of zero crossings [4] were computed for each segment. If both the short-time energy and the number of zero crossings were lower than experimentally derived thresholds, the segment was regarded as containing silence and was temporarily eliminated from the utterance.

<table>
  <tr>
    <td>![](<031a888e402c82517f213222ae97147dd7dc_page_2_pg1_images/imageFile1.png>)</td>
  </tr>
</table>


Figure 1: True speaker change points causing troubles (marked with a circle) in the condition (2).

Sometimes short sections with a high energy can occur in silent parts of the utterance. Such sections can be caused for example by the speaker breathing. The high energy impels the silence detector to regard these sections as speech. In order to overcome this problem, we implemented a clustering algorithm: if a part of a speech signal shorter than 645 ms was surrounded by silent segments, this part was also regarded as silence. On the contrary, if there was a silent segment shorter than 250 ms between two segments containing speech, this segment was regarded as containing speech.

# 3.2. Speaker change candidate detection

Equally as in Section 2.1, the potential speaker change points were detected on the smoothed graph of the symmetric Kullback-Leibler distance. However, the condition (2) necessary to detect the potential speaker change points was changed. The reason for the change was the fact, that the condition (2) did not allow to detect some local maxima of the graph as the potential speaker change points. The problems were caused mainly by the maxima that were rather near each other, so that the minimum between them was too high to satisfy the condition (2). An example of such a kind of peaks is shown in Figure 1. For that reason the conjunction in (2) was substituted with the disjunction, i.e. a local maximum was regarded as a potential speaker change point if it satisﬁed the condition

|max − minl| > ασ or |max − minr| > ασ,

(6)

where α, σ, minl, minr, and max have the same meaning as before.

In order to avoid the situation that two different maxima belonging in fact to one true speaker change would be detected as two potential speaker change points, we required a minimal distance between two maxima: if two maxima were closer than 0.5 s, the lowest one was discarded. This condition protects the algorithm against false alarms.

# 3.3. Speaker change position location

Having detected the potential speaker change points, we used the ∆BIC value (3) to discard or validate the points similarly

