# arXiv:2503.08705v1 [math.OC] 9 Mar 2025

## A Block-Based Heuristic Algorithm for the Three-Dimensional Nuclear Waste Packing Problem

Yajie Wena,1, Defu Zhangb,2

Xiamen University, Siming south street 443, Xiamen, 361000, Fujian, China

#### ARTICLE INFO

#### ABSTRACT

Keywords: Three-dimensional packing Nuclear waste Heuristic

In this study, we present a block-based heuristic search algorithm to address the nuclear waste container packing problem in the context of real-world nuclear power plants. Additionally, we provide a dataset comprising 1600 problem instances for future researchers to use. Experimental results on this dataset demonstrate that the proposed algorithm effectively enhances the disposal pool’s space utilization while minimizing the radiation dose within the pool. The code and data employed in this study are publicly available to facilitate reproducibility and further investigation.

relationship is mathematically expressed as (1). 𝐻̇ =

### 1. Introduction

Thispaperaddressesthechallengeofnuclearwastetreatment in the context of a real-life nuclear power plant. During regular operation, nuclear power plants generate radioactive waste, which must be collected, classified into distinct boxes, and stored in pre-dug disposal pools. The waste packages are sealed with cement to ensure the safety of the environment and human health.

Γ ⋅ 𝐴 𝑟2

(1)

- • Dose Rate 𝐻̇ [Sv∕𝑡]: The amount of radiation absorbed per unit time, adjusted for biological effects.
- • Dose Rate Constant Γ [Sv ⋅ m2∕(Bq ⋅ 𝑡)]: A factor that describes how much radiation dose is received per unit of radioactive source activity at a given distance.
- • Activity 𝐴 [Bq]: The number of radioactive decay occurring per second.
- • Distance 𝑟 [m]: The distance from the radiation source to the point of measurement.


The waste packages within the pools must be strategically arranged to maximize disposal pool usage and reduce radiation exposure per unit time (measured in Sieverts per second) in each pool. This problem can be formulated as a three-dimensional knapsack problem with an additional constraint on the minimum radiation limit. To tackle this, the paper proposes a block-based heuristic algorithm, BSNA, to identify optimal placement strategies for the waste boxes.

For simplicity, let the vertical distance from the center point of the nuclear waste box to the top of the disposal pool be 𝑟. Given a disposal pool with length 𝐿, width 𝑊 , and height 𝐻, and a set of 𝑛 nuclear waste boxes, each with length 𝑙𝑖, width 𝑤𝑖, height ℎ𝑖, activity 𝐴𝑖, and dose rate constant Γ𝑖, the objective of the problem is to place as many nuclear waste boxes as possible into the disposal pool to maximize the utilization rate of the disposal pool, while minimizing the sum of the dose rates of all the nuclear waste boxes in the disposal pool. This problem is similar to a variant of the three-dimensional bin packing problem, as it has an additional optimization objective.

Furthermore, we generate 1600 synthetic nuclear waste packing problems based on real-world nuclear waste data to evaluate the proposed algorithm’s performance. These generated problems are intentionally more complex than typical real-world scenarios, incorporating larger disposal pools and a greater variety and volume of nuclear waste boxes. This provides a comprehensive test bed for assessing the algorithm’s effectiveness in more challenging settings.

### 2. Problem Description

The dose rate of a nuclear waste box at a given position, measured in Sieverts per second, is determined by the number of radioactive decay occurring per second, known as the activity, multiplied by the dose rate constant of the radioactive element. This value is then divided by the square of the distance between the nuclear element and the observation point. Since the dose rate constant for a specific nuclear element is a fixed value, the radiation dose of the nuclear waste box is directly proportional to the activity and inversely proportional to the square of the distance. The

### 3. Literature Review

The three-dimensional bin packing problem (3D-BPP or 3D-CLP) is a well-known NP-hard optimization problem. Over the years, various approaches have been developed to tackle this problem, including exact algorithms, heuristic algorithms, metaheuristic algorithms, and more recently, deep learning-based methods. Among these, heuristic and metaheuristic algorithms are the most widely adopted due to their practical efficiency in solving large-scale problems.

wynne.jei@gmail.com (Y. Wen); dfzhang@xmu.edu.cn (D. Zhang) ORCID(s): 0009-0004-2053-0583 (Y. Wen)

![](<2503.08705_pg1_images/imageFile1.png>)

Yajie Wen et al.: Preprint submitted to Elsevier Page 1 of 10

