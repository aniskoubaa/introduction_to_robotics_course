# shared — style sources used by every week

| File | Purpose | Status |
|---|---|---|
| `ee414-beamer-preamble.tex` | Lecture deck palette, terminal-style code boxes, `\fullslide`, `\rosver` | ❌ |
| `ee414-exercise-style.tex` | Exercise/solution preamble with the `\ifsolutions` switch | ❌ |
| `ee414-infographic-style.prompt.txt` | Fixed prompt for generated figures, so illustrations across 15 weeks look like one course | ❌ |
| `alfaisal_logo.png` | Title-slide logo | ❌ |

## The one macro that matters

`\rosver` expands to the pinned ROS 2 distribution. **No deck, exercise or lab sheet writes
the distribution name literally.** A distribution upgrade is then one edit here plus one in
`setup/README.md`, instead of a search across 15 weeks of LaTeX that will miss three of them.

## Code box rule

`pycode`, `shell` and their small variants (`pycodes`, `shells`) all render as a macOS
terminal window — rounded dark panel, grey bar, three traffic lights. The keys are re-applied
*after* the caller's options, so there is no way to switch the bar off. Do not add an
exception: a deck where some code has the bar and some does not reads as an inconsistency
rather than as a distinction.

Mathematics, pseudocode and message-definition (`.msg`) listings use the light `spec` box —
they are not runnable, and the contrast is the point.
