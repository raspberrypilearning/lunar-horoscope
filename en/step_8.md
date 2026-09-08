## Find the animal

Use the cycle position to look up an animal in the supplied list.

> [!TASK]
>
> On the **Stage**, create `Animal Index` and `Animal Name`. Leave both ticked and untick `Cycle`.
>
> An **index** is a position. This calculation gives positions `0` to `11`, one for each animal. Add the new block below `set Cycle`.
>
> ```blocks3
> set [Cycle v] to (((((Birth Year) - (1984)) mod (60)) + (60)) mod (60))
> +set [Animal Index v] to ((Cycle) mod (12))
> ```

> [!TASK]
>
> Add a `set Animal Name` block below it. Find `item 1 of Animal Names` in **Variables**, then put `Animal Index + 1` in the item number.
>
> ```blocks3
> set [Animal Index v] to ((Cycle) mod (12))
> +set [Animal Name v] to (item ((Animal Index) + (1)) of [Animal Names v])
> ```
>
> Scratch lists start at item `1`, so we add `1` to the index: index `0` looks up item `1`, which is `Rat`.

> [!TASK]
>
> **Test your project.** Enter `2024` to check that **Animal Index** is `4` and **Animal Name** is `Dragon`, then restart with `2025` to check for index `5` and `Snake`.
