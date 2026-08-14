so we can get

 

dt = x2 + b

# b10x1x2 + b

# b10x21x2 + b

dx1

# b210x22 + b

# b210x1x22 + b

b310x31 + O(∥x∥4)

11

20

21

12

30



dx2

dt = a11x1x2 + a

b10 x22 + a

# b10 x1x22 + a12x21x2 + a

b210 x32 + O(∥x∥4)

20

21

30

 

x3 = x1 x4 = x2 + b



# b10x21x2 + b

# b10x1x2 + b

# b210x22 + b

# b210x1x22 + b

b310x31 + O(∥x∥4)

21

11

20

12

30

 

x1 = x3 x2 = x4 + v11x3x4 + v02x24 + v21x23x4 + v12x3x24 + v03x34 + O(∥x∥4)



wherein:

b11 b10

b20 b210

# v11 = −

,v02 = −

,

b211 − b12b10 b210

v21 =

.

2b220 b410

3b11b20 − b21b10 b310

,v03 =

.

# v12 =

Substitute the new variables (x3,x4) into the original system, and we can get:

 

dx3

dt = x4



dx4

dt = e11x3x4 + e02x24 + e21x23x4 + e12x3x24 + e03x34 + O(∥x∥4)

wherein:

- e11 = a11, e02 =

a20 + b21 b10

,

e21 = a12 +

- a11b11

- b10


+ a11v11,

- e12 = a12v02 +


(a20 + b11)b10 + a21b10 + 2a11b20 + a20b11 + b211 + 2b10b12 b210

,

2(a20 + b11)b210v02 + a30 + b21 + 2a20b20 + b11b20 b310

e03 =

.

Then make the following transformation for the system (14):

 

x5 = x3 x6 = x4 − e02x3x4



15

(14)

