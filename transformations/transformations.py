from helpers import split_range
from transformations.helpers import get_vlan_names

LOOP_PROTECT_DEFAULT = True


def add_vlans_to_ports(res, out_ports):
    vlan_names = dict(get_vlan_names(res))
    for vid_str, props in res.items():
        vid = int(vid_str)
        if 'tagged' in props:
            for port in split_range(props['tagged']):
                if int(port) in out_ports:
                    if 'tagged_vlans' not in out_ports[int(port)]:
                        out_ports[int(port)]['tagged_vlans'] = [vlan_names[vid]]
                    else:
                        out_ports[int(port)]['tagged_vlans'].append(vlan_names[vid])
                else:
                    out_ports.append[int(port)] = {'tagged_vlans': [vlan_names[vid]]}
        if 'untagged' in props:
            for port in split_range(props['untagged']):
                if int(port) in out_ports:
                    out_ports[int(port)]['native_vlan'] = vlan_names[vid]
                else:
                    out_ports[int(port)] = {'native_vlan': vlan_names[vid]}


def add_loop_protect_to_ports(res, ports):
    if LOOP_PROTECT_DEFAULT:
        for port in set(ports.keys()) - set(split_range(res)):
            ports[port]['loop_protect'] = False
    else:
        for port in split_range(res):
            ports[port]['loop_protect'] = True
