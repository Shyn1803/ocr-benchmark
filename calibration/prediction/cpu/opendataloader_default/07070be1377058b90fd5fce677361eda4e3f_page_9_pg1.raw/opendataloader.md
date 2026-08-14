To appear in the ACM SIGGRAPH conference proceedings

<table>
  <tr>
    <td> </td>
    <td>covered (K pix)<br><br></td>
    <td>rendered (K pix)</td>
    <td>overdraw</td>
    <td> </td>
    <td>vertex (ms)</td>
    <td>geometry (ms)<br><br></td>
    <td>raycasting (ms)</td>
    <td>lighting (ms)<br><br></td>
    <td>shadow (ms)</td>
    <td>texturing (ms)<br><br></td>
    <td> </td>
    <td>Total (ms)<br><br></td>
    <td>Ratio</td>
  </tr>
  <tr>
    <td>GL ST PT SQ PQ<br><br>Lens1<br>Lens2<br></td>
    <td>308 406 897 714 5089 5006<br><br></td>
    <td>249 173 197 173 181 172 172</td>
    <td>0% 78% 106% 418% 294% 2859% 2810%<br><br></td>
    <td> </td>
    <td>0.40 0.41 0.41 0.41 0.40 0.40 0.40<br><br></td>
    <td>0.57 0.69 0.40 0.36 0.47 0.44</td>
    <td>0.13 0.16 0.33 0.29 2.55 2.00<br><br></td>
    <td>0.33 0.34 0.39 0.44 0.42 0.53 0.79<br><br></td>
    <td>0.06 0.57 0.70 0.26 0.22 0.61 0.49<br><br></td>
    <td>0.45 0.24 0.17 0.36 0.37 0.65 0.62</td>
    <td> </td>
    <td>1.25 2.25 2.52 2.20 2.06 5.21 4.74<br><br></td>
    <td>100% 180% 202% 176% 165% 417% 379%</td>
  </tr>
  <tr>
    <td>600 2800 4900<br><br></td>
    <td>702 714 786</td>
    <td>181<br><br>181<br><br>182<br><br><br></td>
    <td>288% 294% 332%<br><br></td>
    <td> </td>
    <td>0.39 0.40 0.45<br><br></td>
    <td>0.16 0.36 0.52</td>
    <td>0.26 0.29 0.29<br><br></td>
    <td>0.44 0.42 0.43</td>
    <td>0.17 0.22 0.27<br><br></td>
    <td>0.13 0.37 0.49</td>
    <td> </td>
    <td>1.55 2.06 2.44<br><br></td>
    <td>128% 165% 185%</td>
  </tr>
  <tr>
    <td>Temple PQ Patio PQ<br><br></td>
    <td>1950 1271<br><br></td>
    <td>250 335</td>
    <td>680% 279%<br><br></td>
    <td> </td>
    <td>0.17 7.55<br><br></td>
    <td>0.33 31.47</td>
    <td>0.77 0.86<br><br></td>
    <td>0.63 0.24</td>
    <td>0.42 5.93<br><br></td>
    <td>0.57 38.28</td>
    <td> </td>
    <td>2.88 79.85</td>
    <td>461% 600%<br><br></td>
  </tr>
</table>


Table 3: Rendering times for our algorithm, with the cost of the diﬀerent steps. The ﬁrst 7 lines are for the Facade scene (2800 triangles), for several projection methods: GL (standard GLSL rendering with per pixel lighting), Sx is Spherical map; Px is Parabola map; xT uses triangles enclosing shape; while xQ uses quad bounding box. The next three lines are for Facade with diﬀerent scene complexity for the PQ algorithm. The last two lines are for larger scenes.

# 6 Conclusion and Future Directions

In this paper, we have presented a robust algorithm for handling speciﬁc non-linear projections inside the graphics pipeline. Our algorithm works both for direct display of the non-linear projection, e.g. a ﬁsh-eye lens inside a video game, or for indirect use, e.g. when rendering a shadow map with a paraboloid projection.

As with previous work, we start by bouding the projection of each shape, then discard extra fragments inside the bounding shape. Our contributions are twofold. First: two diﬀerent methods for bounding the non-linear projections, one based on triangles that is optimal in fragments but requires more work in the geometry engine, the other based on quads that is optimal for the geometry engine but can causes more overdraw. Second: a mathematical analysis of several non-linear projection methods, where we show that some of them have simple expressions, and thus lend themselves to easy bounding through geometric tools.

Although non-linear projections are slower than linear projections, the extra cost is manageable. As a single non-linear projection can replace up to ﬁve linear projections (in a hemicube), it can even be a practical alternative, both for rendering time and memory cost.

# Acknowledgements

The authors wish to thank the anonymous reviewers for their valuable comments. Nicolas Holzschuch is currently on a sabbatical at Cornell University, funded by the INRIA.

Part of this research was carried within the ARTIS research team; ARTIS is a research team of the INRIA Rhˆone-Alpes and of the LJK; LJK is UMR 5224, a joint research laboratory of CNRS, INRIA, INPG, U. Grenoble I and U. Grenoble II. This research was supported in part by the R´egion Rhˆone-Alpes, under the Dereve II and the LIMA research programs, and by the ANR under the ART3D program.

Most 3D models used in this research were created by Laurence Boissieux.

# References

B, S., A, T.,  S, H.-P. 2002. Shadow mapping for hemispherical and omnidirectional light sources. In Computer

Graphics International, Springer, 397–408.

F, G. 2005. Caches multiples et cartes programmables pour un calcul progressif et interactif de l’e´clairement global. PhD thesis, Universit´e Lyon 1.

H, W.,  S, H.-P. 1998. View-independent environment maps. In Graphics Hardware ’98.

H, X., W, L.-Y., S, H.-Y.,  G, B. 2006. Real-time multi-perspective rendering on graphics hardware. In Rendering Techniques 2006: Eurographics Symposium on Rendering.

- K, J., L, J.,  A, T. 2004. Hemispherical rasterization for self-shadowing of dynamic objects. In Rendering Techniques 2004: Eurographics Symposium on Rendering 2004, 179–184.

K, J. J.,  B, M. L. 2000. Fish-eye lens designs and their relative performance. In Current Developments in Lens Design and Optical Systems Engineering, SPIE, 360–369.

- L, S., S, H., K, J., L, J.,  A, T. 2007. Incremental instant radiosity for real-time indirect illumination. In Rendering Techniques 2007 (Proceedings of the Eurographics Symposium on Rendering), 277–286.


L, J. H. 1772. Anmerkungen und Zusa¨tze zur Entwerfung der Land- und Himmelscharten.

L, D. B., G, N. K., T, D., M, S. E.,  M, D. 2006. Practical logarithmic shadow maps. In Siggraph 2006 Sketches and applications.

- L, D. B., G, N. K., Q, C., M, S. E.,  M, D. 2007. Practical logarithmic rasterization for low-error shadow maps. In Graphics Hardware 2007.
- M¨, T.,  T, B. 1997. Fast, minimum storage raytriangle intersection. Journal of Graphics Tools 2, 1, 21–28.


O, B., B, M.,  ME, C. 2006. Practical implementation of dual paraboloid shadow maps. In ACM SIGGRAPH Symposium on Videogames, ACM Press, 103–106.

8

