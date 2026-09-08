## Ask for a year

Ask the player for a year and store their answer in a variable.

> [!TASK]
>
> Select the **Stage** and choose **Variables → Make a Variable**. Name it `Birth Year`, including the space and capital letters. Creating it on the Stage makes it available to every sprite.
>
> Leave its checkbox ticked so you can see its value on the Stage.

> [!TASK]
>
> Find the Stage’s existing `when I receive START` script. Add these two blocks at its bottom, after `delete all of Your Traits`.
>
> Use **Sensing** for `ask and wait` and `answer`, **Variables** for `set`, and **Operators** for `round`. Drag the oval `answer` into `round`, then drag that into the `set` block.
>
> ```blocks3
> when I receive [START v]
> switch backdrop to (Spinner v)
> hide list [Your Traits v]
> delete all of [Your Traits v]
> +ask [Enter a whole birth year \[YYYY\]. Born before Lunar New Year? Enter the previous year.] and wait
> +set [Birth Year v] to (round (answer))
> ```
>
> `START` is a **broadcast**, a message that scripts can listen for. The green flag already sends this message. For now, use the example year `2024`; you do not need to enter your own birth year.

> [!TASK]
>
> **Test your project.** Click the green flag, enter `2024`, and check that the **Birth Year** display changes to `2024`.
