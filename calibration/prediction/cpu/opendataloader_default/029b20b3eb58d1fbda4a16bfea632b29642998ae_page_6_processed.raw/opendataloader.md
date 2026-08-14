The distributed middleware architecture of the application was based on the framework described in [10]. The physics of the scene was simulated using the Bullet Physics Library2. Simplified forms of non-convex pieces and holes were designed for the physics simulation in order to facilitate their manipulation, as the Bullet Physics Library does not handle nonconvex meshes properly.

![](<029b20b3eb58d1fbda4a16bfea632b29642998ae_page_6_processed_images/imageFile1.png>)

Fig. 2. on Top: six holes complexity task description. On Bottom: two holes complexity task description In both cases, twelve pieces were involved, six ”fitters” to place in the holed box and six ”non-fitters” to place in the disposal zone.

The virtual coordinates of the flystick were linked to the physical ones by the mean of a standard proportional derivative control scheme for positions and a suboptimal control scheme with a quadratic cost for rotations, as described in [32]. Performance levels were set at

2 www.bulletphysics.org

