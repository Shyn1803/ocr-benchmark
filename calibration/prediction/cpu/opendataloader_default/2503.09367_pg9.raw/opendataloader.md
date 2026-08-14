z2 z3

zc−1

z1

zc

F′

y2

y1

ap

bq

L1

ap−1

T

bq−1

L2

a1

b1

ws−1 ws

x2

x1

Bs−1 Bs Bs+1

Figure 3: Some notations on Bs.

a contradiction. If |G2| ≥ t, then |Br| = |G2| ≥ t and m(Br) < m(G2) = m(G). Since Br is 2-connected and

n − (t − 1) 3t − 7

− 1 =

m(Br) ≤ m(G) − 1 <

![](<2503.09367_pg9_images/imageFile1.png>)

contradicting the choice of G.

n − (3t − 7) − (t − 1) 3t − 7

![](<2503.09367_pg9_images/imageFile2.png>)

|Br| − (t − 1) 3t − 7

<

,

![](<2503.09367_pg9_images/imageFile3.png>)

# 4 Proof of Theorem 1.5

The proof proceeds by induction. If klog2 3 ≤ n ≤ 36klog2 3, then

k3 4

n 36k1+log2 3 +

e(G) ≤ 3n − 6 ≤ 3n − 6 −

, the result holds. So, we assume that

![](<2503.09367_pg9_images/imageFile4.png>)

![](<2503.09367_pg9_images/imageFile5.png>)

n > 36klog2 3. (2)

Let G be a 2Ck-free plane graph with e(G) = exP(n,2Ck). It is clear that G is connected; otherwise we can add an edge between two components of G to make it remain 2Ck-free, a contradiction. If G is Ck-free, then by Theorem 1.3, e(G) ≤ 3n − 6 − 4k n

2

≤ 3n − 6 − 36k n

+ k

2 , the result holds. So, we assume that G contains a Ck.

![](<2503.09367_pg9_images/imageFile6.png>)

![](<2503.09367_pg9_images/imageFile7.png>)

![](<2503.09367_pg9_images/imageFile8.png>)

log2 3

1+log2 3

- Case 1. G is 2-connected.

In that case, the boundary of each face in G is a cycle. Assume that c is the smallest number of vertices that need to be removed from G to make it Ck-free, and let v1,v2,...,vc be one such set of vertices. Then c ≤ k, since we can remove vertices of a k-cycle to make it Ck-free. Moreover, for any i,j ∈ [c], there exists a k-cycle in G such that vi is contained in the k-cycle, but vj not.

- Case 2.1. c = 1.


Since G is 2-connected, it follows that G′ = G − v1 is connected and is Ck-free. Assume that G′ has r blocks B1,B2,...,Br, where |Bi| ≥ klog2 3 for i ∈ [q] and |Bi| < klog2 3 for q + 1 ≤ i ≤ r. For each i ∈ [q], since Bi is a Ck-free 2-connected plane graph, it follows that

|Bi| − (klog2 3 − 1) 3klog2 3 − 7

m(Bi) ≥

;

![](<2503.09367_pg9_images/imageFile9.png>)

9

