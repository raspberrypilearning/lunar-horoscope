## Vary the spins

Give each wheel a different number of turns while keeping the correct result.

> [!TASK]
>
> Select **Zodiac Wheel**. Replace the `60` in its repeat block with this calculation; keep the blocks inside and below the loop.
>
> Build the left half, `pick random 2 to 6 × 60`, first. It chooses two to six full turns. Then add the right half, `((12 − Animal Index) mod 12) × 5`, which supplies the extra small turns needed to reach the chosen animal.
>
> ```blocks3
> when I receive [SPIN v]
> +repeat (((pick random (2) to (6)) * (60)) + ((((12) - (Animal Index)) mod (12)) * (5)))
>   turn cw (6) degrees
>   wait (0.01) seconds
> end
> point in direction ((90) - ((Animal Index) * (30)))
> ```
>
> Each animal slice takes five small turns because `30 ÷ 6 = 5`. The final direction block still sets the exact stopping position.

> [!TASK]
>
> Select **Element Wheel** and replace its repeat count too. There are five element slices, and each takes `72 ÷ 6 = 12` small turns.
>
> ```blocks3
> when I receive [SPIN v]
> +repeat (((pick random (2) to (6)) * (60)) + ((((5) - (Element Index)) mod (5)) * (12)))
>   turn cw (6) degrees
>   wait (0.01) seconds
> end
> point in direction ((90) - ((Element Index) * (72)))
> ```

> [!TASK]
>
> **Test your project.** Try `2026` several times and check that the wheels can finish at different times but always stop on **Horse** and **Fire**.
>
> Random choices can repeat, so two spins may sometimes look the same.
