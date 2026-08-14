you performed this command last is used. If you specify *PRV for the PAGSEG parameter; it is not necessary to specify a library

page-segment-name

Specify the name of the page segment to be created.

The possible library values are:

# *CURLIB

The current library for the job is used to create the page segment: If no library is specified as the current for the job, library QGPL is used. library

library-name

Specify the library in which the page segment will be created.

# From folder (FRMFLR)

Specifies the name of the folder that contains the PC document to be converted.

The possible values are:

*PRV Specifies the name of the folder used when you previously created page segment of the same name.

folder-name

Specify the folder name.

# From PC document (FRMDOC)

Specifies the PC document name to be converted

The possible values are:

- *PRV Specifies the name of the PC document used when you previously created a page segment of the same name
- *PAGSEG


Specifies that the name of the page segment to be created is the same as the name of the PC document.

# PC-document-name

Specify the PC document name that is to be converted.

# Change image size (CHGIMGSIZE)

Specifies whether the size of the image in the page segment is changed or not

The possible values are:

# SAME

Specifies the same value used for this parameter when you previously created a page segment of the same name. If this is the first page segment, the default value is *NO.

- *NO Specifies not to change the image size.
- *YES Specifies to change the image size.


If you specify *YES, the IMGSIZE and MAPPING parameters appear; and you can specify the new image size in the page segment and how to map the input image to the size. will

