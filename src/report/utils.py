from typing import List, Dict, MutableMapping, Tuple


def format_tg_results(data: List[Dict]) -> Dict:
    formatted_results = {}
    for d in data:
        for k, v in d.items():
            formatted_results[k] = v

    return formatted_results


def format_response(key: str, response: MutableMapping) -> Dict:
    formatted_response = {
        key: {
            'data': response['data'],
            'total': response['total']
        }
    }

    return formatted_response


def swarm_check(docker_snapshot_results: Dict) -> Tuple:
    swarm_info = docker_snapshot_results['system']['data']['Swarm']
    swarm_mode = swarm_info['LocalNodeState']

    if swarm_mode == 'active':
        swarm_control = swarm_info['ControlAvailable']
        if swarm_control:
            swarm_role = 'manager'
        else:
            swarm_role = 'worker'

        return swarm_mode, swarm_role

    return swarm_mode, None
