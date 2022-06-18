import os

import sys
import yaml
from ttp import ttp

from transformations import add_management_vlan, get_ports, add_vlans_to_ports, add_loop_protect_to_ports, get_vlans, \
    get_management_ip


def to_yaml_file(obj, filename):
    # print(yaml.dump(obj))
    with open(filename, 'w') as file:
        yaml.dump(obj, file)


def main():
    config_file = sys.argv[1]
    parser = ttp(config_file, './template.pcc')
    parser.parse()

    parser_result = parser.result(structure='dictionary')

    result = parser_result['_root_template_'][0]

    ports = dict(get_ports(result['ports']))
    vlans = dict(get_vlans(result['vlans'], ports))
    add_management_vlan(result['properties']['management_vlan'], vlans)

    add_vlans_to_ports(result['vlans'], ports)
    add_loop_protect_to_ports(result['loop-protect']['range'], ports)

    management_ip = get_management_ip(result['properties']['management_vlan'], vlans)

    hostname = result['properties']['hostname']

    basepath = os.path.join('./out', hostname)
    os.makedirs(basepath, mode=0o755, exist_ok=True)

    to_yaml_file(
        {
            'vlans': vlans,
            'uplink': {'gateway': result['properties']['default-gw']}
        },
        os.path.join(basepath, 'vlans.yml')
    )
    to_yaml_file({'ports': ports}, os.path.join(basepath, 'ports.yml'))

    to_yaml_file(
        {'ansible_host': management_ip,
         'hostname': result['properties']['hostname'],
         'location': result['properties']['location']
         }, os.path.join(basepath, 'common.yml')
    )

if __name__ == '__main__':
    main()
