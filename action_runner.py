import yaml
import argparse
import subprocess
from copy import copy

with open("config.yaml") as f:
    config = yaml.safe_load(f)
    config_actions = config["actions"]
    action_choices = []
    for i in config_actions:
        action_choices.append(i)
        for j in config_actions[i]:
            action_choices.append(i+'-'+j)

    config_overrides = config["overrides"]
    action_overrides = []
    for i in config_overrides:
        action_overrides.append(i)

def parse_action(action: str):
    parts = action.split('-')
    _action = parts[0]
    if len(parts) > 1:
        _secondary = parts[1]
        return config['actions'][_action][_secondary]
    else:
        if 'default' in config['actions'][_action]:
            return config['actions'][_action]['default']
        else:
            return list(config['actions'][_action].values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", nargs="*", choices=action_choices)
    parser.add_argument("--overrides", nargs="*", choices=action_overrides)
    args = parser.parse_args()
    print(args.action)
    print(config)
    parsed_list = []
    for i in args.action:
        a = parse_action(i)
        if isinstance(a, list):
            parsed_list.extend(a)
        else:
            parsed_list.append(a)

    print(parsed_list)
    for i in parsed_list:
        out = subprocess.check_output(i, shell=True)
        print(out)



if __name__  == "__main__":
    main()
