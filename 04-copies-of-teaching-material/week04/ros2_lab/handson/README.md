# Week 4 hands-on — the two files the students write

Reference copies of the code in `EE414_W04_hands_on_lab.html`. The lab asks the
students to type them; these are here so the instructor can paste a working
version when someone falls behind, and so
`../../shared/screenshots/verify_w04_handson.sh` can install and run them
without the HTML being the source of truth.

| File | Goes to | Lines |
|---|---|---|
| `my_turtle_circle/circle.py` | `~/ros2_course_ws/src/my_turtle_circle/my_turtle_circle/circle.py` | 30 |
| `ros2_motion_cpp/circle.cpp` | `~/ros2_course_ws/src/ros2_course_packages/src/ros2_motion_cpp/src/circle.cpp` | 33 |
| `ros2_motion_cpp/CMakeLists.fragment.txt` | pasted into that package's `CMakeLists.txt` | 7 |

`circle.py` also needs one line added to its `setup.py`:

```python
'circle = my_turtle_circle.circle:main',
```

Both nodes publish `linear.x = 2.0`, `angular.z = 1.0`, so both trace a circle
of radius `v / ω = 2.0` turtlesim units. Measured from `/turtle1/pose` over a
full revolution: **2.000 by 2.000**.
