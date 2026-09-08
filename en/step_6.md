## Check the answer

Keep asking until the player enters a whole year from 1 to 9999.

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
