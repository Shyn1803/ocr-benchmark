# Chapter 2. Introduction to the Overlay Utility

The Overlay Utility is one of the AFP Utilities that allows you to create electronic form overlays; which can always be printed in their stored format and can be positioned anywhere on the page.

Using the overlay utility; you can:

Design an overlay interactively on a display The information you defined for an overlay is called a source overlay.

- 2 Save a source overlay in your file.
- 3 Create an overlay object from a source overlay; which can be printed on the IPDS printers.


You can change the design of the overlay by changing the source overlay

# Notes:

- 1 You cannot directly change the overlay object:  You need to change the source overlay and create the overlay object from it.
- 2 You can work with the overlay object using the resource management utility See Chapter 19. Work with Overlays Function on page 341 for more information.


# Print Form and Overlay

You can merge the overlay object with various spooled files as your final printout. You can use overlays at any time you want on various types of forms. Thus, you can eliminate the use of preprinted paper forms.

The overlay can be composed of text; images; graphics; lines, boxes; and bar codes called elements. All of the environmental data (such as font references) is defined as of the overlay definition: The fonts defined for the overlay are not influenced by the fonts used for the variable data on the logical page. part

The basic function of the overlay is to provide a template-like pattern that establishes fixed data for merging with various files. spooled

For each element; you must specify its position and the horizontal and vertical and vertical distances of the overlay origin from the origin of the page. The initial values are set to zero offset in both directions; which means the overlay origin will coincide with the page origin. This eliminates the need for preprinted paper forms.

