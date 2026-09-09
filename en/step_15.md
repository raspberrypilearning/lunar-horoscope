## Collect the animal traits

Build a result list containing the chosen animal’s heading and three lines of traits.

> [!TASK]
>
> Select the **Stage**. Add these blocks below `wait 0.6 seconds` at the bottom of its `START` script. (You can make one, then **duplicate** it to make the others.)
>
> All these lists already exist. Use **Variables** blocks to empty **Your Traits**, then add one item from each animal list. Each lookup uses the same `Animal Index + 1` item number.
>
> ```blocks3
> wait (0.6) seconds
> +delete all of [Your Traits v]
> +add (item ((Animal Index) + (1)) of [Animal Headings v]) to [Your Traits v]
> +add (item ((Animal Index) + (1)) of [Animal Trait Line 1 v]) to [Your Traits v]
> +add (item ((Animal Index) + (1)) of [Animal Trait Line 2 v]) to [Your Traits v]
> +add (item ((Animal Index) + (1)) of [Animal Trait Line 3 v]) to [Your Traits v]
> ```
>
> You can duplicate the first `add` block, then change its source-list dropdown. Check that every destination dropdown still says **Your Traits**.
>
> The source lists line up: item `5` describes Dragon in every animal list. Emptying the result list prevents old traits from building up.

> [!TASK]
>
> **Test your project.** Enter `2024`, wait for the wheels to stop, then tick **Your Traits** to check that it has exactly four rows starting with `DRAGON TRAITS`.
