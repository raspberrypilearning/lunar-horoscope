## Find a place in the cycle

Turn the year into a position in a repeating 60-year cycle.

> [!TASK]
>
> On the **Stage**, create a variable called `Cycle`. Leave it ticked and untick `Birth Year` to make room on the Stage.
>
> The project uses `1984` as position `0`. After position `59`, the cycle returns to `0`.

> [!TASK]
>
> Add a `set Cycle` block **below the whole repeat-until loop**, outside it. Build its calculation from the inside out: subtract `1984` from `Birth Year`, use `mod 60`, add `60`, then use `mod 60` again.
>
> ```blocks3
> +set [Cycle v] to (((((Birth Year) - (1984)) mod (60)) + (60)) mod (60))
> ```
>
> **Mod** gives the remainder after division: `61 mod 60` is `1`. The extra `+ 60` and `mod 60` keep the result in the range `0` to `59`, including for years before 1984, and match the completed project.

> [!TASK]
>
> **Test your project.** Restart for each year and check that `1984` gives **Cycle** `0`, `2024` gives `40`, `2044` gives `0`, and `1983` gives `59`.
