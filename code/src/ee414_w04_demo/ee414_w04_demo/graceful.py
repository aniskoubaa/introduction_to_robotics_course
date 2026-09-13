#!/usr/bin/env python3
"""Make Ctrl-C do what a demonstration needs it to do.

By default `rclpy.init()` installs its own SIGINT handler, and that handler
shuts the context down immediately. Everything after it then fails:

    rclpy._rclpy_pybind11.RCLError: Failed to publish:
        publisher's context is invalid
    [ros2run]: Process exited with failure 1

Two things are wrong with that in front of a class. The obvious one is
twenty lines of red traceback. The one that matters is that the robot never
receives the stop message -- the node dies mid-drive and the robot keeps
going, because a differential drive holds the last velocity it was given.

So we ask rclpy not to install a handler, and install one that only sets a
flag. The context stays valid, the loops notice the flag and return, and the
usual `stop()` on the way out actually reaches the robot.

Usage is three lines:

    rclpy.init(args=args)                 # -> init(args)  from here
    while not interrupted():              # in any hold loop
        ...
"""

import signal

import rclpy
from rclpy.signals import SignalHandlerOptions

_interrupted = False


def _handler(signum, frame):
    global _interrupted
    _interrupted = True


def init(args=None):
    """rclpy.init, with the signal handler replaced by our flag."""
    global _interrupted
    _interrupted = False
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)


def interrupted():
    """True once Ctrl-C has been pressed. The context is still alive."""
    return _interrupted


def shutdown(node=None):
    """Tear down without caring which way we got here."""
    if node is not None:
        node.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
