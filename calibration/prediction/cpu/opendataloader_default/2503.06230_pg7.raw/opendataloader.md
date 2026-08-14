Proposition 3.0.8. [8, Proposition 6] Soit L un anneau de Lie Mc tel que pour tout x ∈ L, il existe un n tel que [x+y,n x] = [y,n x] = 0 pour tout y ∈ L′. Alors L est nilpotent.

Démonstration. On procède par récurrence sur la classe de résolubilité, le cas abélien étant trivial. On peut donc supposer que L′ est nilpotent. Il suﬃt de montrer par récurrence que tout centre itéré de L′ est contenu dans un centre itéré de L : il existera alors un indice i tel que L′ = Zn(L′) ≤ Zi(L) et donc L/Zi(L) est abélien et L = Zi+1(L). Evidemment, {0} = Z0(L′) est contenu dans Z0(L). Supposons que Zi(L′) ≤ Zk(L); les sous-anneaux Zi+1(L′) et Zi(L′) sont des idéaux de L. On considère A = Zi+1(L′)/Zi(L′); c’est un anneau de Lie abélien sur lequel L agit de façon adjointe, de sorte que A est un L-module. L’anneau de Lie A est centralisé par L′ et on obtient donc une structure de L/L′-module.

Comme L est Zf, il existe x1,...,xn dans L tels que CA(L) = CA(x1,..,xn). Pour tout xi, il existe un entier ni tel que [xi + y,n

xi] = 0 ; ainsi, pour tout y ∈ L′, l’action de xi + y sur A coïncide avec celle de xi. D’après le Lemme 3.0.7, on obtient donc pour tout y ∈ Zi+1(L′), [y,m L] ≤ Zi(L′) ≤ Zk(L) pour m = 1 + ki=1(ni − 1). Par conséquent, d’après la Proposition 2.0.6, y ∈ Zk+m(L). Finalement, Zi+1(L′) ≤ Zk+m(L).

xi] = [y,n

i

i

![](<2503.06230_pg7_images/imageFile1.png>)

![](<2503.06230_pg7_images/imageFile2.png>)

![](<2503.06230_pg7_images/imageFile3.png>)

![](<2503.06230_pg7_images/imageFile4.png>)

Théorème 3.0.9. [8, Theorem 8] Soit L un anneau de Lie Mc. Alors F(L) est un idéal nilpotent.

Démonstration. L’idéal F = F(L) est localement nilpotent et donc résoluble d’après la Proposition 3.0.3. Soit x ∈ F ; cet élément appartient à un idéal nilpotent I de L, de classe de nilpotence r. Par conséquent, pour un élément y de F′, [x,y] ∈ I et donc adrx(x + y) = adrx(y) = 0. On conclut d’après la Proposition 3.0.8.

![](<2503.06230_pg7_images/imageFile5.png>)

![](<2503.06230_pg7_images/imageFile6.png>)

![](<2503.06230_pg7_images/imageFile7.png>)

![](<2503.06230_pg7_images/imageFile8.png>)

# 4 Théorème de Engel

Dans cette section, nous allons établir un analogue du théorème de Engel. Sauf mention explicite du contraire, L est une algèbre de Lie sur un corps de caractéristique nulle. D’après les travaux de Hartley, il est possible de déﬁnir un analogue du radical de Baer dans ce contexte.

Déﬁnition 4.0.1. Soit L une algèbre de Lie. On dit que H est un sous-idéal de L s’il existe une suite ﬁnie de sous-algèbres telle que :

H0 = H ⊳ H1 ⊳ ... ⊳ Hn = L.

L’indice d’un sous-idéal désigne la longueur minimale d’une suite de la forme précédente.

Fait 4.0.2. [9] Le radical de Baer B(L) est la sous-algèbre engendrée par les sous-idéaux nilpotents et de dimension ﬁnie. On a :

7

