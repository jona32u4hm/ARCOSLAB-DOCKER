import mujoco
import mujoco.viewer
import numpy as np
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from robot_descriptions import panda_mj_description

import mink

model = mujoco.MjModel.from_xml_path(panda_mj_description.MJCF_PATH)
data = mujoco.MjData(model)
configuration = mink.Configuration(model)


task = mink.FrameTask(
    frame_name="attachment_site",
    frame_type="site",
    position_cost=1.0,     # Heavily prioritize moving to the target position
    orientation_cost=0.0   # Ignore orientation for now to keep it easy
)

# Global variables for your live MQTT data
target_x, target_y, target_z = 0.0, 0.0, 0.0

# MQTT Callback function (stays exactly the same)
def on_message(client, userdata, msg):
    global target_x, target_y, target_z
    data_string = msg.payload.decode()
    target_x, target_y, target_z = map(float, data_string.split(","))

# Initialize MQTT Client
mqtt_client = mqtt.Client(CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("vr/hand_position")
mqtt_client.loop_start()

# Main Loop
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        
        # Create a 3D target coordinate from your live VR data
        target_xyz = np.array([target_x, target_y, target_z])
        
        # --- THE BLACK BOX IK ---
        # 1. Update the library with our live VR coordinates
        task.set_target(mink.SE3.from_rotation_and_translation(np.eye(3), target_xyz))
        
        # 2. Tell Mink to calculate the perfect joint velocities to get there.
        # It handles limits and math completely behind the scenes.
        velocity = mink.solve_ik(configuration, [task], dt=0.01)
        
        # 3. Integrate the calculated velocity 
        configuration.integrate_inplace(velocity, dt=0.01)
        
        # 4. Copy the calculated positions from the mink configuration over to MuJoCo's data
        data.qpos[:] = configuration.q
        
        # 5. Tell your position servos to hold this new position
        data.ctrl[:7] = data.qpos[:7]
        
        # 6. Step physics and sync the viewer window
        mujoco.mj_step(model, data)
        viewer.sync()