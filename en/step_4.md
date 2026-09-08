## Prepare a new turn

Reset the backdrop and hide the parts that belong on the result screen.

> [!TASK]
>
> Select the **Stage**. Add a second script beside the green flag script, using `when I receive START`. Choose the existing **Spinner** backdrop and **Your Traits** list from the dropdowns.
>
> ```blocks3
> +when I receive [START v]
> +switch backdrop to (Spinner v)
> +hide list [Your Traits v]
> +delete all of [Your Traits v]
> ```
>
> **Your Traits** is the empty list where you will collect the result. The other lists hold the data to look up; leave their contents unchanged.

> [!TASK]
>
> Select **Animal** and add these blocks. Its picture should only appear when there is a result to show.
>
> ```blocks3
> +when I receive [START v]
> +hide
> +clear graphic effects
> +set rotation style [don't rotate v]
> ```

> [!TASK]
>
> Select **Try Another Year** and add this script to hide the button at the beginning of a turn.
>
> ```blocks3
> +when I receive [START v]
> +hide
> ```

> [!TASK]
>
> **Test your project.** Use each sprite’s **Show** control to reveal **Animal** and **Try Another Year**, then click the green flag to check that both hide while the wheels and pointers stay visible.
