Lemma 2.3. For a binary (near) equireplicate r × c row-column design on v symbols,

- (a) λrc = e− + e+ − e

−e+

![](<2503.07166_pg4_images/imageFile1.png>)

e = e + (e

+−e)(e−e−)

![](<2503.07166_pg4_images/imageFile2.png>)

e ,

- (b) λ−rc = e− and λ+rc = e+,
- (c) λrr = c(λ

rc−1) r−1 ,

![](<2503.07166_pg4_images/imageFile3.png>)

- (d) λcc = r(λ


rc−1) c−1 .

![](<2503.07166_pg4_images/imageFile4.png>)

Remark 2.4. Lemma 2.3 (a) implies that λrc ≥ e, and that the equality holds if and only if e is an integer, i.e. the row-column design is equireplicate.

Proof of Lemma 2.3. For an equireplicate design all claims hold due to Lemma 2.2, so from now on we assume that it is near equireplicate, that is, e− < e < e+. Noting that v = v− + v+, a double counting argument similar to the proof of Lemma 2.2 together with Lemma 2.1 gives that the number of common symbols summed over all pairs of a row and a column is

rcλrc = v−(e−)2 + v+(e+)2 = v(e+ − e)(e−)2 + v(e − e−)(e+)2. Dividing by v and using e = rc/v, we get

eλrc = (e+ − e)(e−)2 + (e − e−)(e+)2 = e((e+)2 − (e−)2) + e−e+(e− − e+). (1) Note that e+ − e− = 1, so (e+)2 − (e−)2 = e+ + e−, thus

eλrc = e(e+ + e−) − e−e+,

from which (a) follows. In order to prove (b) it suﬃces to show that e− < λrc < e+, which follows from (a):

(e+ − e)(e − e−) e

e− < e < e +

= λrc,

![](<2503.07166_pg4_images/imageFile5.png>)

(e+ − e)(e − e−) e

e − e− e

= e + (e+ − e) ·

< e + (e+ − e) = e+.

λrc = e +

![](<2503.07166_pg4_images/imageFile6.png>)

![](<2503.07166_pg4_images/imageFile7.png>)

Again using double counting and Lemma 2.1, the number of common symbols summed over all pairs of rows is

e+ 2

e+ 2

e− 2

e− 2

r 2

= v(e+ − e)

+ v(e − e−)

. Dividing by v/2, we get

+ v+

λrr = v−

r(r − 1)λrr v

= (e+ − e)e−(e− − 1) + (e − e−)e+(e+ − 1)

![](<2503.07166_pg4_images/imageFile8.png>)

= e((e+)2 − (e−)2) + e+e−(e− − e+) + e(e− − e+)

= eλrc − e,

where the last equality follows from (1). This implies (c), and a similar count gives (d). Having done this ground work, we now formally deﬁne our main object of study.

![](<2503.07166_pg4_images/imageFile9.png>)

![](<2503.07166_pg4_images/imageFile10.png>)

![](<2503.07166_pg4_images/imageFile11.png>)

![](<2503.07166_pg4_images/imageFile12.png>)

Deﬁnition 2.5. An (r × c,v)-near triple array is a binary (near) equireplicate r × c row-column design on v symbols in which

- 1. any row and column have either λ−rc or λ+rc common symbols,
- 2. any two rows have either λ−rr or λ+rr common symbols,
- 3. any two columns have either λ−cc or λ+cc common symbols.


Note that the deﬁnition allows a near triple array to be equireplicate. To avoid having to calculate the quantities involved in the deﬁnition explicitly, it will often be convenient to instead use the following alternative characterization of near triple arrays.

4

