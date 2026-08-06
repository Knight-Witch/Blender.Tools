from mathutils import Vector, kdtree


def weight_group_names(obj):
    return {vg.name for vg in obj.vertex_groups}


def candidate_suffix_pairs(props):
    pairs = [(props.wtm_left_suffix, props.wtm_right_suffix)]
    common = [('.L', '.R'), ('_L', '_R'), ('-L', '-R'), ('.l', '.r'), ('_l', '_r')]
    for pair in common:
        if pair not in pairs:
            pairs.append(pair)
    return pairs


def detect_active_suffix_pair(obj, props):
    names = weight_group_names(obj)
    best_pair = (props.wtm_left_suffix, props.wtm_right_suffix)
    best_count = -1
    for left_suffix, right_suffix in candidate_suffix_pairs(props):
        count = 0
        for name in names:
            if name.endswith(left_suffix) and (name[:-len(left_suffix)] + right_suffix) in names:
                count += 1
            elif name.endswith(right_suffix) and (name[:-len(right_suffix)] + left_suffix) in names:
                count += 1
        if count > best_count:
            best_count = count
            best_pair = (left_suffix, right_suffix)
    return best_pair


def vertex_group_weight_map(obj, group_index):
    result = {}
    for vertex in obj.data.vertices:
        for group in vertex.groups:
            if group.group == group_index:
                result[vertex.index] = group.weight
                break
    return result


def clear_group(group, vertex_count):
    if group is not None:
        group.remove(list(range(vertex_count)))


def backup_group(obj, group_name):
    source = obj.vertex_groups.get(group_name)
    if source is None:
        return None
    backup_name = f'{group_name}__WTM_BAK'
    previous = obj.vertex_groups.get(backup_name)
    if previous is not None:
        obj.vertex_groups.remove(previous)
    backup = obj.vertex_groups.new(name=backup_name)
    for index, weight in vertex_group_weight_map(obj, source.index).items():
        backup.add([index], weight, 'REPLACE')
    return backup


def build_mirror_map(obj, tolerance):
    verts = obj.data.vertices
    kd = kdtree.KDTree(len(verts))
    for vert in verts:
        kd.insert(vert.co.copy(), vert.index)
    kd.balance()
    mapping = {}
    for vert in verts:
        target = Vector((-vert.co.x, vert.co.y, vert.co.z))
        _co, index, distance = kd.find(target)
        if distance <= tolerance:
            mapping[vert.index] = index
    return mapping


def is_same_name_candidate(name, left_suffix, right_suffix):
    return not (name.endswith(left_suffix) or name.endswith(right_suffix))
