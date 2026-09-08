# Authoring and QA notes

## Scope and source

This is an in-place Scratch adaptation of the read-only ProjectShaper instructions, authorised by the user. The local `dino-jump` project is the authority for both formatting and manageable tasks, as clarified by the user. The audience is 11–14-year-olds with some experience dragging Scratch blocks; the lessons explain broadcasts, variables, list indexes, remainder, and rounding as they appear.

The source of truth is `code/lunar-horoscope-complete/lunar-horoscope-complete.sb3`, SHA-256 `68fac17f7e74bcf72e315c4aff6a779ff3e8da341ae7461dd6c5327c7ae95fff`. The older `scripts/build_lunar_horoscope_sb3.py` does not reproduce all edits in that archive and is not used to generate this lesson. The solution download has been aligned with the supplied complete archive.

The additional `lunar-horoscrope-starter.sb3` supplied during authoring contained eight variables and no scripts. It is preserved unchanged under `render_targets/source_inputs/`, outside the runnable starter folder. The canonical learner starter is `code/lunar-horoscope-starter/lunar-horoscope-starter.sb3`.

## Starter and variable progression

The starter has all 10 original lists, all 60 Animal costumes, the two wheels, pointers, button, and two backdrops. Asset bytes, list contents, and costume order match the complete target. Every target has an empty blocks mapping and an empty variables mapping; there are no variable monitors or dangling variable references.

| Lesson | Variables created on the Stage |
| --- | --- |
| 5 | Birth Year |
| 7 | Cycle |
| 8 | Animal Index, Animal Name |
| 9 | Element Index, Element Name |
| 10 | Costume Number |
| 11 | Your Sign |

Lessons 2–4 build the scene-reset scripts. Lessons 5–11 build input, calculations, and lookups. Lessons 12–14 add wheel animation. Lessons 15–16 assemble the traits. Lessons 17–19 arrange the result, animate the reveal, and enable retry. Lesson 20 tests and saves; lesson 21 exports Your Traits to a text file; lesson 22 is an optional challenge.

## Format and opening flow

`step_1.md` is a plain `## What you will make` introduction with a short outcome, descriptive interaction summary, and separate `NOPRINT` and `PRINTONLY` previews. It contains no learner tasks, setup, tests, code, or starter link.

`step_2.md` contains the starter-opening task, artwork/list orientation, and the first reset scripts. Its learner entry point is the [user-supplied Scratch starter](https://scratch.mit.edu/projects/1379109668), followed by See inside to open the editor. There is no SB3 download/load workflow in that step. The local SB3 remains the source artifact for the hosted starter.

The completed-project URL has not yet been supplied. Step 1 currently uses the observed finished-project screenshot, with a hidden authoring comment marking the URL insertion point. Do not substitute the starter or an unrelated project ID. The starter URL is recorded from the user's message; the hosted project's contents have not been independently checked.

All coding lessons follow Dino Jump: a plain `##` title, short goal, quoted `> [!TASK]` callouts with `blocks3` diagrams and `+` additions, optional `TIP` callouts, and a final test task. There are no HTML task headings, numbered `### Step` subsections, or `c-project-code` wrappers. The challenge ends with a `SAVE` marker. Metadata begins with `What you will make`, with no separate landing-page flag or file.

Scratch configs retain `type: 'scratch'` and `build: true`. Text-file line numbers and fictitious filenames are omitted.

## Validation

From the repository root:

```sh
python3 scripts/build_lesson_assets.py
python3 scripts/validate_scratch_lesson.py
```

To package a particular checkpoint for Scratch, add `--checkpoint 19` (or a lesson number from 1 to 22) to the build command. JSON checkpoints live under `render_targets/` and share the original archive’s assets. They represent the scripts at each lesson, with variable display positioning left to the learner as described.

The validator checks starter ZIP integrity, unchanged assets and lists, zero starter scripts and variables, reference integrity in all 22 checkpoints, variable creation order, exact final block-graph agreement with the complete target, metadata, local links, config alignment, and screenshot claims. It evaluates the source calculation graph for every accepted year from 1 to 9999, including costume/name agreement, seven result rows, the example table, and 60-year repetition. It also checks invalid examples at each relevant checkpoint. This is data-flow validation, not a full Scratch VM or animation test.

`render_targets/validation_report.json` records the current results. The unmodified ProjectShaper validator report in `render_targets/projectshaper_validation.log` is historical: it predates the user’s clarification that Dino Jump is the formatting authority. The updated Scratch-aware validator checks the current Dino Jump layout and is the applicable check for this project; do not run ProjectShaper’s old heading-based metadata sync over these pages.

## Visual QA and remaining limitations

The supplied complete project was run in Scratch 3.32.1 with `2024`; the observed result was Wood Dragon with seven trait rows. Its screenshot is used in lesson 19, whose final scripts match the target. Lesson 21 also includes an actual screenshot of the populated Your Traits list with its context menu open. `images/render_status.json` records every lesson honestly. Screenshots for other lessons were not produced: the generic renderer has no Scratch checkpoint targets, and native file-loading attempts encountered Computer Use errors. Missing screenshots are omitted from the lessons.

Lesson 21 adds list export without changing any scripts or variables. Scratch’s [list export implementation](https://github.com/scratchfoundation/scratch-gui/blob/develop/src/containers/monitor.jsx) saves the list name plus `.txt`, with one item per line. The lesson asks learners to preserve the year in the filename and compare all seven rows with the Stage list.

The first context-menu screenshot is now captured in `images/step_21_output.png`, with a source copy under `render_targets/`. Selecting export opened a native save dialog showing `Your Traits.txt`. An additional screenshot with export highlighted or the save operation completed remains outstanding: subsequent controls failed with stale element IDs and `noWindowsAvailable`, and no actual exported text file was obtained. A hidden note marks that remaining capture without a broken image link. A blank, unshared Scratch QA draft was automatically created in Chrome at `https://scratch.mit.edu/projects/1379068179/editor`; it is not a starter or completed-project publication URL.

The completed-project URL and a project-specific hero image were not supplied. The supplied generic banner is retained. The lesson site has not been published, and the repository’s publication pipeline was not available for a rendered `blocks3` review. Literal square brackets in the year prompt are escaped for Scratchblocks.

All scientific/personality claims are avoided: the text describes the supplied traditional associations as an exploration for fun. The code works from a supplied year, does not calculate Lunar New Year dates, and does not infer a sign from a full date of birth.
