## Spin the element wheel

Make the second wheel spin at the same time and stop on the chosen element.

> [!TASK]
>
> Select **Element Wheel** and add this new script. Choose the existing `SPIN` message, and use `Element Index` in the direction calculation.
>
> ```blocks3
> +when I receive [SPIN v]
> +repeat (60)
> +  turn cw (6) degrees
> +  wait (0.01) seconds
> +end
> +point in direction ((90) - ((Element Index) * (72)))
> ```
>
> This wheel has five slices, so each is `360 ÷ 5 = 72` degrees. Both wheels receive the same message and run together; the Stage waits for both to finish.

> [!TASK]
>
> **Test your project.** Enter `2026` and check that both wheels spin, then stop with **Horse** and **Fire** under their pointers.
