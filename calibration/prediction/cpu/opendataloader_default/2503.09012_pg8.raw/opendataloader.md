8

![](<2503.09012_pg8_images/imageFile1.png>)

FIG. 3. The one-shot work cost 𝑊𝜀(𝜌𝐴𝐵; 𝜎𝐴′𝐵′) of converting Alice’s system in the presence of Bob’s side information is calculated as follows. Initially, Alice’s and Bob’s systems are in the state 𝜌𝐴𝐵, and Alice has access to a battery system 𝐴0 in a pure state representing her initial work storage. Supposedly without doing work, they perform a conditionally uniformity-covariant operation N𝐴0𝐴𝐵→𝐴1𝐴′𝐵′ such that the state 𝜏𝐴1𝐴′𝐵′ after the operation is 𝜀-close to the target state 𝜎𝐴′𝐵′ in tensor product with a pure state of a battery system 𝐴1 representing Alice’s final work storage. According to Landauer’s principle, Alice has to invest (1/𝛽b)(log2|𝐴0| − log2|𝐴1|) or extract (1/𝛽b)(log2|𝐴1| − log2|𝐴0|) work to “recharge” or “discharge” her battery afterwards, returning her work storage to the initial level. This completes the the desired conversion from 𝐴 to 𝐴′ without causing significant change to the environment (specifically, the battery), and the work cost of the whole process boils down to the amount of work involved in Alice’s recharging or discharging her battery.

that the desired conversion can always be completed. In the end, the decrease or increase in the number of pure qubits in the battery gives a precise account for the overall amount of work invested to or extracted from the conversion. Third, as argued in Sec. IIA, every legitimate operation that can be performed without work supply must fall within the scope of conditionally uniformity-covariant operations. Here, we assume that the converse is also true, namely that all such operations can be performed freely, so that the work cost defined under such oper-

ations is equal to the actual work cost in its literal sense. Note that even in a less permissive setting without this assumption, the work cost defined under conditionally uniformity-covariant operations still provides a no-go limit on the actual work cost. Fourth, we accommodate the practical need for approximate conversion, where a bounded error is tolerated.

Formally, for a pair of states 𝜌𝐴𝐵, 𝜎𝐴′𝐵′, we define the oneshot work cost of converting 𝐴 to 𝐴′ with error 𝜀 ∈ [0, 1] as

𝑊𝜀(𝜌𝐴𝐵; 𝜎𝐴′𝐵′) ≔

1 𝛽b

inf

𝐴0,𝐴1, N𝐴0𝐴𝐵→𝐴1𝐴′𝐵′ ∈CUCO

log2 |𝐴0| − log2 |𝐴1| : Δ |0⟩⟨0|𝐴1 ⊗ 𝜎𝐴′𝐵′, N𝐴0𝐴𝐵→𝐴1𝐴′𝐵′ |0⟩⟨0|𝐴0 ⊗ 𝜌𝐴𝐵 ≤ 𝜀 ,

(40)

where CUCO denotes the set of conditionally uniformitycovariant operations. In Eq. (40), 𝐴0 and 𝐴1 are the battery systems representing Alice’s initial and final work storage, respectively. A positive work cost means that Alice has to release this amount of work from her storage and invest it into the conversion; a negative work cost means that Alice can extract an amount of work, equal to the absolute value of the work cost, from the conversion and keep it in her storage. See Fig. 3 for an illustration.

We now focus on two particular conversion tasks, namely preparation and erasure with side information. For a state 𝜌𝐴𝐵,

the one-shot work costs of preparing and erasing the system 𝐴 with error 𝜀 ∈ [0, 1] are defined, respectively, as

𝑊prep𝜀 (𝜌𝐴𝐵) ≔ 𝑊𝜀(|0⟩⟨0|𝐴; 𝜌𝐴𝐵), (41) 𝑊eras𝜀 (𝜌𝐴𝐵) ≔ 𝑊𝜀(𝜌𝐴𝐵; |0⟩⟨0|𝐴). (42)

In other words, the preparation task refers to putting Alice’s system in a given state, coupled with Bob’s system, when it is initialized to a default pure state; the erasure task refers to the reverse process of overwriting Alice’s system with the default pure state when it is initialized to the given state. Our first

