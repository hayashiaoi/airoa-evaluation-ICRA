# airoa-evaluation-ICRA

Participant evaluation runtime for ICRA 2026 VLA Workshop Competition.

## 1. Editable Scope

Main implementation targets:

- `server/`
- `src/`

## 2. Host Requirements

- Linux
- Docker Engine
- Docker Compose v2
- NVIDIA driver
- NVIDIA Container Toolkit

```bash
docker --version
docker compose version
nvidia-smi
```

Verified environment (2026-02-20):

- OS: Ubuntu 24.04.3 LTS
- GPU: NVIDIA GeForce RTX 5070 Ti
- NVIDIA driver: 580.126.09
- Docker: 29.0.1
- Docker Compose: v2.40.3

## 3. Implementation Workflow

1. Create a feature branch from the prepared base branch.
2. Add your model repository under `src/`.
3. Update `server/serve_hsr_policy_ws.py` (currently the OpenPI version) and server-side dependencies for your model runtime.
4. Add an adapter in `src/` or `server/`.

Adapter definition:
An adapter is a thin conversion layer that maps between the HSR client contract and your model's native
input/output format. For required fields and shapes, just follow the `WebSocket I/O Contract` section below.

5. Run the test flow and confirm `Action executed.` appears in logs.
6. Submit your branch.

## 4. Required Environment Variables

```bash
export POLICY_CHECKPOINT_PATH=/abs/path/to/checkpoint_dir
```

## 5. Sample Openpi Variables
```bash
export POLICY_CHECKPOINT_PATH=/abs/path/to/pi05_hsr_task6891011_level12_v2.5_train_adaptive/pi05_hsr_task6891011_level12_v2.5_train_adaptive_gpu8/200000/
export POLICY_CONFIG_NAME=pi05_hsr_task6891011_level12_v2.5_train_adaptive
```

## 6. Test Flow

Start containers:

```bash
./RUN-DOCKER-CONTAINER.sh up
```

Enter client shell:

```bash
./RUN-DOCKER-CONTAINER.sh shell
```

Run launch inside the container:

```bash
roslaunch hsr_policy_client hsr_policy_client.launch
```

By default, `test_mode` is `true`. In this mode, the client uses synthetic random observations
(`head_rgb`, `hand_rgb`, and `state`) in an infinite loop and prints language/action logs.

## 7. Logs and Stop

```bash
./RUN-DOCKER-CONTAINER.sh logs policy_server
./RUN-DOCKER-CONTAINER.sh down
```

## 8. WebSocket I/O Contract

Inference request fields:

- `head_rgb`: image array `(H, W, 3)` (current HSR dataset profile: `(480, 640, 3)`)
- `hand_rgb`: image array `(H, W, 3)` (current HSR dataset profile: `(480, 640, 3)`)
- `state`: `(8,)`
- `prompt`: `str`

Inference response field:

- `actions` with shape `(T, 11)`, `T >= 1`

Action order:

- `[arm_lift_joint, arm_flex_joint, arm_roll_joint, wrist_flex_joint, wrist_roll_joint, gripper, head_pan_joint, head_tilt_joint, base_x, base_y, base_t]`

Value requirement:

- finite numeric values only

## 9. TeamKIT Deployment Procedure

### 9.1 environment variables
```bash
export TEST_MODE=false
export HSR_IP=<YOUR_HSR_IP>
export ROS_MASTER_URI=http://<YOUR_HOST_IP>:11311
export ROS_IP=<YOUR_HOST_IP>
export POLICY_CHECKPOINT_PATH=/abs/path/to/checkpoint_dir
export POLICY_SERVER_HOST=127.0.0.1
export POLICY_SERVER_PORT=8000
export POLICY_SERVER_API_KEY=
export POLICY_CACHE_DIR=$PWD/.docker_cache/policy_cache
export HF_CACHE_DIR=$PWD/.docker_cache/hf
export ROSBAG_DIR=$PWD/datasets/rosbags
```

### 9.2 Optional policy-specific variables
```bash
export POLICY_CONFIG_NAME=pi05_KIT
export POLICY_DEFAULT_PROMPT="Pick up the coffee bottle on the right"
export POLICY_RECORD_DIR=record_dir
export POLICY_PYTORCH_DEVICE=cuda
```

### 9.3 Start and verify containers
```bash
./RUN-DOCKER-CONTAINER.sh up
./RUN-DOCKER-CONTAINER.sh logs policy_server
./RUN-DOCKER-CONTAINER.sh logs hsr_client
```

### 9.4 Run deploy launch
Enter client shell:
```bash
./RUN-DOCKER-CONTAINER.sh shell
```
Launch inside client container:
```bash
roslaunch hsr_policy_client hsr_policy_client.launch test_mode:=false
```
