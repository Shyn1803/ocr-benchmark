<table>
  <tr>
    <th> </th>
    <th>covered (K pix)</th>
    <th>rendered (K pix)</th>
    <th>overdraw</th>
    <th>vertex (ms)</th>
    <th>geometry (ms)</th>
    <th>raycasting (ms)</th>
    <th>lighting (ms)</th>
    <th>shadow (ms)</th>
    <th>texturing (ms)</th>
    <th>Total (ms)</th>
    <th>Ratio</th>
  </tr>
  <tr>
    <td>GL</td>
    <td> </td>
    <td>249</td>
    <td> </td>
    <td>0.40</td>
    <td> </td>
    <td> </td>
    <td>0.33</td>
    <td>0.06</td>
    <td>0.45</td>
    <td>1.25</td>
    <td>100%</td>
  </tr>
  <tr>
    <td>ST</td>
    <td>308</td>
    <td>173</td>
    <td>789</td>
    <td>0.41</td>
    <td>0.57</td>
    <td>0.13</td>
    <td>0.34</td>
    <td>0.57</td>
    <td>0.24</td>
    <td>2.25</td>
    <td>180%</td>
  </tr>
  <tr>
    <td>PT</td>
    <td>406</td>
    <td>197</td>
    <td>106%</td>
    <td>0.41</td>
    <td>0.69</td>
    <td>0.16</td>
    <td>0.39</td>
    <td>0.70</td>
    <td>0.17</td>
    <td>2.52</td>
    <td>202%</td>
  </tr>
  <tr>
    <td>SQ</td>
    <td>897</td>
    <td>173</td>
    <td>418%</td>
    <td>0.41</td>
    <td>0.40</td>
    <td>0.33</td>
    <td>0.44</td>
    <td>0.26</td>
    <td>0.36</td>
    <td>2.20</td>
    <td>176%</td>
  </tr>
  <tr>
    <td>PQ</td>
    <td>714</td>
    <td>181</td>
    <td>294%</td>
    <td>0.40</td>
    <td>0.36</td>
    <td>0.29</td>
    <td> </td>
    <td>0.22</td>
    <td>0.37</td>
    <td>2.06</td>
    <td>165%</td>
  </tr>
  <tr>
    <td> </td>
    <td>5089</td>
    <td>172</td>
    <td>2859%</td>
    <td>0.40</td>
    <td>0.47</td>
    <td>2.55</td>
    <td>0.53</td>
    <td>0.61</td>
    <td>0.65</td>
    <td>5.21</td>
    <td>417%</td>
  </tr>
  <tr>
    <td>Lens2</td>
    <td>5006</td>
    <td>172</td>
    <td>2810%</td>
    <td>0.40</td>
    <td>0.44</td>
    <td>2.00</td>
    <td>0.79</td>
    <td>0.49</td>
    <td>0.62</td>
    <td>4.74</td>
    <td>379%</td>
  </tr>
  <tr>
    <td>600</td>
    <td>702</td>
    <td>181</td>
    <td>288%</td>
    <td>0.39</td>
    <td>0.16</td>
    <td>0.26</td>
    <td>0.44</td>
    <td>0.17</td>
    <td>0.13</td>
    <td>1.55</td>
    <td>128%</td>
  </tr>
  <tr>
    <td>2800</td>
    <td>714</td>
    <td>181</td>
    <td>294%</td>
    <td>0.40</td>
    <td>0.36</td>
    <td>0.29</td>
    <td>0.42</td>
    <td>0.22</td>
    <td>0.37</td>
    <td>2.06</td>
    <td>165%</td>
  </tr>
  <tr>
    <td>4900</td>
    <td>786</td>
    <td>182</td>
    <td>332%</td>
    <td>0.45</td>
    <td>0.52</td>
    <td>0.29</td>
    <td>0.43</td>
    <td>0.27</td>
    <td>0.49</td>
    <td>2.44</td>
    <td>185%</td>
  </tr>
  <tr>
    <td>Temple PQ Patio PQ</td>
    <td>1950</td>
    <td>250</td>
    <td>6809</td>
    <td> </td>
    <td>0.33</td>
    <td>0.77</td>
    <td>0.63</td>
    <td>0.42</td>
    <td>0.57</td>
    <td>2.88</td>
    <td>4619</td>
  </tr>
  <tr>
    <td>Patio PQ</td>
    <td>1271</td>
    <td>335</td>
    <td>2799</td>
    <td>7.55</td>
    <td>31.47</td>
    <td>0.86</td>
    <td>0.24</td>
    <td>5.93</td>
    <td> </td>
    <td>79.85</td>
    <td>6009</td>
  </tr>
</table>


Table 3: Rendering times for our algorithm, with the cost of the di ﬀ erent steps. The ﬁrst 7 lines are for the Facade scene (2800 triangles), for several projection methods: GL (standard GLSL rendering with per pixel lighting), S x is Spherical map; P x is Parabola map; x T uses triangles enclosing shape; while x Q uses quad bounding box. The next three lines are for Facade with di ﬀ erent scene complexity for the PQ algorithm. The last two lines are for larger scenes.

# 6 Conclusion and Future Directions

In this paper, we have presented a robust algorithm for handling speciﬁc non-linear projections inside the graphics pipeline. Our algorithm works both for direct display of the non-linear projection, e.g. a ﬁsh-eye lens inside a video game, or for indirect use, e.g. when rendering a shadow map with a paraboloid projection.

As with previous work, we start by bouding the projection of each shape, then discard extra fragments inside the bounding shape. Our contributions are twofold. First: two di ﬀ erent methods for bounding the non-linear projections, one based on triangles that is optimal in fragments but requires more work in the geometry engine, the other based on quads that is optimal for the geometry engine but can causes more overdraw. Second: a mathematical analysis of several non-linear projection methods, where we show that some of them have simple expressions, and thus lend themselves to easy bounding through geometric tools.

Although non-linear projections are slower than linear projections, the extra cost is manageable. As a single non-linear projection can replace up to ﬁve linear projections (in a hemicube), it can even be a practical alternative, both for rendering time and memory cost.

# Acknowledgements

The authors wish to thank the anonymous reviewers for their valuable comments.

Nicolas Holzschuch is currently on a sity, funded by the INRIA.

Part of this research was carried within the ARTIS research team; ARTIS is a research team of the INRIA Rhˆ one-Alpes and of the LJK; LJK is UMR 5224, a joint research laboratory of CNRS, INRIA, INPG, U. Grenoble I and U. Grenoble II. This research was supported in part by the R´egion Rhˆone-Alpes , under the Dereve II and the LIMA research programs, and by the ANR under the ART3D program.

were created by Laurence Boissieux .

# References

Graphics International , Springer, 397–408.

F  , G. 2005. Caches multiples et cartes programmables pour un calcul progressif et interactif de l’e´clairement global . PhD thesis, Universit´ e Lyon 1.

H  , W.,  S  , H.-P. 1998. View-independent environment maps. In Graphics Hardware ’98 .

H  , X., W  , L.-Y., S  , H.-Y.,  G  , B. 2006. Real-time multi-perspective rendering on graphics hardware. In Rendering Techniques 2006: Eurographics Symposium on Rendering .

K  , J., L  , J.,  A  , T. 2004. Hemispherical rasterization for self-shadowing of dynamic objects. In Rendering Techniques 2004: Eurographics Symposium on Rendering 2004 , 179–184.

K  , J. J.,  B  , M. L. 2000. Fish-eye lens designs and their relative performance. In Current Developments in Lens Design and Optical Systems Engineering , SPIE, 360–369.

 , S., S  , H., K  , J., L  , J.,  A  , T. 2007. Incremental instant radiosity for real-time indirect illumination. In Rendering Techniques 2007 (Proceedings of the Eurographics Symposium on Rendering) , 277–286.

L  , J. H. 1772. Anmerkungen und Zusa¨tze zur Entwerfung der Landund Himmelscharten .

AND MANOCHA, D 2006. In Siggraph 2006 Sketches and applications.

- L  , D. B., G  , N. K., Q  , C., M  , S. E.,  M  , D. 2007. Practical logarithmic rasterization for low-error shadow maps. In Graphics Hardware 2007 .
- M¨  , T.,  T  , B. 1997. Fast, minimum storage raytriangle intersection. Journal of Graphics Tools 2 , 1, 21–28.


 , B., B  , M.,  M  E  , C. 2006. Practical implementation of dual paraboloid shadow maps. In ACM SIGGRAPH Symposium on Videogames , ACM Press, 103–106.

hemispherical   and omnidirectional light sources. In Computer

