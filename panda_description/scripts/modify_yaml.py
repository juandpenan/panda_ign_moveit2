#!/usr/bin/env python3
"""Utility to rename Panda joint names to a new prefix inside MoveIt controller YAML files.

It updates only entries whose original prefix matches ORIGINAL_PREFIX (default 'panda').
"""

import os
import yaml
import argparse
from ament_index_python.packages import get_package_share_directory


def rename_string(obj, new_name: str, yaml_name: str):
    if 'controllers' in yaml_name and 'moveit' not in yaml_name:
        for idx, joint in enumerate(obj['/**/joint_trajectory_controller']['ros__parameters']['joints']):
            joint_name_parts = joint.split('_joint')
            if len(joint_name_parts) == 2:
                replacement = f'{new_name}_joint{joint_name_parts[1]}'
                obj['/**/joint_trajectory_controller']['ros__parameters']['joints'][idx] = replacement

        for idx, joint in enumerate(obj['/**/gripper_trajectory_controller']['ros__parameters']['joints']):
            joint_name_parts = joint.split('_finger_joint')
            if len(joint_name_parts) == 2:
                replacement = f'{new_name}_finger_joint{joint_name_parts[1]}'
                obj['/**/gripper_trajectory_controller']['ros__parameters']['joints'][idx] = replacement
    elif 'limits' in yaml_name:
        joint_limits = obj.get('joint_limits', {})
        if isinstance(joint_limits, dict):
            new_joint_limits = {}
            for joint_name, limits_val in joint_limits.items():
                if 'finger' not in joint_name:
                    joint_name_parts = joint_name.split('_joint')
                    if len(joint_name_parts) == 2:
                        new_key = f'{new_name}_joint{joint_name_parts[1]}'
                    else:
                        new_key = joint_name
                else:
                    joint_name_parts = joint_name.split('_finger_joint')
                    if len(joint_name_parts) == 2:
                        new_key = f'{new_name}_finger_joint{joint_name_parts[1]}'
                    else:
                        new_key = joint_name
                new_joint_limits[new_key] = limits_val
            obj['joint_limits'] = new_joint_limits
    elif 'moveit' in yaml_name:
        for idx, joint in enumerate(obj['joint_trajectory_controller']['joints']):
            joint_name_parts = joint.split('_joint')
            if len(joint_name_parts) == 2:
                replacement = f'{new_name}_joint{joint_name_parts[1]}'
                obj['joint_trajectory_controller']['joints'][idx] = replacement

        for idx, joint in enumerate(obj['gripper_trajectory_controller']['joints']):
            joint_name_parts = joint.split('_finger_joint')
            if len(joint_name_parts) == 2:
                replacement = f'{new_name}_finger_joint{joint_name_parts[1]}'
                obj['gripper_trajectory_controller']['joints'][idx] = replacement
    else:
        print('INVALID YAML FILE')
    return obj


def main():
    parser = argparse.ArgumentParser(description='Modify YAML files in a ROS package.')
    parser.add_argument('--name', required=True, help='new robot name')
    parser.add_argument('--controller', required=True, help='name of the yaml we are modifing')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='print a summary of replacements'
    )
    args = parser.parse_args()

    name = args.name
    controller = args.controller
    yaml_dir = get_package_share_directory('panda_moveit_config')
    yaml_dir = os.path.join(yaml_dir, 'config')
    yaml_files = [
        f for f in os.listdir(yaml_dir)
        if (
            f == f'controllers_{controller}.yaml'
            or f == 'joint_limits.yaml'
            or f == 'moveit_controller_manager.yaml'
        )
    ]

    for yaml_file in yaml_files:
        print(f'Processing YAML file: {yaml_file}')
        yaml_path = os.path.join(yaml_dir, yaml_file)
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        data = rename_string(data, name, yaml_file)

        yaml.safe_dump(data, sort_keys=False)

        with open(yaml_path, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False)


if __name__ == '__main__':
    main()
