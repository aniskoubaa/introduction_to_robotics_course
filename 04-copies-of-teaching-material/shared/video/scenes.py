#!/usr/bin/env python3
"""The seventeen scenes of the Week 3 screencast.

Every command comes from EE414_W03_demo_cue_sheet.html, and every caption is
that page's own one-line explanation of the command, so the video and the
runbook say the same thing in the same words.
"""
import json, os, re

V = os.path.dirname(os.path.abspath(__file__))
CARDS = json.load(open(os.path.join(os.path.dirname(V), "cmds.json")))

# (deck-letter, slide) -> [ {cmd, does, where} ]
INDEX = {}
for c in CARDS:
    deck = (c["deck"] or " ")[0]
    INDEX.setdefault((deck, c["pg"]), []).extend(c["steps"])


def look(deck, pg, cmd_prefix, nth=0):
    """Find a step by the start of its command, and return (cmd, caption)."""
    hits = [s for s in INDEX.get((deck, pg), []) if s["cmd"].startswith(cmd_prefix)]
    if not hits:
        raise KeyError(f"{deck}·{pg}: {cmd_prefix!r}")
    s = hits[nth]
    say = re.sub(r"^T\d\s+", "", s["does"]).strip()
    return s["cmd"], say


# A step is (slide-label, kind, seconds, cmd, caption).
#   kind "run" -- run to completion;  "int" -- interrupt after N seconds
def S(deck, pg, prefix, nth=0, kind="run", secs=0, label=None):
    cmd, say = look(deck, pg, prefix, nth)
    return (label or f"{deck} · {pg}", kind, secs, cmd, say)


A, B, N = "D", "D", " "        # both decks come through as "Deck ..."


def deckA(pg, prefix, **kw):
    kw.setdefault("label", f"A · {pg}")
    return S(A, pg, prefix, **kw)


def deckB(pg, prefix, **kw):
    kw.setdefault("label", f"B · {pg}")
    return S(B, pg, prefix, **kw)


def front(prefix, **kw):
    kw.setdefault("label", "Setup")
    return S(N, "", prefix, **kw)


SIM = {"term": "T2 — commands", "sim": "T1 — turtlesim"}
SIM2 = {"node": "T4 — your node", "term": "T2 — commands", "sim": "T1 — turtlesim"}
TWO = {"node": "T4 — your node", "term": "T2 — commands"}
ONE = {"term": "T2 — commands"}
CODE = {"code": "The package files", "term": "T2 — commands"}
CODE2 = {"code": "reset_client.py", "node": "T4 — odom_node", "term": "T2 — commands"}
GZ = {"node": "T3 — the simulator", "term": "T2 — commands", "sim": "TurtleBot 3 in Gazebo"}

REF = os.path.join(V, "ref")
WS = "/tmp/ee414home/ee414_ws"
IFACE = f"{WS}/src/ee414_w03_interfaces"
NODES = f"{WS}/src/ee414_w03_nodes"

CHAPTERS = [
 # ---------------------------------------------------------------- Deck A --
 dict(id="a0", title="Start turtlesim", deck="A", layout="term_sim", labels=SIM,
      needs=[], starts_sim=True,
      blurb="One node that offers a topic, a service, an action and parameters.",
      steps=[front("ros2 run turtlesim", kind="sim", secs=11)]),

 dict(id="a1", title="Interaction Models", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"], reset=True,
      blurb="Four ways to talk to a node, and the one command that lists all of them.",
      steps=[deckA("6", "ros2 topic pub", kind="int", secs=7),
             deckA("7", "ros2 node info", secs=4),
             deckA("7", "ros2 topic list"),
             deckA("7", "ros2 service list -t | grep"),
             deckA("7", "ros2 action list -t"),
             deckA("7", "ros2 param list")]),

 dict(id="a2", title="Interface Definitions", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"],
      blurb="Every message, service and action is a file you can print.",
      steps=[deckA("9", "ros2 interface show geometry_msgs"),
             deckA("9", "ros2 interface proto"),
             deckA("10", "ros2 interface show sensor_msgs"),
             deckA("11", "ros2 interface show std_msgs"),
             deckA("12", "ros2 interface show turtlesim/srv"),
             deckA("12", "ros2 interface show turtlesim/action")]),

 dict(id="a3", title="Topics", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"], reset=True,
      blurb="A stream with no memory: when the sending stops, the movement stops.",
      steps=[deckA("15", "ros2 topic echo /turtle1/pose", kind="int", secs=6),
             deckA("16", "ros2 topic echo /turtle1/pose --once"),
             deckA("16", "ros2 topic info", nth=0),
             deckA("16", "ros2 topic pub", kind="int", secs=8),
             deckA("16", "ros2 topic info", nth=1)]),

 dict(id="a4", title="Services", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"], reset=True,
      blurb="A question asked once and answered once — and the answer is visible.",
      steps=[deckA("18", "ros2 service list -t | grep"),
             deckA("18", "ros2 service type"),
             deckA("18", "ros2 service list -t", nth=1),
             deckA("20", "ros2 service list -t | grep"),
             deckA("20", "ros2 service call /spawn", secs=4),
             deckA("21", "ros2 service call /kill", secs=3)]),

 dict(id="a5", title="Actions", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"],
      blurb="A long job that reports progress while it runs.",
      steps=[deckA("23", "ros2 action list -t"),
             deckA("23", "ros2 action info"),
             deckA("24", "ros2 interface show turtlesim/action"),
             deckA("25", "ros2 action send_goal", nth=0, secs=6),
             deckA("25", "ros2 action send_goal", nth=1, secs=5)]),

 dict(id="a6", title="Parameters", deck="A", layout="term_sim", labels=SIM,
      needs=["sim"],
      blurb="Settings you can read and change while the node keeps running.",
      steps=[deckA("27", "ros2 param list"),
             deckA("28", "ros2 param describe"),
             deckA("29", "ros2 param get"),
             deckA("29", "ros2 param set /turtlesim background_r", secs=3),
             deckA("29", "ros2 param set /turtlesim background_g", secs=3),
             deckA("29", "ros2 param set /turtlesim background_b", secs=4)]),

 dict(id="a7", title="Back to the starting state", deck="A", layout="term_sim",
      labels=SIM, needs=["sim"],
      blurb="Four lines that undo everything the demo changed.",
      steps=[front("ros2 service call /reset", secs=3),
             front("ros2 service call /kill", secs=3),
             front("ros2 param set /turtlesim background_r", secs=2),
             front("ros2 param set /turtlesim background_g", secs=2),
             front("ros2 param set /turtlesim background_b", secs=4)]),

 dict(id="a8", title="The same commands on a real robot", deck="A", layout="gz_scene",
      labels=GZ, needs=["gazebo"], stops_sim=True, node_ready_after=34,
      node_steps=[deckA("32", "export TURTLEBOT3_MODEL"),
                  deckA("32", "ros2 launch turtlebot3_gazebo")],
      blurb="TurtleBot 3 in Gazebo. The robot changed; the commands did not.",
      steps=[deckA("32", "ros2 topic list", secs=4),
             deckA("32", "ros2 topic echo /scan --once --field range_max", secs=3),
             deckA("32", "ros2 topic echo /odom", secs=3),
             deckA("11", "ros2 topic echo /scan --once --field header", secs=3),
             deckA("33", "ros2 topic hz", kind="int", secs=9),
             deckA("33", "ros2 topic info /scan --verbose", secs=4)]),

 # ---------------------------------------------------------------- Deck B --
 dict(id="b1", title="Where packages live", deck="B", layout="term", labels=ONE,
      needs=[],
      blurb="Everything installed is a package. Yours will be too.",
      steps=[deckB("4", "ros2 pkg list"),
             deckB("4", "ros2 pkg prefix")]),

 dict(id="b2", title="Creating the two packages", deck="B", layout="term", labels=ONE,
      needs=[],
      blurb="One package for the interfaces, one for the nodes.",
      steps=[deckB("5", "cd ~/ee414_ws/src"),
             deckB("5", "ros2 pkg create ee414_w03_interfaces", secs=3),
             deckB("5", "ros2 pkg create ee414_w03_nodes", secs=3),
             deckB("7", "ros2 pkg create --build-type", secs=5)]),

 dict(id="b3", title="Writing the interfaces", deck="B", layout="code_term",
      labels=CODE, needs=["code"], code_folder=WS,
      code_files=[
        (f"{IFACE}/msg/WheelState.msg",
         "The message. One field per line: a type, then a name. Header carries the "
         "time stamp and the frame the numbers belong to."),
        (f"{IFACE}/srv/ResetOdom.srv",
         "The service. The three dashes split the request above from the reply below. "
         "A message has no dashes; a service has one line of them."),
        (f"{IFACE}/CMakeLists.txt",
         "rosidl_generate_interfaces turns the two files into Python and C++ code. "
         "Every .msg and .srv file must be listed here by name."),
        (f"{IFACE}/package.xml",
         "The manifest. member_of_group tells colcon this package generates "
         "interfaces, so it is built before anything that uses them."),
        (f"{NODES}/ee414_w03_nodes/wheel_publisher.py",
         "The node that will send the message. It is in the second package, which "
         "depends on the first one."),
      ],
      blurb="Two definition files, four lines of CMake, and the build that turns them into code.",
      steps=[deckB("8", "cd ~/ee414_ws/src/ee414_w03_interfaces"),
             deckB("8", "mkdir msg srv"),
             ("B · 8", "files", 0, "", "The two definition files and the two manifest "
              "files are added to the package. They are shown on the left."),
             deckB("10", "cd ~/ee414_ws"),
             deckB("10", "colcon build", secs=6),
             deckB("10", "source install/setup.bash"),
             deckB("11", "ros2 interface show ee414_w03_interfaces/msg"),
             deckB("11", "ros2 interface show ee414_w03_interfaces/srv")]),

 dict(id="b4", title="Publishing on a topic", deck="B", layout="term2", labels=TWO,
      needs=["node"], node_cmd="ros2 run ee414_w03_nodes wheel_publisher",
      node_label="T4 — wheel_publisher",
      blurb="Your own message type, on a channel of your own.",
      steps=[deckB("14", "ros2 run ee414_w03_nodes wheel_publisher", kind="shown"),
             deckB("15", "ros2 topic echo /wheel_state", secs=4)]),

 dict(id="b5", title="Service server and client", deck="B", layout="term2", labels=TWO,
      needs=["node"], node_cmd="ros2 run ee414_w03_nodes odom_node",
      node_label="T4 — odom_node",
      blurb="A service of your own, called from the command line.",
      steps=[deckB("17", "ros2 run ee414_w03_nodes odom_node", kind="shown"),
             deckB("18", "ros2 service list | grep"),
             deckB("18", "ros2 service call /reset_odom", secs=4)]),

 dict(id="b6", title="The deadlock", deck="B", layout="code_term2", labels=CODE2,
      needs=["code", "node"], code_folder=WS,
      code_files=[(f"{NODES}/ee414_w03_nodes/reset_client.py",
                   "One file, three modes. spin calls the service from inside a "
                   "callback, hang waits for the reply there, and fix uses "
                   "call_async with a done callback.")],
      node_label="T4 — odom_node", node_ready_after=6,
      node_steps=[("B · 17", "run", 0, "ros2 run ee414_w03_nodes odom_node",
                   "The service server from the last chapter, started again. "
                   "The client needs something to call.")],
      blurb="A callback that waits is a callback that never returns.",
      steps=[deckB("20", "ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=spin",
                   kind="int", secs=9),
             ("B · 21", "beat", 4, "", "The next run prints two lines and then freezes. "
              "Nothing crashes, nothing exits — watch the clock."),
             deckB("21", "ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=hang",
                   kind="int", secs=17),
             deckB("24", "ros2 run ee414_w03_nodes reset_client --ros-args -p mode:=fix",
                   kind="int", secs=8)]),

 dict(id="b7", title="Parameters on your own node", deck="B", layout="term2", labels=TWO,
      needs=["node"], node_cmd="ros2 run ee414_w03_nodes driver",
      node_label="T4 — driver",
      blurb="Change a setting while the node runs — and watch it forget on restart.",
      steps=[deckB("26", "ros2 run ee414_w03_nodes driver", kind="shown"),
             deckB("27", "ros2 param list /driver"),
             deckB("27", "ros2 param get", nth=0),
             deckB("27", "ros2 param set", secs=5),
             deckB("27", "ros2 param get", nth=1),
             deckB("28", "ros2 run ee414_w03_nodes driver", kind="restart", secs=6),
             deckB("28", "ros2 param dump", secs=4)]),

 dict(id="b8", title="Action clients", deck="B", layout="term2", labels=TWO,
      needs=["node"], node_cmd="ros2 run action_tutorials_py fibonacci_action_server",
      node_label="T4 — fibonacci_action_server",
      blurb="Feedback while the job runs, or silence until it ends.",
      steps=[deckB("30", "ros2 run action_tutorials_py", kind="shown"),
             deckB("30", "ros2 action send_goal", nth=0, secs=5),
             deckB("30", "ros2 action send_goal", nth=1, secs=5)]),
]

if __name__ == "__main__":
    n = 0
    for ch in CHAPTERS:
        real = [s for s in ch["steps"] if s[1] not in ("beat", "files")]
        n += len(real)
        print(f"{ch['id']:4} {ch['title']:36} {ch['layout']:10} {len(real):2} cmds")
    print(f"\n{len(CHAPTERS)} chapters, {n} commands")
