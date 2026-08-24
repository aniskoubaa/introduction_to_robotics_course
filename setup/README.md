# Setup — do this before Week 2

Every practice hour and every assignment assumes a working ROS 2 installation. Budget
**60–90 minutes**. Do not arrive in Week 2 without it.

> **If you get stuck, stop after 30 minutes and ask.** Post the output of
> `check_ros2_setup.py` on the LMS forum. Every failure this script reports has been seen
> before, and none of them is a reason to fall behind.

## Pinned distribution

> **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04 LTS**.
> Gazebo **Harmonic**. Python **3.12**.

⚠️ This is the **only** place in the course where the distribution is named. Every other
document refers here; the lecture decks reach it through the `\rosver` macro, and
`check_ros2_setup.py` holds it in four constants at the top of the file. When the course
upgrades, change those two places and nothing else.

## Pick a route

| Route | For | Effort | Recommended |
|---|---|---|---|
| **A — Native Ubuntu 24.04** | Anyone with a spare machine or a dual boot | Medium | ✅ Best performance, fewest surprises |
| **B — WSL2 on Windows 11** | Most students | Low | ✅ Works, including GUI apps (RViz2, Gazebo) via WSLg |
| **C — Docker** | macOS, especially Apple Silicon | Medium | Acceptable; Gazebo is slower |
| **D — University lab machines** | Fallback | None | Pre-imaged; no personal state persists |

Apple Silicon users: route C. Gazebo runs but expect reduced frame rates — this affects
comfort, not correctness, and every assignment is sized to run on it.

---

## Route A — native Ubuntu 24.04

```bash
# 1. Locale (ROS 2 needs a UTF-8 locale; a fresh minimal install may not have one)
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 2. Add the ROS 2 apt repository
sudo apt install -y software-properties-common curl
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
     -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 3. Install. `desktop` — NOT `ros-base`. See the note below.
sudo apt update && sudo apt upgrade -y
sudo apt install -y ros-jazzy-desktop
sudo apt install -y python3-colcon-common-extensions
sudo apt install -y ros-jazzy-turtlesim ros-jazzy-ros-gz
```

> **Install `desktop`, not `ros-base`.** `ros-base` omits RViz2, turtlesim and several
> message packages. It looks like it worked, and then Week 2's practice session has nothing
> to run. The extra download is worth it.

Then **[Finish — every route](#finish--every-route)**.

---

## Route B — WSL2 on Windows 11

In **PowerShell as Administrator**:

```powershell
wsl --install -d Ubuntu-24.04
```

Reboot when told to. Windows will open an Ubuntu window and ask for a username and password —
this is your Linux account, unrelated to your Windows one. Then, **inside the Ubuntu window**,
follow **Route A** from step 1.

### What is different on WSL2

| | |
|---|---|
| **GUI apps** | Work without any extra setup. WSLg forwards RViz2, Gazebo and turtlesim to Windows automatically. |
| **If no window ever appears** | In PowerShell: `wsl --shutdown`, then reopen Ubuntu. This fixes it nine times out of ten. |
| **Your files** | Keep your workspace in the Linux home directory (`~/ee414_ws`), **not** under `/mnt/c/`. Building on `/mnt/c` is several times slower and occasionally corrupts `colcon` output. |
| **Editing from Windows** | VS Code with the *WSL* extension opens `~/ee414_ws` natively. This is the setup most students end up with. |

---

## Route C — Docker (macOS, including Apple Silicon)

Install Docker Desktop, then:

```bash
docker pull osrf/ros:jazzy-desktop

docker run -it --name ee414 \
  -v "$HOME/ee414_ws:/root/ee414_ws" \
  osrf/ros:jazzy-desktop bash
```

The `-v` flag maps a folder on your Mac into the container, so your code survives the
container being deleted. **Write your code on the Mac; build and run it inside.**

Inside the container:

```bash
apt update && apt install -y ros-jazzy-turtlesim python3-colcon-common-extensions
```

Re-enter the container later with `docker start -i ee414`.

### Graphics

The base image has no display, so turtlesim, RViz2 and Gazebo will not open. Two options:

1. **XQuartz** — install it, enable *Allow connections from network clients* in its settings,
   run `xhost + 127.0.0.1`, and add `-e DISPLAY=host.docker.internal:0` to `docker run`.
2. **A VNC image** — search for a `ros:jazzy` image with a built-in desktop and connect a VNC
   client to it. Slower, but nothing to configure on the Mac.

> Weeks 2 and 3 are entirely command-line and need neither. Sort graphics out before Week 4.

---

## Route D — university lab machines

Pre-imaged with the pinned stack. Nothing to install.

**Nothing you save persists between sessions.** Push your workspace to your own Git repository
at the end of every session, or you will lose it. This is the habit Week 2B asks you to build
anyway, so route D students simply have no choice about it.

---

## Finish — every route

### 1. Source ROS 2 in every terminal

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

Sourcing edits the environment of **one shell**. A new terminal is a new shell and knows
nothing. Putting it in `~/.bashrc` is what makes every future terminal work.

### 2. Set your assigned `ROS_DOMAIN_ID`

You were given a number in Week 1. Use **that** number.

```bash
echo "export ROS_DOMAIN_ID=<your number>" >> ~/.bashrc
source ~/.bashrc
```

**This is not optional in a shared lab.** Discovery reaches every machine on the network
segment. Without distinct domain IDs, thirty students share one graph: your nodes see theirs,
theirs see yours, and nobody can work out which robot they are driving. It costs ten minutes to
prevent and half a session to diagnose.

### 3. Run the check

```bash
cd <this repo>/setup
python3 check_ros2_setup.py
```

Every row must say `PASS`. `WARN` on Gazebo or the display is acceptable for Weeks 2 and 3.
Work top to bottom — **a failure high in the list usually causes the ones below it**, so fix
the first one and run it again before reading further.

### 4. Prove it end to end

Two terminals:

```bash
ros2 run demo_nodes_cpp talker      # terminal 1
ros2 run demo_nodes_py listener     # terminal 2
```

The listener should print the talker's messages. Two programs, written in different languages,
never compiled together, finding each other with no configuration — that is the entire subject
of Week 2, working on your machine.

**Screenshot the check output and bring it to the session.**

---

## When it goes wrong

Ordered by how often it actually happens.

| Symptom | Cause | Fix |
|---|---|---|
| `ros2: command not found` | Fresh shell, not sourced | `source /opt/ros/jazzy/setup.bash`, then put it in `~/.bashrc` |
| `No module named 'rclpy'` | Not sourced, **or** the wrong Python is first on `PATH` | Check the Python row of the checker. A conda or pyenv interpreter is the usual culprit — `conda deactivate`, new terminal |
| Checker says Python 3.11 or 3.13 | conda / pyenv shadowing the system interpreter | `conda deactivate`; if it persists, remove the conda line from `~/.bashrc` for this course |
| `Package 'turtlesim' not found` | Installed `ros-base` instead of `desktop` | `sudo apt install ros-jazzy-turtlesim` |
| Your node sees another student's topics | Everyone on `ROS_DOMAIN_ID` 0 | Set your assigned number, in **every** terminal |
| Nodes run, no data arrives | Different domain IDs, different topic names, or incompatible QoS | `ros2 topic info <topic> --verbose` — Week 2A teaches this |
| No window opens (WSL2) | WSLg not running | `wsl --shutdown` in PowerShell, reopen Ubuntu |
| Build is extremely slow (WSL2) | Workspace on `/mnt/c/` | Move it to `~/ee414_ws` |
| `colcon: command not found` | Separate package from ROS 2 itself | `sudo apt install python3-colcon-common-extensions` |
| Gazebo opens black or crashes | No GPU acceleration in a VM or container | Expected. Reduced frame rate, not a correctness problem |

---

## To be authored

| Item | Status |
|---|---|
| Route-by-route steps, with the common failures | ✅ |
| `check_ros2_setup.py` | ✅ 11 checks, every failure carries a fix, exits non-zero |
| Screenshots of a successful run on each route | ❌ — needs a machine per route |
| Recorded 15-minute walkthrough on the LMS | ❌ |
| `ROS_DOMAIN_ID` assignment list | ❌ — **instructor task, before Week 2** |

> ⚠️ **The route instructions have not been executed end to end on a clean machine.** They are
> assembled from the official ROS 2 Jazzy installation documentation and the failures this
> course expects. Standing rule 2 says every command in the material has been *run*, and these
> have not been — run them once on a clean Ubuntu 24.04 and once on a clean WSL2 before this
> page is treated as verified.
