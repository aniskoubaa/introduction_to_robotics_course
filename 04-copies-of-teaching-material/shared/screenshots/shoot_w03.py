#!/usr/bin/env python3
"""Week 3 — every screenshot in both decks, captured from a live ROS 2 system.

Run with the anaconda python (it has python-xlib and Pillow); the commands it
photographs run with the system python, which is what a student has.

    source rosenv.sh
    ros2 run turtlesim turtlesim_node &
    ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py &
    /home/alfaisalx/anaconda3/bin/python3 shoot_w03.py

Deck A is turtlesim: one node that exposes a topic, a service, an action and a
parameter, so the whole lecture can be demonstrated against a single process.
Deck B is the week's own two packages, built from scratch.
"""
import sys, os, time, subprocess, shutil, signal

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from capture import term_shot, win_shot, clean_env, raise_window     # noqa: E402

COURSE = os.path.abspath(os.path.join(S, "..", "..", ".."))
DEMO = "/tmp/ee414_ws"          # throwaway, so `pkg create` output is first-run


def sh(cmd, t=25):
    return subprocess.run(["bash", "-c", f"source {S}/rosenv.sh; {cmd}"],
                          capture_output=True, text=True, timeout=t, env=clean_env())


def bg(cmd):
    return subprocess.Popen(["bash", "-c", f"source {S}/rosenv.sh; exec {cmd}"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            env=clean_env(), start_new_session=True)


def kill(*procs):
    for p in procs:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass


# =====================================================================
# DECK A — the turtlesim thread
# =====================================================================
print("== A: turtlesim ==")

# Start from one turtle. A `scout` left over from the /spawn demo below would
# double the service list in every later capture.
sh("ros2 service call /kill turtlesim/srv/Kill \"{name: 'scout'}\"")
sh("ros2 service call /reset std_srvs/srv/Empty '{}'")
sh("timeout 3 ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist "
   "'{linear: {x: 2.0}, angular: {z: 1.8}}'", t=10)
time.sleep(0.5)
win_shot("a01_turtlesim_window", "TurtleSim")

# The slide the lecture turns on: four headings, one command. Sized so all 30
# lines and the prompt fit -- if the prompt scrolls off, this stops working.
term_shot("a02_node_info", "show 'ros2 node info /turtlesim'", cols=1580, rows=830)

term_shot("a03_pose_echo", "show 'ros2 topic echo /turtle1/pose --once'",
          cols=1150, rows=380)
term_shot("a04_service_list", "show 'ros2 service list -t | grep -v parameter'",
          cols=1150, rows=420)

# A service is a question answered at once -- and the answer is visible.
sh("ros2 service call /reset std_srvs/srv/Empty '{}'")
time.sleep(1.0)
win_shot("a05_spawn_before", "TurtleSim")
term_shot("a06_service_call",
          "show 'ros2 service call /spawn turtlesim/srv/Spawn "
          "\"{x: 2.0, y: 8.0, theta: 0.0, name: \\\"scout\\\"}\"'",
          cols=1150, rows=300, settle=6)
time.sleep(1.0)
win_shot("a07_spawn_after", "TurtleSim")
sh("ros2 service call /kill turtlesim/srv/Kill \"{name: 'scout'}\"")

term_shot("a08_iface_spawn", "show 'ros2 interface show turtlesim/srv/Spawn'",
          cols=1150, rows=300)
term_shot("a09_iface_rotate",
          "show 'ros2 interface show turtlesim/action/RotateAbsolute'",
          cols=1150, rows=380)

# The whole action exchange must fit: goal, feedback, result, status. theta is
# small on purpose -- feedback arrives on a timer, so a large rotation prints
# hundreds of lines and the prompt scrolls away.
term_shot("a10_action_feedback",
          "ros2 action send_goal /turtle1/rotate_absolute "
          "turtlesim/action/RotateAbsolute '{theta: 0.0}' >/dev/null 2>&1; clear; "
          "show 'ros2 action send_goal /turtle1/rotate_absolute "
          "turtlesim/action/RotateAbsolute \"{theta: 0.12}\" --feedback'",
          cols=1580, rows=830, settle=16)

# Parameters, with the change visible on screen.
sh("ros2 param set /turtlesim background_b 255")
sh("ros2 param set /turtlesim background_r 69")
sh("ros2 param set /turtlesim background_g 86")
time.sleep(1.0)
win_shot("a11_bg_before", "TurtleSim")
term_shot("a12_param_list", "show 'ros2 param list /turtlesim'", cols=1150, rows=300)
term_shot("a13_param_set",
          "show 'ros2 param get /turtlesim background_r'; "
          "show 'ros2 param set /turtlesim background_r 200'; "
          "show 'ros2 param set /turtlesim background_g 60'; "
          "show 'ros2 param set /turtlesim background_b 60'",
          cols=1150, rows=300, settle=7)
time.sleep(1.5)
win_shot("a14_bg_after", "TurtleSim")

# ---------------------------------------------------------------------
print("== A: TurtleBot 3 grounding ==")

# Point the GUI camera somewhere that shows the arena. Gazebo's camera looks
# down its local +X; this pose is (3, -3, 4.2) aimed back at the origin.
sh("gz service -s /gui/move_to/pose --reqtype gz.msgs.GUICamera "
   "--reptype gz.msgs.Boolean --timeout 3000 "
   "--req 'pose: {position: {x: 3.0, y: -3.0, z: 4.2}, "
   "orientation: {x: -0.3663, y: 0.1517, z: 0.8482, w: 0.3514}}'")
time.sleep(3)
raise_window("Gazebo Sim")          # x11grab photographs whatever is on top
win_shot("a15_tb3_gazebo", "Gazebo Sim")

term_shot("a16_scan_echo",
          "show 'ros2 topic echo /scan --once --field header'; "
          "show 'ros2 topic echo /scan --once --field angle_increment'; "
          "show 'ros2 topic echo /scan --once --field range_min'; "
          "show 'ros2 topic echo /scan --once --field range_max'",
          cols=1150, rows=420, settle=8)
term_shot("a17_iface_laserscan",
          "show 'ros2 interface show sensor_msgs/msg/LaserScan'", cols=1500, rows=790)
term_shot("a18_topic_hz", "show 'timeout 8 ros2 topic hz /scan'",
          cols=1150, rows=300, settle=12)
term_shot("a19_topic_info", "show 'ros2 topic info /scan --verbose'",
          cols=1150, rows=700, settle=6)


# =====================================================================
# DECK B — the week's own packages
# =====================================================================
print("== B: package creation ==")
shutil.rmtree(DEMO, ignore_errors=True)
os.makedirs(f"{DEMO}/src", exist_ok=True)

term_shot("b01_pkg_create",
          f"cd {DEMO}/src && "
          "show 'ros2 pkg create ee414_w03_interfaces --build-type ament_cmake' "
          "| grep -E 'going to|package name|build type|creating' | head -8; echo; "
          "show 'ros2 pkg create ee414_w03_nodes --build-type ament_python "
          "--dependencies rclpy std_msgs' "
          "| grep -E 'going to|package name|build type|dependencies|creating' | head -10",
          cols=1150, rows=560, settle=9)

# The trap: --dependencies is nargs='+', so a package name written after it is
# swallowed as a third dependency and the error names `package_name` -- the one
# thing the student did type. Worth a slide of its own.
term_shot("b01b_pkg_create_wrong",
          f"cd {DEMO}/src && "
          "show 'ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs "
          "ee414_w03_nodes' 2>&1 | tail -4",
          cols=1150, rows=300, settle=7)

print("== B: build and inspect ==")
term_shot("b02_colcon_build",
          f"cd {COURSE}/code && rm -rf build install log >/dev/null 2>&1; "
          "show 'colcon build --symlink-install' 2>&1 | grep -v WARNING",
          cols=1150, rows=340, settle=35)
term_shot("b03_iface_show",
          "show 'ros2 interface show ee414_w03_interfaces/msg/WheelState'; "
          "show 'ros2 interface show ee414_w03_interfaces/srv/ResetOdom'",
          cols=1150, rows=520, settle=6)

print("== B: the nodes ==")
pub = bg("ros2 run ee414_w03_nodes wheel_publisher")
odom = bg("ros2 run ee414_w03_nodes odom_node")
time.sleep(5)

term_shot("b04_topic_echo_custom", "show 'ros2 topic echo /wheel_state --once'",
          cols=1150, rows=460, settle=7)
term_shot("b05_service_call",
          "show 'ros2 service list | grep reset'; "
          "show 'ros2 service call /reset_odom ee414_w03_interfaces/srv/ResetOdom "
          "\"{zero_heading: true}\"'",
          cols=1150, rows=460, settle=8)

# Two ways to wait inside a callback, and they fail differently. Jazzy raises on
# spin_until_future_complete; client.call() genuinely deadlocks in silence.
term_shot("b06_deadlock_spin",
          "show 'ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=spin' "
          "2>&1 | tail -9",
          cols=1150, rows=420, settle=13)
term_shot("b06b_deadlock_hang",
          "show 'ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=hang'",
          cols=1150, rows=300, settle=14)
term_shot("b07_deadlock_fix",
          "show 'ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=fix'",
          cols=1150, rows=380, settle=13)

drv = bg("ros2 run ee414_w03_nodes driver")
time.sleep(4)
term_shot("b08_param_live",
          "show 'ros2 param list /driver'; "
          "show 'ros2 param get /driver max_speed'; "
          "show 'ros2 param set /driver max_speed 0.05'; "
          "show 'ros2 param get /driver max_speed'",
          cols=1150, rows=520, settle=9)

fib = bg("ros2 run action_tutorials_py fibonacci_action_server")
time.sleep(5)
term_shot("b09_action_fib",
          "show 'ros2 action send_goal /fibonacci "
          "action_tutorials_interfaces/action/Fibonacci \"{order: 3}\" --feedback'",
          cols=1580, rows=830, settle=13)

kill(pub, odom, drv, fib)
print("done -- now run: python3 trim_shots.py 'shots/*.png'")
