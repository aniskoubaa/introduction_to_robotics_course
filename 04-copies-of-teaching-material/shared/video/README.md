# Week 3 screencast harness

Standing rule 2: **every command has been run.** This directory is how that is
shown rather than claimed — it records the Week 3 cue sheet end to end against a
live ROS 2 Jazzy system, and can re-record it when the distribution moves.

Nothing here is typed by a person. Each terminal runs a generated script that
prints the prompt itself, types the command out one character at a time, and
then runs it. The output on screen is real.

## What it produces

`out/EE414_W03_demo.mp4` — 1080p, silent, chaptered: an opening card, then for
each of the 17 chapters a title card followed by the recording. `out/chapters.txt`
holds the timestamps.

## Nothing personal is on screen

The recording is a fixed region of a stage window that covers everything else,
so no part of the desktop appears. Inside it:

| Leak | How it is closed |
|---|---|
| Shell prompt | The terminals run a script, not an interactive shell. There is no `PS1`; `prompt()` in `drive.sh` prints `ee414@ros2` by hand. |
| Paths | `HOME` is `/tmp/ee414home`, so every path reads `~/ee414_ws`. It is outside the scratchpad on purpose — `ros2 pkg create` echoes its destination directory, and the scratchpad path carries the real user name. |
| `ros2 pkg create` maintainer | It prints `getpass.getuser()`. `USER`, `LOGNAME` and `USERNAME` are set to `ee414` for everything the recording launches. |
| Package files | `ref/` holds a copy of `code/src/ee414_w03_*` with the maintainer name and address replaced. The originals are untouched. |
| The editor | A throwaway `--user-data-dir`: no account, no sign-in, no telemetry, no git, no chat panel. |
| Notifications | GNOME banners are turned off for the run and turned back on afterwards. |

## Files

| File | Purpose |
|---|---|
| `stagecfg.py` | Geometry. Written in design units of a 1920×1080 frame; the desktop runs at 2×, so the capture region is 3840×2160 and ffmpeg scales back down — which is why the text is sharp. |
| `frame.py` | Draws the stage with PIL and IBM Plex: header, slot frames, caption strip. |
| `stage.py` | Shows that frame in one undecorated window and polls the caption state file. |
| `xwin.py` | Finds, moves and raises windows with python-xlib. There is no `xdotool` on this machine. |
| `rec.py` | Environments, window launching, ffmpeg recording. |
| `drive.sh` | The typing driver every terminal sources: `step`, `step_int`, `run_until`, `cap`. |
| `env.sh` | The ROS 2 environment, with the same three strips as `shared/screenshots/rosenv.sh`. |
| `scenes.py` | The 17 chapters. Commands and captions are read from `cmds.json`, extracted from the cue sheet, so the video and the page cannot drift apart. |
| `run_demo.py` | Records one clip per chapter. |
| `cards.py` / `build.py` | Title cards, and the concatenation into the finished film. |

## Re-recording

```bash
gsettings set org.gnome.desktop.notifications show-banners false
python3 extract_cmds.py <cue sheet>.html cmds.json    # if the page changed
/home/alfaisalx/anaconda3/bin/python3 run_demo.py     # all 17 chapters
/home/alfaisalx/anaconda3/bin/python3 cards.py
/home/alfaisalx/anaconda3/bin/python3 build.py
gsettings set org.gnome.desktop.notifications show-banners true
```

`run_demo.py` takes chapter ids, so a single scene can be redone:
`run_demo.py b6`. Deck A must be run from `a0`, which is the chapter that
starts turtlesim and owns it for the rest of the deck.

The driver runs under the anaconda python because that is the one with
`python-xlib` and Pillow; the *recorded* commands run with the system python,
which is what a student has. That split is deliberate and matches
`shared/screenshots/README.md`.

## Two things that will break a re-record

1. **terminator's DBus single-instance.** A second `terminator` command joins the
   first process and inherits its environment, so `QT_SCALE_FACTOR` never reaches
   turtlesim and it records at 500×500. `dbus = False` in `tcfg/terminator/config`
   prevents it.
2. **Mutter will not place a window under the top bar.** The stage asks for a
   centred region and is put lower; the capture origin is therefore read back
   from where the stage actually landed, never assumed.

## Narration

The spoken track is generated separately and laid onto the finished film, so
the video can be rebuilt silent or narrated from the same clips.

```bash
python3 narration.py                    # the script, from the cue sheet's own words
GEMINI_API_KEY=... python3 tts.py       # one WAV per line, voice Algenib, cached
python3 run_demo.py                     # re-record: pauses now fit the narration
python3 build.py                        # cards sized to their lines; writes timeline.json
python3 voiceover.py                    # mixes the voice onto the film
```

`tts.py` caches by text, so rewording one line costs one request, not 107.

**How the voice is timed.** `cap` in `drive.sh` appends every caption to
`caplog/<chapter>.tsv` with a timestamp, which gives the exact spacing between
captions. `captiming.py` then finds the first frame where the caption strip
changes in the recorded clip, and that anchors the sequence to the video. So no
part of the timing depends on the recorder's clock agreeing with the shell's.
`run_demo.py` reads `voice/durations.json` and pads each command's pause so a
line is never cut off by the next command, and `build.py` sizes each title card
to its own line.
