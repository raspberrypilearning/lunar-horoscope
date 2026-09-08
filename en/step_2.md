## Set up your project

Open your starter project and make the green flag reset the animal wheel.

> [!TASK]
>
> Open the [Lunar horoscope starter project](https://scratch.mit.edu/projects/1379109668){:target="_blank"} in a new tab, then choose **See inside** to open the editor.
>
> All the artwork and lists are included. There are no scripts or variables yet: you will create them as you build.

> [!TASK]
>
> Find the five sprites: **Zodiac Wheel**, **Element Wheel**, **Pointers**, **Animal**, and **Try Another Year**.
>
> Select **Animal**, then **Costumes**. It has 60 costumes: five elements for each of 12 animals. Keep their order and names so your code can choose the right one.

> [!TASK]
>
> Select the **Stage** thumbnail, then **Code → Variables**. Tick **Animal Names** to inspect the list: `Rat` is item 1 and `Pig` is item 12. Untick it afterwards.
>
> A **variable** stores one value; a **list** stores several values in order. You will create variables when you need them.

> [!TASK]
>
> With the **Stage** selected, add a **when green flag clicked** hat from **Events** and a `broadcast` block below it. In the broadcast dropdown, choose **New message** and name it `START`.
>
> ```blocks3
> +when green flag clicked
> +broadcast [START v]
> ```
>
> Add the blocks marked with `+` in each diagram; the other blocks show where they fit. You drag blocks in Scratch rather than type the diagrams.

> [!TIP]
>
> A **broadcast** sends a message to scripts across your project. You will use `START` to reset everything for a new turn.

> [!TASK]
>
> Select **Zodiac Wheel**. Add an **Events** `when I receive START` hat, then these **Motion** and **Looks** blocks.
>
> ```blocks3
> +when I receive [START v]
> +set rotation style [all around v]
> +go to x: (-112) y: (45)
> +set size to (35) %
> +point in direction (90)
> +show
> ```
>
> `all around` lets the wheel rotate. The position and size fit the artwork supplied in your starter. A direction of `90` shows the costume without turning it.

> [!TASK]
>
> **Test your project.** Drag the animal wheel somewhere else on the Stage, click the green flag, and check that it returns to the left with its original size and direction.
