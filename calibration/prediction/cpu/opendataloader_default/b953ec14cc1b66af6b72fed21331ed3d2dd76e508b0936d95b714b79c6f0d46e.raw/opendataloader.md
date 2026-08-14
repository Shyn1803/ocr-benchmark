Performing a write operation on the target generates one of the following actions, depending on the bitmap:

If the bitmap indicates the grain to be modified on the target is not yet copied, it is first copied from the source (copy on demand). The bitmap is updated, and the grain is modified on the target with the new value, as shown in Figure 11-7. The source volume remains unchanged.

<table>
  <tr>
    <td>![](<b953ec14cc1b66af6b72fed21331ed3d2dd76e508b0936d95b714b79c6f0d46e_images/imageFile1.png>)</td>
  </tr>
</table>


- Figure 11-7 Modifying a non-copied grain on the target

If the bitmap indicates the grain to be modified on the target was copied, it is directly changed. The bitmap is not updated, and the grain is modified on the target with the new value, as shown in Figure 11-8.

- Figure 11-8 Modifying an already copied grain on the Target


# Note: If the entire grain is to be modified and not only part of it (some blocks only), the copy on demand is bypassed. The bitmap is updated, and the grain on the target is modified but not copied first.

<table>
  <tr>
    <td>![](<b953ec14cc1b66af6b72fed21331ed3d2dd76e508b0936d95b714b79c6f0d46e_images/imageFile2.png>)</td>
  </tr>
</table>


Chapter 11. Advanced Copy Services 445

