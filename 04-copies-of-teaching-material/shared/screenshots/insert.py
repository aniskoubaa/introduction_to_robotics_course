#!/usr/bin/env python3
"""Drop each code snapshot into the cue it belongs to.

Anchored on the command text, so a snapshot can never end up under the wrong
demonstration: find the command, then insert after the </ol> that closes that
cue's list of steps.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snippets import render, SNIPS

# snippet id -> the command whose cue it belongs under
PLACE = [
  ("quat",        "ros2 run ee414_w04_demo quaternion_demo --part 1"),
  ("wrap",        "ros2 run ee414_course angle_wrap"),
  ("twistcompat", "ros2 interface show geometry_msgs/msg/Twist"),
  ("sixfields",   "ros2 run ee414_course nonholonomic"),
  ("fk",          "ros2 run ee414_w04_demo wheels_to_body --table"),
  ("ik",          "ros2 run ee414_w04_demo body_to_wheels 0.2 1.0"),
  ("saturate",    "ros2 run ee414_w04_demo body_to_wheels 0.5 3.0"),
  ("urdf",        "check_urdf $(ros2 pkg prefix --share ee414_w04_demo)/urdf/burger_min.urdf"),
  ("sdf",         "grep -A7 'systems::DiffDrive'"),
  ("odomread",    "ros2 topic echo /odom --once"),
  ("integrators", "ros2 run ee414_w04_demo dead_reckoning --compare"),
  ("closedloop",  "ros2 run ee414_course go_to_goal --x 9.0 --y 9.0"),
]

# Snapshots that belong under a cue with no command of its own: anchor on a
# phrase, insert before the </div> that closes that cue.
AFTER_TEXT = [
  ("openloop", "knows where it is. Why did it not use that?</em></p>\n"),
]


def main(path):
    s = open(path).read()
    if 'details class="code"' in s:
        # Inserting twice would give every cue two copies. Regenerate from a
        # copy of the sheet taken before the snapshots were first added.
        sys.exit(f"{path} already contains code snapshots; nothing done.")
    for key, tail in AFTER_TEXT:
        i = s.find(tail)
        if i == -1:
            print(f"  !! text not found for {key}")
            continue
        j = i + len(tail)
        s = s[:j] + render(key) + s[j:]
        print(f"  placed {key} (by text)")
    for key, cmd in PLACE:
        i = s.find(cmd)
        if i == -1:
            print(f"  !! command not found for {key}: {cmd[:50]}")
            continue
        j = s.find("      </ol>\n", i)
        if j == -1:
            print(f"  !! no </ol> after {key}")
            continue
        j += len("      </ol>\n")
        s = s[:j] + render(key) + s[j:]
        print(f"  placed {key}")
    open(path, "w").write(s)

if __name__ == "__main__":
    main(sys.argv[1])
