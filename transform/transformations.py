from .helpers import get_vlan_names, split_range

LOOP_PROTECT_DEFAULT = True


def add_vlans_to_ports(res, out_ports):
    vlan_names = dict(get_vlan_names(res))
    for vid_str, props in res.items():
        vid = int(vid_str)

        if 'tagged' in props:
            for port in split_range(props['tagged']):
                out_ports.setdefault(int(port), {})
                out_ports[int(port)] \
                    .setdefault('tagged_vlans', []) \
                    .append(vlan_names[vid])

        if 'untagged' in props:
            for port in split_range(props['untagged']):
                out_ports.setdefault(int(port), {})
                out_ports[int(port)] \
                    .setdefault('native_vlan', vlan_names[vid])


def add_loop_protect_to_ports(res, ports):
    if LOOP_PROTECT_DEFAULT:
        for port in set(ports.keys()) - set(split_range(res)):
            ports[port]['loop_protect'] = False
    else:
        for port in split_range(res):
            ports[port]['loop_protect'] = True
