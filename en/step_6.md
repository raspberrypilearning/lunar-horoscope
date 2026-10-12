## Find the animal and element

Use the cycle position to look up an animal and an element in the supplied lists.

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
> Create `Element Index` and `Element Name`. Leave them ticked and untick the two animal variables.
>
> Insert `set Element Index` **between** `set Animal Index` and `set Animal Name`. Use the **Operators** block with a dropdown, usually labelled `abs`, and choose `floor`. Build `Cycle mod 10`, divide it by `2`, then put that inside `floor`.
>
> ```blocks3
> set [Animal Index v] to ((Cycle) mod (12))
> +set [Element Index v] to ([floor v] of (((Cycle) mod (10)) / (2)))
> set [Animal Name v] to (item ((Animal Index) + (1)) of [Animal Names v])
> ```
>
> `floor` rounds down: `floor of 1.5` is `1`. This groups the cycle positions into pairs and gives an index from `0` to `4`.

> [!TASK]
>
> Add the element lookup below `set Animal Name`. The **Element Names** list is already in the order `Wood`, `Fire`, `Earth`, `Metal`, `Water`.
>
> ```blocks3
> set [Animal Name v] to (item ((Animal Index) + (1)) of [Animal Names v])
> +set [Element Name v] to (item ((Element Index) + (1)) of [Element Names v])
> ```

> [!TASK]
>
> **Test your project.** Check these years:
>
> - `2024`: animal index `4`, **Dragon**, element index `0`, **Wood**
> - `2025`: animal index `5`, **Snake**, element index `0`, **Wood**
> - `2026`: animal index `6`, **Horse**, element index `1`, **Fire**
