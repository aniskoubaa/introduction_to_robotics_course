# Start a command in its own process group, and signal that group later.
#
# Sourced by every harness that has to interrupt something. It exists because
# the obvious way to do this is wrong in a way that reports success.
#
# THE TRAP, in full, because it has now cost two days across two harnesses.
#
#   setsid bash -c '...' &
#   pgid=$!
#   kill -INT -"$pgid"
#
# `setsid(1)` only calls setsid(2) directly when the calling process is not
# already a process group leader. When it *is* one, setsid forks, the parent
# exits immediately, and the child -- the thing you actually wanted to signal
# -- has a pid nobody recorded. `$!` is that parent. It is already dead.
#
# Whether the parent is a group leader depends on job control:
#
#   set +m  (the default in a script)  background jobs stay in the shell's own
#           process group, so `bash -c` is NOT a leader, setsid does not fork,
#           and $! happens to be right.
#   set -m                             every background job is its own group
#           leader, so setsid DOES fork, and $! is useless.
#
# Both harnesses were written under `set +m` and worked. `set -m` was then
# added to both -- correctly, because without it bash hands background jobs
# SIGINT = SIG_IGN and the interrupt cannot be delivered at all -- and that fix
# silently broke the addressing. `kill -INT -$!` then signalled a group that no
# longer existed: no traceback in the log, exit status 0 from `wait` on a
# parent that had exited cleanly, and a confident PASS. The nodes kept running.
# Leaked `ros2 topic pub` processes from one such run were caught minutes later
# by assert_clean_graph.sh, which is the only reason it was noticed.
#
# So the group id is never inferred. The child writes it down.

# spawn_pg <pgid-file> <log-file> <command string>
#   Start the command in a new session, with its group id in <pgid-file>.
spawn_pg() {
  local pgfile="$1" log="$2" cmd="$3"
  : > "$pgfile"
  setsid bash -c "echo \$\$ > '$pgfile'; $cmd" > "$log" 2>&1 &
  local i
  for i in $(seq 1 30); do [ -s "$pgfile" ] && break; sleep 0.1; done
  [ -s "$pgfile" ]
}

# sigint_pg <pgid-file> [grace-seconds]
#   Send SIGINT to the whole group, the way Ctrl-C does in a terminal, then
#   wait up to `grace` seconds for it to go. SIGKILL only if it will not.
#   Returns 0 if SIGINT was enough, 1 if the group had to be killed.
sigint_pg() {
  local pgfile="$1" grace="${2:-10}" pg i
  [ -s "$pgfile" ] || return 1
  pg="$(cat "$pgfile")"
  kill -INT -"$pg" 2>/dev/null
  for i in $(seq 1 $(( grace * 4 ))); do
    kill -0 -"$pg" 2>/dev/null || return 0
    sleep 0.25
  done
  kill -9 -"$pg" 2>/dev/null
  return 1
}

# kill_pg <pgid-file>
kill_pg() {
  [ -s "$1" ] || return 0
  local pg; pg="$(cat "$1")"
  kill -INT -"$pg" 2>/dev/null; sleep 2; kill -9 -"$pg" 2>/dev/null
  : > "$1"
}
