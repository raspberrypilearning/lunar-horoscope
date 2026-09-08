## Build the result text

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
