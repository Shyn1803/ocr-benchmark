which is rewritten as mA∥u − uh∥2V ≤ ⟨Au − Auh,u − vh⟩ + ⟨Au,vh − u⟩ + ⟨Au,v − uh⟩

+ ⟨Au,u − v⟩ + ⟨Auh,uh − vh⟩. (4.40) Applying (4.2),

⟨Au,u − v⟩ ≤ Φ(v) − Φ(u) + I∆(ψ0(γψu;γψv − γψu)) − ⟨f,v − u⟩. Applying (4.16),

⟨Auh,uh − vh⟩ ≤ Φ(vh) − Φ(uh) + I∆(ψ0(γψuh;γψvh − γψuh)) − ⟨f,vh − uh⟩. Using these inequalities in (4.40), after some rearrangement of the terms, we have

mA∥u − uh∥2V ≤ ⟨Au − Auh,u − vh⟩ + Ru(vh,u) + Ru(v,uh) + Iψ(v,vh), (4.41) where

Ru(v,w) := ⟨Au,v − w⟩ + Φ(v) − Φ(w) + I∆(ψ0(γψu;γψv − γψw)) − ⟨f,v − w⟩, (4.42) Iψ(v,vh) := I∆(ψ0(γψu;γψv − γψu) + ψ0(γψuh;γψvh − γψuh))

− I∆(ψ0(γψu;γψvh − γψu) + ψ0(γψu;γψv − γψuh)). (4.43) Let us bound the first and the last two terms on the right hand side of (4.41). First,

⟨Au − Auh,u − vh⟩ ≤ LA∥u − uh∥V ∥u − vh∥V . By the modified Cauchy-Schwarz inequality (2.12), for any ϵ > 0 arbitrarily small, ⟨Au − Auh,u − vh⟩ ≤ ϵ∥u − uh∥2V + c∥u − vh∥2V (4.44)

for some constant c depending on ϵ. Applying the subadditivity of the generalized directional derivative,

ψ0(z;z1 + z2) ≤ ψ0(z;z1) + ψ0(z;z2) ∀z,z1,z2 ∈ Rm, we have

ψ0(γψu;γψv − γψu) ≤ ψ0(γψu;γψv − γψuh) + ψ0(γψu;γψuh − γψu),

ψ0(γψuh;γψvh − γψuh) ≤ ψ0(γψuh;γψvh − γψu) + ψ0(γψuh;γψu − γψuh). Thus,

Iψ(v,vh) ≤ I∆(ψ0(γψuh;γψvh − γψu) − ψ0(γψu;γψvh − γψu))

+ I∆(ψ0(γψu;γψuh − γψu) + ψ0(γψuh;γψu − γψuh)). By (4.8) and (4.12),

I∆(ψ0(γψu;γψuh − γψu) + ψ0(γψuh;γψu − γψuh)) ≤ αψI∆(|γψu − γψuh|2) ≤ αψc2∆∥u − uh∥2V .

21

