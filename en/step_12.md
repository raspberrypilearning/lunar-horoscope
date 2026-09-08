## Spin the animal wheel

Make the animal wheel turn and stop on the chosen animal.

> [!TASK]
>
> Select **Zodiac Wheel**. Add this **new script**, leaving its `START` script in place. In the **Events** hat’s dropdown, choose **New message** and name it `SPIN`.
>
> Use **Control** for the repeat and wait blocks, and **Motion** for turn and point in direction. The `turn right` block has a clockwise arrow.
>
> ```blocks3
> +when I receive [SPIN v]
> +repeat (60)
> +  turn cw (6) degrees
> +  wait (0.01) seconds
> +end
> +point in direction ((90) - ((Animal Index) * (30)))
> ```
>
> Sixty turns of 6 degrees make one full turn: `60 × 6 = 360`. The final block lines up the result under the pointer. There are 12 animals, so each slice is `360 ÷ 12 = 30` degrees.

> [!TASK]
>
> Select the **Stage**. Attach these blocks at the bottom of its `START` script, immediately after `set Your Sign`.
>
> ```blocks3
> set [Your Sign v] to (join (Birth Year) (join [ • ] (join (Element Name) (join [ ] (Animal Name)))))
> +broadcast [SPIN v] and wait
> +wait (0.6) seconds
> ```
>
> `broadcast and wait` lets the wheel finish before the Stage continues. The extra pause will let the player see where the wheels stop.

> [!TASK]
>
> **Test your project.** Enter `2024` and check that the animal wheel spins once, then lines up **Dragon** under its pointer while the element wheel stays still.
