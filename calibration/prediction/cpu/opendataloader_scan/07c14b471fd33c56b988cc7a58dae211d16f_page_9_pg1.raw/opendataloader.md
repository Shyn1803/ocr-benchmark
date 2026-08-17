# METHOD AND APPARATUS FOR PROVIDING FINER MARKING GRANULARITY FOR FIELDS WITHIN OBJECTS

# Related Application

This application is related to the Subject matter in a pending U.S. patent application, entitled “Supporting Space Time Dimensional Program Execution by Selectively Ver Sioning Memory Updates,” by inventors Shailender Chaudhry and Marc Tremblay, having Ser. No. 09/313,229 and a filing date of May 17, 1999.

The Subject matter of this application is also related to the Subject matter in a co-pending non-provisional application by the same inventor(s) as the instant application and filed on the same day as the instant application entitled, “Using Time Stamps to Improve Efficiency in Marking Fields Within Objects,” having Ser. No. 09/327,399, and filing date Jun. 7, 1999.

15

20

# BACKGROUND

1. Field of the Invention

The present invention relates to performance enhance ments in object-oriented programming Systems. More Specifically, the present invention relates to a method and an apparatus that Supports finer marking granularity for fields within objects defined within an object-oriented program ming System.

25

30

2. Related Art

AS increasing Semiconductor integration densities allow more transistors to be integrated onto a microprocessor chip, computer designers are investigating different methods of using these transistors to increase computer System perfor mance Some recent computer architectures exploit “instruc tion level parallelism,” in which a single central processing unit (CPU) issues multiple instructions in a single cycle. Given proper compiler Support, instruction level parallelism has proven effective at increasing computational perfor mance acroSS a wide range of computational taskS. However, inter-instruction dependencies generally limit the perfor mance gains realized from using instruction level parallel ism to a factor of two or three.

Another method for increasing computational Speed is “speculative eXecution' in which a processor executes mul tiple branch paths simultaneously, or predicts a branch, So that the processor can continue executing without waiting for the result of the branch operation. By reducing depen dencies on branch conditions, Speculative execution can increase the total number of instructions issued.

50

Unfortunately, conventional Speculative execution typi cally provides a limited performance improvement because only a Small number of instructions can be speculatively executed. One reason for this limitation is that conventional Speculative eXecution is typically performed at the basic block level, and basic blocks tend to include only a small number of instructions. Another reason is that conventional hardware structures used to perform Speculative eXecution can only accommodate a Small number of Speculative instructions.

55

60

What is needed is a method and apparatus that facilitates Speculative execution of program instructions at a higher level of granularity So that many more instructions can be Speculatively executed.

One challenge in designing a system that supports specu lative execution is to detect a rollback condition. A rollback condition can occur in a number of situations. For example_ rollback condition occurs when a speculative thread that is executing program instructions in advance of a head thread reads from memory element before the head thread performs write to the memory element. In this case, the speculative thread must "rollback so that it can read the value stored by the head thread. A rollback condition can be detected by "marking memory elements as are read by the speculative  thread so that the head thread can subse 10   quently determine if the memory elements have been read by the speculative thread. Unfortunately; separate marking indicator for each memory element can consume large amount of memory; which can reduce cache hit rates arid thereby degrade system performance . they using What is needed is a method and an apparatus for marking memory elements that does   require amount of memory for large storing

# SUMMARY

One embodiment of the present invention provides a System that facilitates marking of objects defined within an object-oriented programming System to keep track of accesses to fields within the objects. The System operates by receiving a reference to a field within an object, and iden tifying a marking bit within the object that is associated with the field. Note that each marking bit within the object is associated with a different Subset of fields within the object. Next, the System sets the marking bit to indicate that at least one field within the associated Subset of fields has been referenced. Finally, the System performs the reference to the field.

In one embodiment of the present invention, the object includes N marking bits numbered 0,1,2,...,N-1 and M fields numbered 0,1,2,..., M-1. In this embodiment, the system identifies the marking bit associated with the field by Starting with a field number for the field, and applying a modulo N operation to the field number to produce a number for the associated marking bit. In a variation on this embodiment, N is a power of two.

35

40

In one embodiment of the present invention, the System Supports Space and time dimensional execution. To this end, the System Supports a head thread that executeS program instructions and a Speculative thread that executeS program instructions in advance of the head thread. The head thread accesses a primary version of the object and the Speculative thread accesses a Space-time dimensioned version of the object. In this embodiment, the Steps of identifying the marking bit and Setting the marking bit take place for a read operation by the Speculative thread.

45

In a variation on this embodiment, there exists a separate Set of marking bits for write operations. In this variation, if the reference is a write operation by the Speculative thread, the Steps of identifying the marking bit and Setting the marking bit involve the Separate Set of marking bits. Upon a Subsequent write operation to the field by the head thread, the head thread writes to both the primary version and the Space-time dimensioned version if the marking bit is unset, and otherwise writes to the primary version.

In one embodiment of the present invention, during a Subsequent write, operation to the field by the head thread, the System determines if the marking bit associated with the field has been Set by executing a special bit extract instruc tion to examine the marking bit.

In one embodiment of the present invention, if the object is an array object with N marking bits numbered 0,1,2,..., N-1 and M array elements numbered 0, 1, 2, . . . , M-1,

65

