#!/usr/bin/env python3
"""Put the beginner snapshot above the full one, for every concept that has one.

insert.py placed the thirteen full-code snapshots. This places the seven
beginner versions, each immediately BEFORE the full snapshot of the same idea:
on the projector the room meets the forty-line version first and the production
version second, which is the order the lecture wants.

Re-runnable: it removes any beginner blocks it placed on a previous run before
placing them again, so the handout can be regenerated after the code changes.

    python3 insert_simple.py ../../week04/ros2_lab/EE414_W04_demo_cue_sheet.html
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import snippets

CSS = """
/* The beginner snapshot: same component, green rather than indigo, and it sits
   directly above the full version of the same idea. The colour is the whole
   signal -- green is the one you read out loud, indigo is the one that ships. */
details.code.simple {
  border-left-color: var(--ok); background: var(--ok-wash);
}
details.code.simple > summary { color: var(--ok); }
"""


def main(path):
    s = open(path).read()

    # Undo a previous run, so this is idempotent.
    s = re.sub(r'      <details class="code simple">.*?      </details>\n',
               "", s, flags=re.S)

    placed = []
    for key in snippets.SIMPLE:
        block = snippets.render_simple(key)
        summary = snippets.SNIPS[key][3]
        anchor = f'      <details class="code">\n        <summary>Code · {summary}</summary>'
        if anchor not in s:
            print(f"  ! no anchor for {key!r} -- skipped")
            continue
        s = s.replace(anchor, block + anchor, 1)
        placed.append(key)

    if "details.code.simple" not in s:
        marker = "/* ---------- what to notice ---------- */"
        assert s.count(marker) == 1, "cannot find the CSS insertion point"
        s = s.replace(marker, CSS.strip() + "\n\n" + marker, 1)

    open(path, "w").write(s)
    print(f"placed {len(placed)} beginner snapshots: {', '.join(placed)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1
         else "../../week04/ros2_lab/EE414_W04_demo_cue_sheet.html")
