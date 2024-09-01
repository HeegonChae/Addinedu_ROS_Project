# Use the official NVIDIA CUDA base image for CUDA 12.1 support
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set timezone and locale
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y locales && \
    locale-gen ko_KR ko_KR.UTF-8 && \
    update-locale LC_ALL=ko_KR.UTF-8 LANG=ko_KR.UTF-8 && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*
ENV LANG=ko_KR.UTF-8

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl gnupg2 lsb-release && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    apt-get update && \
    apt-get install -y ros-humble-desktop python3-pip python3-opencv python3-colcon-common-extensions python3-rosdep ros-humble-cv-bridge git xterm wget pciutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install ultralytics (YOLOv5)
RUN pip3 install --upgrade pip && \
    pip3 install ultralytics

# Initialize rosdep if not already initialized
RUN rosdep init && rosdep update

# Setup ROS 2 workspace
WORKDIR /home/ros2_ws/src
COPY ai_server /home/ros2_ws/src/ai_server

# Install ROS 2 dependencies and build the workspace
RUN . /opt/ros/humble/setup.sh && \
    cd /home/ros2_ws && \
    rosdep install --from-paths src --ignore-src -r -y --skip-keys="ultralytics" && \
    colcon build

# Source the ROS 2 setup script
RUN echo "source /opt/ros/humble/setup.sh" >> ~/.bashrc
RUN echo "source /home/ros2_ws/install/setup.bash" >> ~/.bashrc

# Set the entrypoint
# ENTRYPOINT ["ros2", "launch", "ai_server", "detection_launch.py"]

CMD ["bash"]
