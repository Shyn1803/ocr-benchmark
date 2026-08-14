Thus, the necessary optimality condition for a two-player game provides the conditions under which both players’ controls are optimal in response to each other’s strategies. Each player’s control must satisfy the condition that the derivative of the Hamiltonian with respect to their control vanishes almost everywhere, ensuring that the strategy of each player is optimal given the strategy of the other player.

Proof. Consider the variation of the functional J1 with respect to the control u1. We compute the derivative:

d dϵ

. Expanding the objective functional:

J1(u1 + ϵv1,u2)

ϵ=0

d dϵ

J1(u1 + ϵv1,u2)

## = lim

ϵ→0

ϵ=0

1 ϵ

E

RZ

f1(ζ,Y (u1+ϵv1,u2)(ζ),u1(ζ) + ϵv1(ζ),u2(ζ))

− f1(ζ,Y (u1,u2)(ζ),u1(ζ),u2(ζ)) dζ + g1(Y (u1+ϵv1,u2)(Z)) − g1(Y (u1,u2)(Z)) .

Using the first-order expansion:

d dϵ

## = E

J1(u1 + ϵv1,u2)

ϵ=0

RZ

∂f1 ∂y

(ζ,Y (u1,u2)(ζ),u1(ζ),u2(ζ))G1(ζ)

∂f1 ∂u1

∂g1 ∂y

(ζ,Y (u1,u2)(ζ),u1(ζ),u2(ζ))v1(ζ) dζ +

+

(Y (u1,u2)(Z))G1(Z) ,

where G1 is the variation in the system’s state due to the change in control. We now decompose it into two terms:

d dϵ

= I1 + I2, where

J1(u1 + ϵv1,u2)

ϵ=0

I1 = E

+

RZ

∂H1 ∂y

(ζ) −

∂α ∂y

(ζ)p1(ζ) −

∂β ∂y

(ζ)q1(ζ) − (L1 ⋆

∂α ∂y

)(ζ) G1(ζ)dζ

RZ

∂H1 ∂u1

∂α ∂u1

(ζ) −

(ζ)p1(ζ) −

∂β ∂u1

(ζ)q1(ζ) − (L1 ⋆

∂α ∂u1

)(ζ) v1(ζ)dζ ,

# 18

