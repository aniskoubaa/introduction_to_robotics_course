# Sourced by every terminal in the screencast.
#
# The terminals run a script, not an interactive shell, so there is no PS1 and
# nothing about this machine leaks into the recording: the prompt below is
# printed by hand as ee414@ros2, and $HOME points at a throwaway home, so every
# path shows as ~/ee414_ws.

STAGE_STATE="${STAGE_STATE:-/tmp/ee414_stage.json}"

_c_user=$'\033[38;2;127;191;106m'
_c_path=$'\033[38;2;79;179;217m'
_c_dim=$'\033[38;2;143;160;174m'
_c_cmd=$'\033[1;38;2;233;238;242m'
_c_note=$'\033[38;2;224;164;88m'
_c_off=$'\033[0m'

TYPE_DELAY="${TYPE_DELAY:-0.022}"

prompt() {
  local p="${PWD/#$HOME/\~}"
  printf '%see414@ros2%s:%s%s%s$ ' "$_c_user" "$_c_off" "$_c_path" "$p" "$_c_off"
}

typeit() {
  local s="$1" i n=${#1}
  printf '%s' "$_c_cmd"
  for ((i = 0; i < n; i++)); do
    printf '%s' "${s:i:1}"
    sleep "$TYPE_DELAY"
  done
  printf '%s\n' "$_c_off"
}

# cap <slide> <command> <one-line explanation>
#
# Also appends the caption to $CAP_LOG. The narration is matched back to the
# video by caption text, so this log is what says which line is spoken when.
cap() {
  [ -n "$CAP_LOG" ] && printf '%s\t%s\n' "$(date +%s.%N)" "$3" >> "$CAP_LOG"
  STAGE_PG="$1" STAGE_CMD="$2" STAGE_SAY="$3" \
  /usr/bin/python3 - "$STAGE_STATE" <<'PY'
import json, os, sys
p = sys.argv[1]
try:
    s = json.load(open(p))
except Exception:
    s = {}
s["pg"]  = os.environ.get("STAGE_PG", "")
s["cmd"] = os.environ.get("STAGE_CMD", "")
s["say"] = os.environ.get("STAGE_SAY", "")
json.dump(s, open(p, "w"))
PY
}

# step <slide> <explanation> <command...>
step() {
  local pg="$1" say="$2"; shift 2
  local cmd="$*"
  cap "$pg" "$cmd" "$say"
  sleep 0.9
  prompt
  typeit "$cmd"
  eval "$cmd"
  local rc=$?
  echo
  sleep "${STEP_PAUSE:-1.8}"      # a beat to read the output before the next line
  return $rc
}

# A comment line in the transcript, for things no command shows.
note() { printf '%s# %s%s\n\n' "$_c_note" "$*" "$_c_off"; }

hold() { sleep "${1:-2}"; }

# Wait, then send SIGINT to a command that never returns on its own.
run_for() {
  local secs="$1"; shift
  eval "$*" &
  local p=$!
  sleep "$secs"
  kill -INT "$p" 2>/dev/null
  wait "$p" 2>/dev/null
  printf '%s^C%s\n\n' "$_c_dim" "$_c_off"
}

# Type and run a command that never returns, then interrupt it.
#
# The command runs in the foreground under `timeout -s INT`. It must not be
# backgrounded: a shell script sets SIGINT to ignore on every asynchronous
# command, so a backgrounded `ros2 topic pub` survives the interrupt forever.
step_int() {
  local pg="$1" say="$2" secs="$3"; shift 3
  local cmd="$*"
  cap "$pg" "$cmd" "$say"
  sleep 0.9
  prompt
  typeit "$cmd"
  eval "timeout -s INT $secs $cmd"
  printf '%s^C%s\n\n' "$_c_dim" "$_c_off"
  sleep 1.2
}

# A caption with no command, for a beat of explanation on its own.
beat() {
  cap "$1" "" "$2"
  sleep "${3:-3}"
}

# Recording handshake: the scene script waits for the recorder, and tells the
# orchestrator when it has finished.
wait_go()  { while [ ! -f "$GO_FILE" ];   do sleep 0.2; done; }
say_done() { : > "$DONE_FILE"; }

wait_ready() { [ -n "$READY_FILE" ] || return 0
               while [ ! -f "$READY_FILE" ]; do sleep 0.2; done; sleep 0.6; }

# Start a node and leave it running until a flag file appears. Used in the T4
# terminal, whose node has to stay up while T2 works against it.
#
# The node runs in the foreground for the same reason as step_int, so the flag
# is watched by a helper that signals it through a pid file.
run_until() {
  local pg="$1" say="$2" flag="$3" ready="$4"; shift 4
  local cmd="$*"
  local pf; pf=$(mktemp)
  cap "$pg" "$cmd" "$say"
  sleep 0.9
  prompt
  typeit "$cmd"
  ( while [ ! -f "$flag" ]; do sleep 0.3; done
    for _ in 1 2 3 4 5; do
      local p; p=$(cat "$pf" 2>/dev/null)
      [ -n "$p" ] && kill -INT "$p" 2>/dev/null && break
      sleep 0.3
    done ) &
  local watcher=$!
  if [ -n "$ready" ] && [ "$ready" != "0" ]; then
    ( sleep "$ready"; : > "$READY_FILE" ) &
  fi
  bash -c 'echo $$ > "$0"; eval exec "$1"' "$pf" "$cmd"
  kill "$watcher" 2>/dev/null
  rm -f "$pf"
  printf '%s^C%s\n\n' "$_c_dim" "$_c_off"
}

# Ask the T4 terminal to stop and restart its node, from T2.
restart_node() {
  local pg="$1" say="$2" cmd="$3" secs="${4:-7}"
  cap "$pg" "$cmd" "$say"
  : > "$RESTART_FILE"
  sleep "$secs"
}

# Hand control to the orchestrator (it adds files to the package and opens
# them in the editor), then wait for it to finish.
ask_host() {
  cap "$1" "" "$2"
  : > "$HOST_FILE"
  while [ ! -f "$HOST_DONE" ]; do sleep 0.3; done
}

# Type a command that opens a window and keep it running in this terminal.
step_launch() {
  local pg="$1" say="$2"; shift 2
  local cmd="$*"
  cap "$pg" "$cmd" "$say"
  sleep 0.9
  prompt
  typeit "$cmd"
  eval "$cmd" &
  sleep 8
}
