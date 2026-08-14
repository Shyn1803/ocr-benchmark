![](<07c14b471fd33c56b988cc7a58dae211d16f_page_9_pg1_images/imageFile1.png>)

# US 6,453,463 B1

1

2

condition can occur in a number ofSituations. For example, a rollback condition occurswhen a speculative threadthatis executingprogram instructions in advance ofa head thread reads from a memory element before the head thread per forms a write to the memory element. In this case, the speculative thread must “rollback” so that it can read the value stored by the head thread. Arollbackcondition can be detectedby “marking memory elements asthey are readby the Speculative thread So that the head thread can Subse quently determine if the memory elements have been read by the Speculative thread. Unfortunately, using a Separate marking indicator for each memory element can consume a large amount of memory, which can reduce cache hit rates arid thereby degrade System performance.

METHOD AND APPARATUS FOR PROVIDING FINER MARKING GRANULARITY FOR FIELDS WITHIN

OBJECTS

Related Application

This application is related to the Subject matter in a pendingU.S. patentapplication, entitled“SupportingSpace Time Dimensional Program Execution by Selectively Ver Sioning Memory Updates,” by inventors Shailender Chaudhry and Marc Tremblay, having Ser. No. 09/313,229 and a filing date of May 17, 1999.

1O

The Subject matter ofthis application is also related to the Subject matter in a co-pending non-provisional application

What is needed is a method and an apparatus for marking memory elements that does require a large amount of memory for Storing marking indicators.

15

## by the same inventor(s) as the instant application and filed

on the same day as the instant application entitled, “Using Time Stamps to Improve Efficiency in Marking Fields Within Objects,” havingSer.No. 09/327,399,and filingdate

SUMMARY

Jun. 7, 1999.

One embodiment of the present invention provides a System that facilitates marking of objects defined within an object-oriented programming System to keep track of accesses to fields within the objects. The System operatesby receiving a reference to a field within an object, and iden tifying a markingbit within the object that is associatedwith the field. Note that each marking bit within the object is associated with a different Subset offields within the object. Next, the System sets the markingbitto indicate thatat least

BACKGROUND

1. Field of the Invention

The present invention relates to performance enhance ments in object-oriented programming Systems. More Specifically, the presentinvention relatesto a method and an apparatus that Supports finer marking granularity for fields within objects defined within an object-oriented program ming System.

25

one field within the associated Subset of fields has been

referenced. Finally, the System performs the reference to the

2. Related Art

AS increasing Semiconductor integration densities allow more transistors tobe integrated onto a microprocessorchip,

field.

In one embodiment of the present invention, the object

computer designers are investigating different methods of

includes N marking bits numbered 0,1,2,...,N-1 and M

using these transistors to increase computer System perfor mance Some recent computerarchitectures exploit“instruc tion level parallelism,” in which a single central processing

fields numbered 0,1,2,..., M-1. In this embodiment, the

35

system identifiesthe markingbitassociated with the fieldby Starting with a field number for the field, and applying a modulo N operation to the field number to produce a number for the associated marking bit. In a variation on this embodiment, N is a power of two.

## unit (CPU) issues multiple instructions in a single cycle.

Given proper compilerSupport, instruction level parallelism has proven effective at increasing computational perfor mance acroSSa wide range ofcomputational taskS. However, inter-instruction dependencies generally limit the perfor mance gains realized from using instruction level parallel

40

In one embodiment of the present invention, the System Supports Space and time dimensional execution. To thisend, the System Supports a head thread that executeS program instructions and a Speculative thread that executeS program

ism to a factor of two or three.

Another method for increasing computational Speed is “speculative eXecution' in which a processor executes mul tiple branch paths simultaneously, or predicts a branch, So that the processor can continue executing without waiting for the result of the branch operation. By reducing depen dencies on branch conditions, Speculative execution can

instructions in advance of the head thread. The head thread

45

accesses a primary version ofthe object and the Speculative thread accesses a Space-time dimensioned version of the object. In this embodiment, the Steps of identifying the markingbit and Setting the markingbit take place for a read operation by the Speculative thread.

50

increase the total number of instructions issued.

In a variation on this embodiment, there exists a separate Set of markingbits for write operations. In this variation, if the reference is a write operation by the Speculative thread, the Steps of identifying the marking bit and Setting the marking bit involve the Separate Set of markingbits. Upon a Subsequent write operation to the field by the head thread, the head thread writes to both the primary version and the Space-time dimensioned version if the marking bit is unset, and otherwise writes to the primary version.

Unfortunately, conventional Speculative execution typi cally provides a limited performance improvement because only a Small number of instructions can be speculatively

executed. One reason for this limitation is that conventional

55

Speculative eXecution is typically performed at the basic block level, and basic blocks tend to include only a small

number of instructions. Another reason is that conventional

hardware structures used to perform Speculative eXecution can only accommodate a Small number of Speculative

In one embodiment of the present invention, during a Subsequent write, operation to the field by the head thread, the System determines ifthe markingbit associated with the field has been Set by executing a specialbit extract instruc tion to examine the marking bit.

60

instructions.

What is needed is a method and apparatus that facilitates Speculative execution of program instructions at a higher level of granularity So that many more instructions can be Speculatively executed.

In one embodiment of the present invention, if the object is an array object with N markingbits numbered0,1,2,..., N-1 and M array elements numbered 0, 1, 2, . . . , M-1,

65

One challenge in designinga System that Supports Specu

lative eXecution is to detect a rollback condition. A rollback

