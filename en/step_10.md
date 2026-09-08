## Choose the animal costume

Choose the costume that matches both the animal and the element.

> [!TASK]
>
> On the **Stage**, create `Costume Number`. Leave it ticked and untick the two element variables.
>
> There are five costumes for each animal. Multiply `Animal Index` by `5` to skip earlier animals, add `Element Index` to choose its element, then add `1` because costume numbers start at `1`.
>
> Attach this block below `set Element Name`.
>
> ```blocks3
> set [Element Name v] to (item ((Element Index) + (1)) of [Element Names v])
> +set [Costume Number v] to ((((Animal Index) * (5)) + (Element Index)) + (1))
> ```

> [!TASK]
>
> Select **Animal**, then **Code**. Add a new **Events** `when I receive` hat and choose **New message** to create `REVEAL`.
>
> Add these blocks to choose the costume and place the animal on the Stage. Drag the orange oval `Costume Number` into the costume dropdown.
>
> ```blocks3
> +when I receive [REVEAL v]
> +switch costume to (Costume Number)
> +go to x: (-118) y: (-42)
> +set size to (68) %
> +show
> +go to [front v] layer
> ```

> [!TASK]
>
> **Test your project.** Enter `2024` to check that **Costume Number** is `21`, then click the Animal sprite’s `when I receive REVEAL` hat to see its `dragon_wood` costume appear.
>
> This click tests just the Animal script; later your Stage code will send `REVEAL` to every sprite, and the green flag will hide the animal again.
