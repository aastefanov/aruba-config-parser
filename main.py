import os

import sys
import yaml
from ttp import ttp

from transform import transform


def to_yaml_file(obj, filename):
    with open(filename, 'w') as file:
        yaml.dump(obj, file)


def main():
    config_file = sys.argv[1]

    parser = ttp(config_file, './template.pcc')
    parser.parse()

    result = transform(parser.result(structure='dictionary')
                       ['_root_template_'][0])

    basepath = os.path.join('./out', result['hostname'])
    os.makedirs(basepath, mode=0o755, exist_ok=True)

    to_yaml_file(
        {
            'vlans': result['vlans'],
            'uplink': {'gateway': result['gw']}
        },
        os.path.join(basepath, 'vlans.yml')
    )

    to_yaml_file(
        {'ports': result['ports']},
        os.path.join(basepath, 'ports.yml')
    )

    to_yaml_file(
        {
            'ansible_host': result['ip'],
            'hostname': result['hostname'],
            'location': result['location']
        }, os.path.join(basepath, 'common.yml')
    )


if __name__ == '__main__':
    main()
