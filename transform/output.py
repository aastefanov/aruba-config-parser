from .helpers import *
from .transformations import *


def transform(result):
    ports = dict(get_ports(result['ports']))
    vlans = dict(get_vlans(result['vlans']))

    add_management_vlan(result['properties']['management_vlan'], vlans)
    add_vlans_to_ports(result['vlans'], ports)
    add_loop_protect_to_ports(result['loop-protect']['range'], ports)

    return {
        'ports': ports,
        'vlans': vlans,
        'hostname': result['properties']['hostname'],
        'location': result['properties']['location'],
        'gw': result['properties']['default-gw'],
        'ip': get_management_ip(result['properties']['management_vlan'], vlans),
    }
