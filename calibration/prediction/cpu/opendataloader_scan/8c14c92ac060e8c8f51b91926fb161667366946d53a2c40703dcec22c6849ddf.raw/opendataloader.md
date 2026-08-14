To use an SBCS font that resides in the system, you can specify either a coded font name or a of code page name and font character set name. To use a DBCS font that resides in the system; you must specify a coded font name. pair

# Code page

Has an object type *FNTRSC with attribute CDEPAG. A code page has many code points and their corresponding character identifiers. Character identifiers are mapped to corresponding character patterns by a font character set.

# Font character set

Has an object type *FNTRSC with attribute FNTCHRSET. A font character set has many character identifiers and their corresponding character patterns.

The WRKFNTRSC command shows you a list of font resources. Most fonts reside in libraries that have names that start with QFNT

Change Font (Font Type=l): When you choose 1 for the Font type prompt, the following display appears.

![](<8c14c92ac060e8c8f51b91926fb161667366946d53a2c40703dcec22c6849ddf_images/imageFile1.png>)

Change

PFD Definition

Font

Font

number

identifier

Font

Font and character

type

Type choices, press

Enter.

Font:

Identifier

1-65535

11

Point

*NONE

0.1-999.9,

size

*NONE

Character identifier:

*SYSVAL

1-32767,

Graphic character set

*SYSVAL

1-32767

Code

page

'description'

Text

10 CPI

Courier

F3=Exit

F5=Refresh

F12=Cancel

Using this display; you can change the font identifier; size, graphic character set, code page; and the description text. point

<table>
  <tr>
    <th>Field Name</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Font number</td>
    <td>Shows the font number of the font being changed.</td>
  </tr>
  <tr>
    <td>Font type</td>
    <td>Shows the font type you specified in the previous display</td>
  </tr>
  <tr>
    <td>Identifier</td>
    <td>Specifies the font identifier: You can specify number from 1 to 65535 for font. your</td>
  </tr>
  <tr>
    <td>Point size</td>
    <td>Specifies the point size. You can use a value from 0.1 to 999.9 for your size point</td>
  </tr>
  <tr>
    <td>Graphic character set</td>
    <td>Specifies the graphic character identifier: You can use number from 1 to 32767. You can also specify *SYSVAL</td>
  </tr>
</table>


