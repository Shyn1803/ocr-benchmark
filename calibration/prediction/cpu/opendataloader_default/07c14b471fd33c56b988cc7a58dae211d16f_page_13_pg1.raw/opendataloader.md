![](<07c14b471fd33c56b988cc7a58dae211d16f_page_13_pg1_images/imageFile1.png>)

# US 6,453,463 B1

### 10

FIG. 9 is a flow chart illustrating operations involved in a write operation to a memory elementby Speculative thread 203 in accordance with an embodiment of the present invention. Ifa space-time dimensioned version510does not exist, the System creates a Space-time dimensioned version

the system starts:with a field number for the field, and applies a modulo N operation to the field number to produce a number for the associated marking bit. This modulo operation canbe efficiently performedifNis a poweroftwo because the modulo operation reduces to a simple bit mask operation that isolates the lower order bits of the field

### 510 in speculative heap 406 (step 902). The system also

updates status word 504 to indicate that speculative thread 203 has written to the object if Such updating is necessary

number.

The selection a value of N for an object involves a tradeoff. IfN istoosmall, there tendsto be lotofaliasingand systemperformance suffers due to false rollbacks. IfN istoo large, a greatdeal of memory is used for markingbits which can cause cache performance to Suffer. In one embodiment of the present invention, N=8. In another embodiment,

### (step 903). The system next writes to space-time dimen sionedversion510(step 904).Such updatingis necessary if

head thread 202 must Subsequently choose between writing to both primary version 500 and space-time dimensioned version 510 or writing only to primary version 500 as is

described above with reference to FIG. 7.

N=16.

Inthecase ofan array object, the System appliesa division

FIG. 10 is a flow chart illustrating operations involved in a join operation between head thread 202 and a speculative thread 203 in accordance with an embodiment the present invention. Ajoin operation occurs for example when head

15

### operation to the array element number (field number) to

identify the associated array element. For example, if the array object has N marking bits numbered 0,1,2,...,N-1 and Marray elements numbered 0,1,2,..., M-1, the step of identifying the marking bit includes dividing the array element numberby the ceiling of M/N to produce a number for the associated marking bit. If the ceiling of M/N is a poweroftwo,the division operationcanbe accomplishedby shiftingthe array indeXSothatthe mostSignificantbitsofthe array indeX become the number for the associated marking

- thread202 reaches a point in the program where speculative
- thread203 began executing. The join operation causes State associatedwiththe speculative thread203 tobe merged with state associated with the head thread 202. This involves copying and/or merging the Stack ofSpeculative thread 203


### into thestackofheadthread202(step 1002). It alsoinvolves

merging Space-time dimension and primary versions of

25

### objects (step 1004) as well as possibly garbage collecting speculative heap406(step 1006). In one embodiment ofthe

bits

The above-described mapping between array elements and marking bits for array objects associates consecutive array locations with a single marking bit. This ensures that not all of the marking bits are Set by common block copy operations involving only a portion of the array.

present invention, one ofthreads202 or 203 performs steps 1002 and 1006, while the other thread performs step 1004.

FIG. 11 is a flow chart illustrating operations involved in a join operation between head thread 202 and a speculative

After the marking bit is identified, the marking bit is Set

thread 203 in accordance with another embodiment of the

## (step 1206) and the reference is performed to the field (or

present invention. In this embodiment, speculative thread

### array element) within the object (step 1208).

203 carries on as a pseudo-head thread. As a pseudo-head thread, speculative thread 203 uses indirection to reference Space-time dimensioned versions of objects, but does not mark objects or create versions. While speculative thread 203 is acting as a pseudo-head thread, head thread 202 updates primary versions of objects. Extension to Additional Speculative Threads

In general the marking mechanism according to the present invention can be used in any application that must keep track of accesses to fields within an object. However, in one embodiment of the present invention, marking is performed for read operationsby speculative thread 203. In anotherembodiment, markingis performed to write bits 606 during a write operation by speculative thread 203 and to read bits 604 during a read operation by speculative thread

35

40

Although the present invention hasbeen described for the case ofa single Speculative thread, the presentinventioncan be extended to provide multiple Speculative threads operat ing on multiple Space-time dimensioned versions of a data object in parallel. Process ofSetting Marking Bits

2O3.

After the markingbits have been set, if a head thread202 Subsequently performs a write operation to a field in the object, head thread 202 can identify the associated marking bitusingthe above-described moduloordivision operations. Next, the markingbit is extracted for examination purposes using a special bit extract operation that is part of the instruction Set of the underlying computer System.

45

FIG. 12 is a flow chart illustrating the process of setting a marking bit associated with a referenced field within an object in accordance with an embodiment of the present invention. First, the System receives a reference to the field

50

within the object (step 1202). This reference may be a read ora write operation. (Notethat in the case ofan array object the field is an array element.)

FIG. 13 illustrates how a marking bit number can be determined from a field number oran array element number in accordance with an embodiment ofthe present invention. The system starts will a field number or an array element number 1302. In the case of a field number, the system performs a modulo operation by masking off all but the lower order three bits of field number 1302 to produce a

Next, the System identifies a markingbit associated with

### the field (step 1204). In one embodiment of the present

55

invention, the System maintains a Separate Set of read marking bits 604 for the object to indicate that a read operationhasoccurredto the field, andaseparate Set ofwrite marking bits 606 to indicate that a write operation has occurred to the field. In this embodiment, ifthe operation is a read operation, one of the read marking bits 604 is selected. Otherwise, one of the write marking bits 606 is

### three bit index(1,0,0) thatspecifiesa markingbit. Inthecase

of an array index, he system performs a division operation by shifting array element number 1302 until only the three

60

### most significant bits (0,1,1) remain.

FIG. 14 illustrates how a block transfer operation sets multiple markingbits in accordance with an embodiment of the present invention. The example illustrated in FIG. 14 includes an array of data elements 1402. These data ele

Selected.

In one embodiment ofthe present invention, the marking bit is identified by performing modulo operation. For example, if the object includes N marking bits numbered 0,

65

ments are numbered 0,1,2,..., 31. FIG. 14 also includes

an array ofreadbits 604. These readbits are numbered 0, 1,

1, 2, ..., N-1 and M fields numbered 0, 1, 2, ..., M-1,

