# ARCOSLAB - Universidad de Costa Rica, 2026
# Author: Rodrigo Chacon Quesada (rodrigo.chacon@ucr.ac.cr)
# Modified by: Jonatan Hidalgo-Morales (jonatan.hidalgo@ucr.ac.cr)
#Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
#(https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)

ARG ZED_SDK=4.1
ARG CUDA=12.1
ARG UBUNTU=22.04

FROM stereolabs/zed:${ZED_SDK}-devel-cuda${CUDA}-ubuntu${UBUNTU}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y --no-install-recommends wget
RUN apt-get install -y --no-install-recommends iputils-ping
RUN apt-get install -y --no-install-recommends git
RUN apt-get install -y --no-install-recommends curl
RUN apt-get install -y --no-install-recommends ca-certificates
RUN apt-get install -y --no-install-recommends software-properties-common
RUN rm -rf /var/lib/apt/lists/* 
RUN apt-get clean

# Install ROS 2 Humble  
RUN apt-get update
RUN add-apt-repository universe -y
RUN apt-get update && apt-get install -y curl gnupg \
    && ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
       | grep -F 'tag_name' | awk -F'"' '{print $4}') \
    && curl -L -o /tmp/ros2-apt-source.deb \
       "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb" \
    && dpkg -i /tmp/ros2-apt-source.deb \
    && rm -f /tmp/ros2-apt-source.deb
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean

RUN apt-get update
RUN apt install -y ros-humble-ros-base
RUN apt install -y ros-humble-rmw-cyclonedds-cpp
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean


# Install Python 3.8 and dependencies

RUN apt-get update && apt-get install -y \
   software-properties-common \
   && add-apt-repository ppa:deadsnakes/ppa -y \
   && apt-get update && apt-get install -y \
   python3.8 \
   python3.8-dev \
   python3.8-venv \
   python3.8-distutils \
   python3-pip \
   build-essential \
   libffi-dev \
   libssl-dev \
   libavcodec-dev \
   libavformat-dev \
   libavdevice-dev \
   libavfilter-dev \
   libavutil-dev \
   libswscale-dev \
   libswresample-dev \
   libpostproc-dev \
   pkg-config \
   libvulkan1 \
   && rm -rf /var/lib/apt/lists/*

#virtual environment:
RUN python3.8 -m venv /opt/myenv
ENV PATH="/opt/myenv/bin:$PATH"

 




#setup OpenTeleVision 
RUN git clone https://github.com/OpenTeleVision/TeleVision.git
RUN pip install --no-cache-dir -r TeleVision/requirements.txt

# NVIDIA ICD/vulkan fix
RUN mkdir -p /root/fix && \
 echo '{ "file_format_version" : "1.0.0", "ICD" : { "library_path" : "libGLX_nvidia.so.0", "api_version" : "1.3" } }' > /root/fix/nvidia_icd.json
# Set NVIDIA environment variables for the runtime:
ENV VK_ICD_FILENAMES=/root/fix/nvidia_icd.json




# Setup environment variables
COPY ./ros_entrypoint.sh /sbin/ros_entrypoint.sh
RUN chmod +x /sbin/ros_entrypoint.sh
ENTRYPOINT ["/sbin/ros_entrypoint.sh"]
CMD ["bash"]

WORKDIR /
