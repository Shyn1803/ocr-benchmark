# A. Filter Intensities and their Respective Parameters

In Section 4.1 we introduce abstract levels of intensities for each ﬁlter we apply to an image. We now map each intensity to actual parameters passed to editing libraries to achieve the given ﬁlter intensity.

Distortion Intensity Actual Parameters

JPEG compression [0, ...+4, +5]

Defocus blur [0, ...+4, +5] Motion blur [0, ...+4, +5] Pixelate [0, ...+4, +5] Gaussian noise [0, ...+4, +5] Impulse noise [0, ...+4, +5]

Technical

The editing library accepts the technical intensities as is.

Brightness [-5, -4, ..., +4, +5] [−1.0, −0.8, ..., 0.8, 1.0] Contrast [-5, -4, ..., +4, +5] [−1.0, −0.8, ..., 0.8, 1.0] Saturation [-5, -4, ..., +4, +5] [−1.0, −0.8, ..., 0.8, 1.0] Exposure [-5, -4, ..., +4, +5] [−3.0, −2.4, ..., 2.4, 3.0] Shadows [-5, -4, ..., +2, +3] [−100, −60, −20, 20, 40, 50, 60, 80,100] Highlights [-3, -2, ..., +4, +5] [−100, −80, −60, −50, −40, −20, 20, 60,100] Temperature [-4, -3, ..., +4, +5] [2000, 3000, 5000, 6000, 6500, 7000, 8000, 10 000, 14 000, 18 000] Tint [-5, -4, ..., +4, +5] [0.75, 0.8, ..., 1.2,1.25] Vibrance [-2, -1, ..., +3, +4] [0, 20, 25, 40, 60, 80, 100]

Style

Rotation [-5, -4, ..., +4, +5] [10◦ , 8◦ , ..., 8◦ , 10◦ ] Horizontal crop [-5, -4, ..., +4, +5]

Composition

We resize the image to 336px and then crop patches of size 224px from the resulting image. Intensity 0 is a centercrop, while a |intensity| == 5 results in a crop from the images’ border.

Vertical crop [-5, -4, ..., +4, +5] Left Diagonal crop [-5, -4, ..., +4, +5] Right Diagonal crop [-5, -4, ..., +4, +5] Image Ratio [-5, -4, ..., +4, +5] [stretch along y-axis 100%, y80%, ..., x80%, stretch along x-axis 100%]

- Table 3. Actual parameters and implementation speciﬁcs for each distortion and intensity level. Technical parameters are passed to imagenet-c [12] and style parameters to darktable [37] while compositional distortions are implemented by us.

B. Dataset Content Analysis

To show that the images of our dataset (Section 4.2) contain a large variety of contents, we apply a pretrained DenseNet121 [16] for image classiﬁcation and RetinaNet [25] for object detection on our newly introduced dataset. We ﬁnd that the images of our dataset spread across many different classes and contain a wide variety of objects and subjects.

most common classes most common objects class count object count seashore 3554 person 44301 alp 2568 car 3186 lakeside 2446 cup 2880 fountain 2265 bird 2788 valley 2011 cell phone 1749 miniskirt 1455 boat 1618 gown 1430 dog 1581 bikini 1176 potted plant 1580 ... ... ... ... sloth bear 2 refrigerator 31 affenpinscher 2 snowboard 25 patas 1 skis 23 Sealyham terrier 1 hair dryer 7 Japanese spaniel 1 toaster 7

- Table 4. Most commonly detected classes and objects in the images of our dataset. Full list: https://github.com/janpf/self-supervised-multi-task-aesthetic-pretraining


