## Build the result

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

Join the year, element, and animal into one result.

> [!TASK]
>
> Select the **Stage** and create `Your Sign`. Untick `Costume Number`.
>
> Insert `hide variable Your Sign` after `switch backdrop to Spinner` at the **top** of the Stage’s `START` script. This clears the previous result from view when a new turn starts.
>
> ```blocks3
> when I receive [START v]
> switch backdrop to (Spinner v)
> +hide variable [Your Sign v]
> hide list [Your Traits v]
> delete all of [Your Traits v]
> ```

> [!TASK]
>
> At the **bottom** of the same script, after `set Costume Number`, add `set Your Sign` with four nested **Operators** `join` blocks.
>
> Build from the inside out: join a single space to `Animal Name`, join `Element Name` to that, join ` • ` to that, then join `Birth Year` to the whole result. You can copy the bullet `•` from this sentence; put one space on each side of it.
>
> ```blocks3
> set [Costume Number v] to ((((Animal Index) * (5)) + (Element Index)) + (1))
> +set [Your Sign v] to (join (Birth Year) (join [ • ] (join (Element Name) (join [ ] (Animal Name)))))
> ```

> [!TASK]
>
> **Test your project.** Enter `2024`, then tick **Your Sign** in Variables after answering to check that it reads `2024 • Wood Dragon`.
>
> The green flag hides this display on each run, so tick it after answering whenever you want to inspect the text.
