# A. Filter Intensities and their Respective Parameters

In Section 4.1 we introduce abstract levels of intensities for each ﬁlter we apply to an image. We now map each intensity to actual parameters passed to editing libraries to achieve the given ﬁlter intensity.

<table>
  <tr>
    <th> </th>
    <th>Distortion</th>
    <th>Intensity</th>
    <th>Actual Parameters</th>
  </tr>
  <tr>
    <td>]</td>
    <td>JPEG compression Defocus blur Motion blur Pixelate Gaussian noise Impulse noise</td>
    <td>[0, 44, +5] [0, +4, +5] [0, +4, +5] [0, 44, +5] [0, +4, +5] [0,</td>
    <td>The editing library accepts the technical intensities as is_</td>
  </tr>
  <tr>
    <td> </td>
    <td>Brightness Contrast Saturation Exposure Shadows Highlights Temperature Tint Vibrance</td>
    <td>[-5, -4 [-5, -4 44,+5] [-5,-4, [-5, -4 44,+5] [-5,-4 +2, +3] [-3,-2 44,+5] [-4,-3 +4, +5] [-5, -4 [-2, -1,</td>
    <td>[1.0, -0.8 0.8, 1.0] [-1.0, -0.8, 0.8, 1.0] [-3.0, -2.4, 2.4, 3.0] [~100, 60, 20, 20, 40, 50, 60, 80,100] [-100, -80, ~20, 20, 60,100] [0.75,0.8, 1.2,1.25] [0, 20, 25, 40, 60, 80, 100]</td>
  </tr>
  <tr>
    <td> </td>
    <td>Rotation Horizontal crop Vertical crop Left Diagonal crop Right Diagonal crop Image Ratio</td>
    <td>[-5, -4 44,+5] [-5,-4, [-5,-4, 44,+5] [-5,-4, +4, +5] [-5,-4 44,+5] [-5,-4, +4, +5]</td>
    <td>We resize the image to 336px and then crop patches of size 224px from the resulting image. Intensity 0 is a centercrop; while a lintensityl 5 results in a crop from the images border. [stretch along y-axis 100 %, y8O %, x80 %, stretch along x-axis 100 %]</td>
  </tr>
</table>


Table 3. Actual parameters and implementation speciﬁcs for each distortion and intensity level. Technical parameters are passed to imagenet-c [ 12 ] and style parameters to darktable [ 37 ] while compositional distortions are implemented by us.

# B. Dataset Content Analysis

To show that the images of our dataset (Section 4.2) contain a large variety of contents, we apply a pretrained DenseNet121 [ 16 ] for image classiﬁcation and RetinaNet [ 25 ] for object detection on our newly introduced dataset. We ﬁnd that the images of our dataset spread across many different classes and contain a wide variety of objects and subjects.

<table>
  <tr>
    <th colspan="2">most common classes</th>
    <th colspan="2">most common objects</th>
  </tr>
  <tr>
    <td>class</td>
    <td>count</td>
    <td>object</td>
    <td>count</td>
  </tr>
  <tr>
    <td>seashore</td>
    <td>3554</td>
    <td>person</td>
    <td>44301</td>
  </tr>
  <tr>
    <td>alp</td>
    <td>2568</td>
    <td>car</td>
    <td>3186</td>
  </tr>
  <tr>
    <td>lakeside</td>
    <td>2446</td>
    <td>cup</td>
    <td>2880</td>
  </tr>
  <tr>
    <td>fountain</td>
    <td>2265</td>
    <td>bird</td>
    <td>2788</td>
  </tr>
  <tr>
    <td>valley</td>
    <td>2011</td>
    <td>cell phone</td>
    <td>1749</td>
  </tr>
  <tr>
    <td>miniskirt gown</td>
    <td>1455</td>
    <td>boat dog</td>
    <td>1618</td>
  </tr>
  <tr>
    <td>gown</td>
    <td>1430</td>
    <td>dog</td>
    <td>1580</td>
  </tr>
  <tr>
    <td>bikini</td>
    <td>1176</td>
    <td>potted plant</td>
    <td>1580</td>
  </tr>
  <tr>
    <td>sloth bear</td>
    <td>2</td>
    <td>refrigerator</td>
    <td>31</td>
  </tr>
  <tr>
    <td>affenpinscher</td>
    <td>2</td>
    <td>snowboard</td>
    <td>25</td>
  </tr>
  <tr>
    <td>patas</td>
    <td> </td>
    <td>1 skis</td>
    <td>23</td>
  </tr>
  <tr>
    <td>Sealyham_terrier</td>
    <td> </td>
    <td>hair dryer</td>
    <td>7</td>
  </tr>
  <tr>
    <td>Japanese_spaniel</td>
    <td> </td>
    <td>toaster</td>
    <td>7</td>
  </tr>
</table>


Table 4. Most commonly detected classes and objects in the images of our dataset.

Full list: https:/ /github _ com/ janpf/ self-supervised-multi-task-aesthetic-pretraining

