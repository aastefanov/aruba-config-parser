ASSIGN_VLANS_BY_ID = False


def split_range(numbers):
    ranges = numbers.replace(' ', '').split(',')

    for vl_range in ranges:
        if '-' in vl_range:
            (start, end) = vl_range.split('-', 1)
            for i in range(int(start), int(end) + 1):
                yield i
        else:
            yield int(vl_range)


def add_management_vlan(res, vlans):
    vlans[int(res)]['management'] = True


def get_management_ip(res, vlans):
    return vlans[int(res)]['ip_address']


def get_ports(res):
    for port_str, props in res.items():
        yield int(port_str), {'description': props['name']}


def get_vlan_names(res):
    for vid_str, props in res.items():
        yield int(vid_str), \
              int(vid_str) if ASSIGN_VLANS_BY_ID else props['name']


def get_vlans(res):
    for vid_str, props in res.items():
        vid = int(vid_str)

        if props.keys() <= {'name', 'tagged', 'untagged'}:
            vlan_obj = props['name']
        else:
            vlan_obj = {'name': props['name']}
            if 'ip' in props:
                vlan_obj['ip_address_mode'] = 'IAAM_STATIC'
                vlan_obj['ip_address'] = props['ip']
                vlan_obj['mask'] = props['mask']

        yield vid, vlan_obj
