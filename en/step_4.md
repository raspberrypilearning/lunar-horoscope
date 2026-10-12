## Ask for and check a year

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

Now keep asking until the player enters a whole year from 1 to 9999.

> [!TASK]
>
> On the **Stage**, attach a **Control** `repeat until` block below `set Birth Year`. Inside it, add a second question and another `set Birth Year to round answer` block.

> [!TASK]
>
> Build the condition from **Operators** blocks. Start with `answer = Birth Year`, put it inside an `and` with `Birth Year > 0`, then put that pair inside another `and` with `Birth Year < 10000`.
>
> Drag the orange oval `Birth Year` into each comparison; do not type its name into a white box.
>
> ```blocks3
> set [Birth Year v] to (round (answer))
> +repeat until <<<(answer) = (Birth Year)> and <(Birth Year) > (0)>> and <(Birth Year) < (10000)>>
> +  ask [Please enter one whole numerical year, for example 2024.] and wait
> +  set [Birth Year v] to (round (answer))
> +end
> ```
>
> The first comparison checks that rounding did not change the answer. The other two check the range. All three checks must be true before the loop finishes.

> [!TASK]
>
> **Test your project.** Enter `hello`, `0`, `10000`, and `2024.5` in turn to check that the question reappears each time, then enter `2024` and check that the question disappears.
