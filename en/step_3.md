## Position the element wheel and pointers

Reset the second wheel and keep the pointers above both wheels.

> [!TASK]
>
> Select **Element Wheel** and add this new script. Choose the existing `START` message from the hat’s dropdown.
>
> ```blocks3
> +when I receive [START v]
> +set rotation style [all around v]
> +go to x: (112) y: (75)
> +set size to (25) %
> +point in direction (90)
> +show
> ```

> [!TASK]
>
> Select **Pointers** and add this script. Its costume contains both arrows, so you only need one sprite.
>
> ```blocks3
> +when I receive [START v]
> +go to x: (0) y: (0)
> +set size to (100) %
> +show
> +go to [front v] layer
> ```
>
> `go to front layer` keeps the arrows visible above the wheels.

> [!TASK]
>
> **Test your project.** Move the element wheel and pointers, then click the green flag to check that the wheel returns to the right and the two arrows return above the wheels.
