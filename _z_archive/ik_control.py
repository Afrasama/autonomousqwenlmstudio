import os
import time
from typing import Dict, List, Optional

import pybullet as p
import pybullet_data


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URDF_PATH = os.path.join(BASE_DIR, "urdf", "mycobot_320.urdf")
HOME_JOINT_TARGET = 0.0
REPOSITION_Z_OFFSET = 0.05


def get_controlled_joint_indices(robot_id: int) -> List[int]:
    joint_indices: List[int] = []
    for joint_index in range(p.getNumJoints(robot_id)):
        joint_info = p.getJointInfo(robot_id, joint_index)
        if joint_info[2] in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
            joint_indices.append(joint_index)
    return joint_indices


def find_end_effector_index(robot_id: int) -> int:
    for joint_index in range(p.getNumJoints(robot_id)):
        if p.getJointInfo(robot_id, joint_index)[12].decode() == "link6":
            return joint_index
    raise ValueError("End effector link6 not found")


def validate_joint_limits(robot_id: int, joint_targets: Dict[int, float]) -> None:
    for joint_index, target in joint_targets.items():
        joint_info = p.getJointInfo(robot_id, joint_index)
        lower_limit = float(joint_info[8])
        upper_limit = float(joint_info[9])

        # PyBullet can report 0, -1 for continuous joints; skip those.
        if upper_limit <= lower_limit:
            continue

        if target < lower_limit or target > upper_limit:
            raise ValueError(
                f"Joint {joint_index} target {target:.4f} exceeds limits "
                f"[{lower_limit:.4f}, {upper_limit:.4f}]"
            )


def command_joint_positions(
    robot_id: int,
    joint_targets: Dict[int, float],
    steps: int = 120,
    force: float = 250.0,
) -> None:
    validate_joint_limits(robot_id, joint_targets)
    for _ in range(steps):
        for joint_index, target in joint_targets.items():
            p.setJointMotorControl2(
                robot_id,
                joint_index,
                p.POSITION_CONTROL,
                targetPosition=target,
                force=force,
            )
        p.stepSimulation()
        time.sleep(1 / 240)


def command_cartesian_target(
    robot_id: int,
    ee_index: int,
    target_pos: List[float],
    steps: int = 120,
    force: float = 250.0,
) -> None:
    joint_indices = get_controlled_joint_indices(robot_id)
    ik_solution = p.calculateInverseKinematics(
        robot_id,
        ee_index,
        target_pos,
        maxNumIterations=200,
    )
    joint_targets = {
        joint_index: float(ik_solution[joint_index])
        for joint_index in joint_indices
    }
    command_joint_positions(robot_id, joint_targets, steps=steps, force=force)


def open_gripper_if_available(robot_state: dict) -> None:
    gripper_id = robot_state.get("gripper_id")
    if gripper_id is None:
        return
    try:
        p.resetBaseVelocity(gripper_id, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    except Exception:
        pass


def execute_recovery(strategy: str, robot_state: dict) -> None:
    """
    Execute a discrete recovery strategy in the active PyBullet simulation.
    """
    valid_strategies = ["retry_grasp", "reposition_arm", "reset_to_home", "abort"]
    if strategy not in valid_strategies:
        raise ValueError(f"Unsupported recovery strategy: {strategy}")

    robot_id = robot_state.get("robot_id")
    if robot_id is None:
        raise ValueError("robot_state must include robot_id for recovery execution")

    ee_index = robot_state.get("ee_index")
    if ee_index is None:
        ee_index = find_end_effector_index(robot_id)

    current_target = robot_state.get("current_target")
    if current_target is None:
        current_target = list(p.getLinkState(robot_id, ee_index)[0])

    if strategy == "abort":
        open_gripper_if_available(robot_state)
        print("Recovery action: abort requested, gripper opened and motion halted.")
        return

    if strategy == "reset_to_home":
        joint_targets = {
            joint_index: HOME_JOINT_TARGET
            for joint_index in get_controlled_joint_indices(robot_id)
        }
        command_joint_positions(robot_id, joint_targets)
        print("Recovery action: moved robot to home configuration.")
        return

    if strategy == "reposition_arm":
        reposition_target = [
            float(current_target[0]),
            float(current_target[1]),
            float(current_target[2]) + REPOSITION_Z_OFFSET,
        ]
        command_cartesian_target(robot_id, ee_index, reposition_target)
        current_target = reposition_target
        print("Recovery action: lifted end effector before retry.")

    command_cartesian_target(
        robot_id,
        ee_index,
        [float(current_target[0]), float(current_target[1]), float(current_target[2])],
    )
    print("Recovery action: retried grasp from current pose.")


def run_keyboard_control_demo() -> None:
    physics_id = p.connect(p.GUI)
    assert physics_id >= 0, "failed to connect to pybullet"

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")

    robot = p.loadURDF(
        URDF_PATH,
        useFixedBase=True,
        flags=p.URDF_USE_INERTIA_FROM_FILE,
    )

    ee_index = find_end_effector_index(robot)
    print("end-effector index:", ee_index)

    target_pos = [0.25, 0.0, 0.15]
    step = 0.01

    print(
        """
keyboard controls:
W/S : +Y / -Y
A/D : -X / +X
Q/E : +Z / -Z
R   : reset
ESC : quit
"""
    )

    while p.isConnected():
        p.stepSimulation()

        try:
            keys = p.getKeyboardEvents()
        except Exception:
            print("physics server disconnected")
            break

        if ord("a") in keys:
            target_pos[0] -= step
        if ord("d") in keys:
            target_pos[0] += step
        if ord("w") in keys:
            target_pos[1] += step
        if ord("s") in keys:
            target_pos[1] -= step
        if ord("q") in keys:
            target_pos[2] += step
        if ord("e") in keys:
            target_pos[2] -= step

        if ord("r") in keys:
            target_pos = [0.25, 0.0, 0.15]

        if 27 in keys:
            print("exiting...")
            break

        command_cartesian_target(robot, ee_index, target_pos, steps=1, force=800.0)
        time.sleep(1 / 240)

    p.disconnect()


if __name__ == "__main__":
    run_keyboard_control_demo()
