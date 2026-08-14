When the parameter values of the elements become incorrect by changing the parameter values of the overlay specifications; a warning message is displayed. You can adjust parameter values of those elements by pressing the Enter or you can change the parameter values of the overlay specifications to correct the errors key

The following table describes the cause of warning messages and the results.

Table 6. The Cause of a Message and Its Results

<table>
  <tr>
    <th>Cause</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>The Unit of measure changed from 1-Inch to 2=Centimeter and the value for Module width gets too centimeters.</td>
    <td>The correct minimum value 0.003 centimeter is used</td>
  </tr>
  <tr>
    <td>The Unit of measure changed from 2=Centimeter to 1-Inch and the value for Module width or Line width gets too large. For example; 2 centimeters becomes 2 inches.</td>
    <td>The correct maximum value 1 inch is used.</td>
  </tr>
  <tr>
    <td>The Printer type changed from 1=4224/4234/4230 or 9=Not specified to another type and the value for Color becomes incorrect. For example, 1-Blue is incorrect.</td>
    <td>The value *DEFAULT is used</td>
  </tr>
  <tr>
    <td>The Printer type changed from another type to 1-4224/4234/4230 or 2-3812/3816/3930, or 3-3916/4028 or 7-3935 and the value for Format becomes incorrect. For example; 2-Vertical is incorrect.</td>
    <td> </td>
  </tr>
  <tr>
    <td>The Printer type changed from 1=4224/4234/4230 or 2-3812/3816 or 3-3916/4028, or 7-3935 specified to another type and the value for Overstrike becomes incorrect. For example; X is incorrect.</td>
    <td>Blank is used_</td>
  </tr>
  <tr>
    <td>The Printer type changed from 1-4224/4234/4230 Or 2-3812/3816/3930 or 3-3916/4028 or 7-3935 or 9-Not specified to another type and the value for Underline becomes incorrect. For example; Yis not correct.</td>
    <td>The value N is used</td>
  </tr>
  <tr>
    <td>The Printer type changed from 1=4224/4234/4230 Or 2-3812/3816/3930 or 3-3916/4028 or 7-3935 or 9-Not specified to another type and the value for Character size becomes incorrect. For example; 1 is not correct.</td>
    <td>The value *DEFAULT is used</td>
  </tr>
</table>


