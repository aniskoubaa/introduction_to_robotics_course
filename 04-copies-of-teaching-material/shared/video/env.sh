# The clean ROS 2 environment every recorded terminal runs in.
# Same three strips as shared/screenshots/rosenv.sh: snap GTK paths, snap
# libraries and anaconda, each of which breaks a GUI or a colcon build here.
unset LOCPATH GTK_PATH GTK_EXE_PREFIX GTK_IM_MODULE_FILE GIO_MODULE_DIR GSETTINGS_SCHEMA_DIR
unset PYTHONPATH PYTHONHOME CONDA_PREFIX CONDA_DEFAULT_ENV
export XDG_DATA_DIRS=/usr/local/share:/usr/share
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v anaconda3 | paste -sd:)
export LD_LIBRARY_PATH=$(echo "$LD_LIBRARY_PATH" | tr ':' '\n' | grep -v '^/snap/' | paste -sd:)
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=77
export TURTLEBOT3_MODEL=burger
export DISPLAY=:1
# Colour-free, deterministic output where ROS offers the choice.
export RCUTILS_COLORIZED_OUTPUT=1
export PYTHONUNBUFFERED=1

# The demo workspace, once it has been built. Before Deck B builds it this is a
# no-op, which is the point: slide B10 has to source it by hand the first time.
if [ -f /tmp/ee414home/ee414_ws/install/setup.bash ]; then
  source /tmp/ee414home/ee414_ws/install/setup.bash
fi
