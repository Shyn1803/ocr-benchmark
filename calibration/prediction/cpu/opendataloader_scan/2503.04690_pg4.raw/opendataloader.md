# Methods

# 2.1 Video Pre-processing

An unprocessed video of a plume that is recorded with ideal background conditions. 1 All frames are converted to gray scale, that is n × d arrays taking on values between 0 and 1 (or 0 to 255). Two main steps are used in pre-processing prior to applying our model: background subtraction and Gaussian blurring.

Background subtraction. A fixed background subtraction method is applied to isolate the plume, where the first k fixed subtraction frames of video (where no plumes are have formed) are used to create an average background image. The average image is subtracted against the remaining frames to create the isolated plume frames. Once the plume dynamics have been isolated from background across selected frames, Gaussian blurring is applied.

Gaussian Blurring. Two separately tuned Gaussian filters are applied—a temporal and spatial filter, respecitvely. First, a Gaussian filter is applied across the time series of frames to add a time blur, reducing the high resolution of the plume dynamics. Second, a Gaussian filter is applied to each frame independently to coarse grain the image, adding spatial blur.

# 2.2 Coarse-graining for Centerline and Edge modeling

We denote the output of data pre-processing as Z = [ z ( t 0 ) ,..., z ( t K )], where background subtraction and Gaussian filters have been applied. We extract a time series of second-order polynomial coefficients that model the center path of the plume for each frame. Additionally, we learn the parameters of a growing sinusoidal function that best characterizes the spread, or edge-model, of the plume. We theorize there exists a connection between the Kevin Helmholtz shear velocity and the sinusoidal frequency.

Each frame z ( t i ) is converted to a reduced order model describing the center and edge paths in a three step procedure: (i) contour detection, (ii) a concentric circle search, and (iii) regression. For each array, z ( t i ), image recognition techniques are used to identify the plume contour and subsequently search along concentric circles, centered at the leak source, to identify the path of highest density, where we denote raw pixel value as a proxy for plume density, and the edge paths, as seen in Fig. 2.

![](<2503.04690_pg4_images/imageFile1.png>)

# Data reduction process for plume film

(d)

Figure 2: The plume point reduction step converts a frame of video into a scatter of edge and center points: (a) the raw frame image, (b) background subtraction, (c) contour selection, and finally (d) Along various ranges from origin, identify the max intensity (center) and intersection (edge) points with contours. (e) displays the final points on the original frame.

Contour Detection. We apply a binary threshold to identify the contours outlining the plume for each array z ( t i ). Hyperpameter selection for the thresholding is done by using opencv ’s Otsu’s binarization. Optimal global threshold selection is performed by inspecting the image histogram for each array z ( t i ). The n largest contours, by area, are then selected for remainder of the pipeline. We denote the identified plume at time t k as ψ k .

(ii) Concentric Circle Search. A search is performed along a set of ℓ concentric circles, centered at the plume leak source, with incrementally growing radii of r i = r · i for i = 1 ,...,ℓ where r is some fixed

1 A solid black background is used when filming plume dynamics.

