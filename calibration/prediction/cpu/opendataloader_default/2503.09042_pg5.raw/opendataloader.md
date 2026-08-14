5

Lemma 3.2. Let k > 0 and let 0 < ϵ < 1/4. Assume that

- (3.1) P[g(X) ≥ k] ≤ ϵ. Then

E Xf(Y )Yg(X) ≤

- 1

- 2 − (1 − 4ϵ)2−k+1.


Proof. Recall our notation Wf,g = E Xf(Y )Yg(X) . Since X is independent of Y , since X and −X have the same distribution, and since Y and −Y have the same distribution, (X,Y ) has the same joint distribution as (X,−Y ), (−X,Y ) or (−X,−Y ). Hence

Wf,g = E −Xf(−Y )Yg(X) = E −Xf(Y )Yg(−X) = E Xf(−Y )Yg(−X) . Summing these and rearranging yields

4Wf,g = E (Xf(Y ) − Xf(−Y ))(Yg(X) − Yg(−X)) .

Let BY be the event that Y1 = Y2 = ··· = Yk−1, and note that P[BY ] = 2−(k−2). Write

4Wf,g =E (Xf(Y ) − Xf(−Y ))(Yg(X) − Yg(−X)) {BY }

- (3.2) + E (Xf(Y ) − Xf(−Y ))(Yg(X) − Yg(−X)) {BYc } . Consider the first term on the right hand side. Since P[g(−X) ≥ k] = P[g(X) ≥ k] ≤ ϵ, we have that P[g(X) ≥ k or g(−X) ≥ k] ≤ 2ϵ, by the union bound. Now, if g(X) < k and g(−X) < k then, under the event BY , Yg(X) = Yg(−X). Hence


(Yg(X) − Yg(−X)) · {BY } = (Yg(X) − Yg(−X)) · {g(X)≥k or g(−X)≥k} · {BY }. We thus have by independence of X and Y that

E (Xf(Y ) − Xf(−Y ))(Yg(X) − Yg(−X)) {BY }

= E (Xf(Y ) − Xf(−Y )) · (Yg(X) − Yg(−X)) · {g(X)≥k or g(−X)≥k} · {BY } ≤ E 4 · {g(X)≥k or g(−X)≥k} · {BY }

= 4P[g(X) ≥ k or g(−X) ≥ k,BY ]

= 4P[g(X) ≥ k or g(−X) ≥ k]P[BY ] ≤ 8ϵ2−(k−2). Consider now the second term on the right hand side of (3.2). Noting

that P Xf(Y ) = Xf(−Y ) Y = y ≥ 1/2 for any y, we get that

E (Xf(Y ) − Xf(−Y ))(Yg(X) − Yg(−X)) {BYc } ≤ 2P[BYc ] = 2(1 − 2−(k−2)). Substituting these two bounds back into (3.2) and diving by 4, we get

1 4

Wf,g ≤

- 1

- 2 − (1 − 4ϵ)2−k+1.


8ϵ2−(k−2) + 2(1 − 2−(k−2)) =

□

