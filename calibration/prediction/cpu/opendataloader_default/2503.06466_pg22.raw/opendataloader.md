## 5.8 Canonical Double Cover Construction

The following is a well-known recursive construction that preserves the degree of the original graph, and in the special case of the canonical double cover, it doubles its order and its cycles of odd lengths. This means that it produces a (k,g′)-graph from a (k,g)-graph of odd girth g, with g′ > g and even. For the sake of completeness, we present the construction, but only for the case when the starting graph is already a (k,g)-graph.

Let Γ be a finite (k,g)-graph, and let D(Γ) denote the set of darts of Γ, obtained by replacing each edge e of Γ with a pair of opposing darts (or arcs) e and e−1. A mapping α : D(Γ) → G is called a voltage assignment on Γ if it satisfies the condition α(e−1) = (α(e))−1 for all e ∈ D(Γ), where G is a group referred to as the voltage group. The voltage graph (also known as the derived graph or the lift) of Γ with respect to α, denoted by Γα, is a new graph with vertex set V (Γα) = V (Γ)×G and edge set E(Γα), where vertices ua and vb are adjacent in Γα if e = (u,v) ∈ D(Γ) and b = aα(e). A voltage graph Γα is a canonical double cover of Γ if the voltage group is Z2 and each edge of Γ is assigned the non-zero voltage 1 ∈ Z2. The canonical double cover construction is a particular type of voltage graph construction, which has been extensively studied by various authors (of the large number of articles considering the canonical double cover, consult, for example, [9, 12]). In our work, we applied the canonical double cover construction to obtain the following graphs: Graph(3,8,48;1), Graph(3,12,224;1), Graph(3,12,228), Graph(4,8,134), Graph(4,8,146), Graph(5,6,60), Graph(6,4,14),

- Graph(6,4,16), Graph(6,4,18), Graph(6,4,20), Graph(6,4,22), Graph(6,4,24), and
- Graph(7,4,16). As is well-known, a canonical double cover of a bipartite graph consists of two disconnected


copies of the original graph. Thus, using the canonical double cover construction systematically, we also obtained the following graphs, which are all disconnected but were used as starting graphs with respect to erasing vertices and adding edges as described in Subsection 5.3: (3,12)graph of order 252, (5,4)-graph of order 20, (5,8)-graph of order 304, and (7,4)-graph of order 28 (which consists of two disconnected copies of K7,7).

# 6 Concluding Remarks

As already stated in the introduction, the aim of the research and results presented in our paper is to gain insights into the structure of (k,g)-graphs; with the graphs of small orders being of particular interest. We conclude by outlining possible directions for future research or applications.

Of the several open questions highlighted in [7], there is one that is attributed to several authors and which is based on the simple observation that all known cages as well as record graphs of even girth happen to be bipartite. This lead to the repeatedly stated conjecture that all even-girth cages must be bipartite. Whether the conjecture holds true or not, it still leads to the following open problem we find both interesting and related to (k,g)-spectra:

For any given k ⩾ 3 and even g ⩾ 4, determine the smallest order n such that there exists a (k,g)-graph of order n which is not bipartite.

Our findings not only expand the current state of affairs with regard to the spectra of orders of (k,g)-graphs, but also highlight the challenges in determining complete spectra for larger values of k and g. The gaps in our results, particularly for higher girths, underscore the complexity of

22

