/* */ /* DESCRIPTION: This program will delete all non-AFP records (or */ /* records that do not begin with X(5A) from the */ /* output object before giving control back to ACIF */ /* */ /*********************************************************************/ /* Standard acif exit header file */ /************************************************/ */ #include "apkexits.h"

long OUTEXIT( OUTEXIT_PARMS *exitstruc ) {

/************************************************************************/ /* Delete all records from the output that do not begin with Hex '5A' */ /************************************************************************/

if(exitstruc->eof != ACIF_EOF) {

if(exitstruc->record[0] == 0x5A)

exitstruc->request = ACIF_USE; else

exitstruc->request = ACIF_DELETE; }

return( 0 ); }

# 11.2.5 Resource exit

If you want to prevent ACIF from collecting a specific type of resource, such as overlays, you can use the ACIF restype parameter. However, if you want to prevent ACIF from writing a specific resource to the resource file, use the resource exit.

The resource exit is best used to control resources at the file name level. For example, you want to exclude particular fonts from the resource file. You can code this exit program to contain a table of the fonts that you want to exclude and filter them from the resource file. The program that is invoked at this exit is defined in the ACIF resexit parameter.

ACIF does not start the exit for the following resource types:

Page definitions: The pagedef is a required resource for converting line data to AFP and it is never included in the resource file.

Form definitions: The formdef is a required resource for processing print files. If you do not want the formdef to be included in the resource file, specify restype=none or explicitly exclude the formdef from the restype list.

Coded fonts: If you specify MCF2REF=CF, ACIF writes coded fonts to the resource file if they are included in the restype list. The default is MCF2REF=CPCS; therefore, ACIF does not write coded fonts to the resource file.

# 11.2.6 Debugging input user exit programs

When you work with an input exit, you must know how the exit changed your data before you load it. A way to determine how the exit changed the data is to set up ACIF to run in stand-alone mode (not called from arsload).

Chapter 11. Exits 247

