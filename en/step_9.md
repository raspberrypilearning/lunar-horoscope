## Find the element

Look up an element that changes every two years.

> [!TASK]
>
> On the **Stage**, create `Element Index` and `Element Name`. Leave them ticked and untick the two animal variables.
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
> **Test your project.** Restart for each year and check that `2024` and `2025` both give **Element Name** `Wood` with index `0`, while `2026` gives `Fire` with index `1`.
