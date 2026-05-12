# ARCOS-LAB Docker with ZedSDK and ROS2 for OpenTeleVision
This repo contains the Dockerfile set up for running OpenTeleVision inside a container.
It includes all the dependencies and automatically installs the requirements, so the scripts are "plug and play".

Currently it has not been tested with hardware but the simulation environment is working and connects successfully to Apple Vision Pro.

## To run the simulation:
- First download Isaac Gym and place the folder named *isaacgym* inside this directory.
- Use *make simulation* to run the container with the Isaac Gym folder mounted.
- Enter the container with *make debug* and run *cd /workspace/IsaacGym/python & pip install -e .*
- Finally *cd /workspace/TeleVision/teleop & python teleop_hand.py*
- Connect from AVP on por **8012**.

