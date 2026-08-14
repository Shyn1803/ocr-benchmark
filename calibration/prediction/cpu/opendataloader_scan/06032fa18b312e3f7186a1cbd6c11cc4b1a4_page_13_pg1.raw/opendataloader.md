![](<06032fa18b312e3f7186a1cbd6c11cc4b1a4_page_13_pg1_images/imageFile1.png>)

Fig. 18. Failure case illustration. First Row: we test our method in wide baseline cases of light field, segmentation tends to inconsistent due to large view point changes. Second Row: The visual results of the nonLambertian cases. Our method discovers correct object boundaries, but mistakenly separates objects due to incorrect depth matches.

![](<06032fa18b312e3f7186a1cbd6c11cc4b1a4_page_13_pg1_images/imageFile2.png>)

Fig. 19. User guided object segmentation. Regions comprising a single object are selected by a user. The regions themselves are not manually altered.

# 7 APPLICATIONS

Segmentation is a starting point for many processes in image manipulation and computer vision. In the following we highlight several applications of our light field segmentation method.

# 7.1 User-guided Object Segmentation.

Like most 2D and video segmentation methods, our method segments the light field into regions of consistent appearance, but not into semantic objects. However with a simple user interface, we can can manually select multiple regions that comprise a single object. Examples of this user-guided object segmentation are shown in Fig. 19.

# 7.2 Light Field Flattening

Image flattening refers to the suppression of texture detail while preserving strong scene edges and overall image structure. Here, we extend an existing 2D method [Bi et al. 2015] to 4D. Specifically, we take into consideration the L 1 sparsity in spatial slices, angular patches as well as the 4D light field segmentation, and jointly minimize the pixel variation and approximation error as detailed in the following.

Spatial Term. f i is the Lab feature vector of pixel p i .

$$
wijllL(i) (24) Pj€Nh (pi)
$$

where Nn (pi) is local h X h patch.  wij is the affinity between pixel pi and pj Here, we simply use Euclidean distance with normalization function_ spatial Angular Term. We prefer a uniform intensity values over simple angular patches of the light field; and smooth exposure variation in different spatial slices. Similar to Eqn. 24, we formulate our angular flattening term as

$$
Ea = (25)
$$

where N a p i is the angular patch that p i lies in.

Segmentation Term. The segmentation provides extra cues to include more pixels for avoiding the influence of shading, reflectance or noise.

$$
Es wijllL(i) L(j)ll1, (26) Pi €sk Pj€sk
$$

Data Fidelity Term. To avoid trivial solution, smoothed light field should be similar to original light field, which is formulated as,

$$
Ea = (27)
$$

where L ini is original light field data. The overall objective function is the sum of those terms,

$$
E = Ed + QE1 + BEa + ~Es, (28)
$$

Fig. 20 shows the results of the light field segmentation, where we then utilize the segmentation cue to remove fine details and preserve the main edges of the light field. In the example of Fig. 21, we visualize our light field segmentation,

edge detection results and pencil sketching. We first utilize our light field segmentation for removing fine details of light field. Then, we apply conventional edge detection method [Doll´ ar and Zitnick 2015]

