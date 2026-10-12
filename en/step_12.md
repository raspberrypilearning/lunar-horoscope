## Fade the animal into view

Make the animal gradually appear when the result is revealed.

> [!TASK]
>
> Select **Animal** and extend its `REVEAL` script as shown. Add `set ghost effect to 100` before `show`, then add the repeat loop and `clear graphic effects` below `go to front layer`.
>
> Use the **Looks** effect dropdowns to choose `ghost`.
>
> ```blocks3
> when I receive [REVEAL v]
> switch costume to (Costume Number)
> go to x: (-118) y: (-42)
> set size to (68) %
> +set [ghost v] effect to (100)
> show
> go to [front v] layer
> +repeat (10)
> +  change [ghost v] effect by (-10)
> +  wait (0.02) seconds
> +end
> +clear graphic effects
> ```
>
> A ghost effect of `100` makes a sprite transparent. Each loop reduces it by `10` until the animal is fully visible. The final block clears any remaining effect.

> [!TASK]
>
> **Test your project.** Run the project with `2024` and watch the animal fade into view after the wheels finish, then restart to check that the fade works again.
