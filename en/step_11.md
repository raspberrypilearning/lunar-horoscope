## Reveal the result

Arrange the result screen and show the sign, traits, and animal together.

> [!TASK]
>
> Select **Zodiac Wheel** and add this new script using the existing `REVEAL` message. It makes space for the animal by shrinking the wheel and moving it to the top.
>
> ```blocks3
> +when I receive [REVEAL v]
> +go to x: (-180) y: (122)
> +set size to (17) %
> ```

> [!TASK]
>
> Select **Element Wheel** and add its result position.
>
> ```blocks3
> +when I receive [REVEAL v]
> +go to x: (-60) y: (122)
> +set size to (17) %
> ```

> [!TASK]
>
> Select **Pointers** and hide the large arrows during the reveal.
>
> ```blocks3
> +when I receive [REVEAL v]
> +hide
> ```

> [!TASK]
>
> Select the **Stage**. Add these blocks at the very bottom of its `START` script, after the last element-trait block. They change the backdrop, show the text, and trigger the sprites’ `REVEAL` scripts, including the Animal script you made earlier.
>
> ```blocks3
> add (item ((Element Index) + (1)) of [Element Trait Line 2 v]) to [Your Traits v]
> +switch backdrop to (Result v)
> +show variable [Your Sign v]
> +show list [Your Traits v]
> +broadcast [REVEAL v] and wait
> ```

> [!TASK]
>
> Untick any calculation variables that are still showing. Run the project and enter `2024`.
>
> After the reveal, drag the **Your Sign** display into the top of the panel on the right. Double-click it to show just its value in a large display. Position **Your Traits** below it and resize the list from its bottom-right corner so you can see all seven rows.
>
> You created **Your Sign** yourself, so its display needs positioning once; Scratch will remember its position when you save.

> [!TASK]
>
> **Test your project.** Enter `2024` and check that the result screen shows `2024 • Wood Dragon`, the matching animal, two small wheels, and seven readable trait rows.
