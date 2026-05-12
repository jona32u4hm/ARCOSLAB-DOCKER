# ARCOS-LAB Docker with ZedSDK and ROS2 for OpenTeleVision
This repo contains the Dockerfile set up for running OpenTeleVision inside a container.
It includes all the dependencies and automatically installs the requirements, so the scripts are "plug and play".

Currently it has not been tested with hardware but the simulation environment is working and connects successfully to Apple Vision Pro.
To allow WebXR on Apple Vision, an https connection is necessary. If using Tailscale to connect the host and the headset, Tailscale can sign a certifcate. 

## To serve https on Tailscale:
1. Enter the **DNS** tab in the Tailscale admin page and make sure *MagicDNS* and *HTTPS Certificates* are both enabled
2. From **Machines** tab select the machine to certify and under **Machine Details** copy the **full domain**. 
3. Run ``` sudo tailscale cert <paste domain here> ```

## Build
To build the container run ``` make .build ```

## To run the simulation:
- First download Isaac Gym Preview 4 and place the folder named *isaacgym* inside this directory.
- Use ```make simulation``` to run the container with the Isaac Gym folder mounted.
- Enter the container with ```make debug``` and run ```cd /workspace/IsaacGym/python & pip install -e .```
- Finally ```cd /workspace/TeleVision/teleop & python teleop_hand.py```
- Connect from AVP on por **8012**.

