def deep_merge(merge_into, merge_from, path=None):
    if path is None: path = []
    for key in merge_from:
        if key in merge_into:
            if isinstance(merge_from[key], dict) and isinstance(merge_into[key], dict):
                deep_merge(merge_into[key], merge_from[key], path + [str(key)])
            elif merge_into[key] == merge_from[key]:
                pass
            else:
                raise Exception('Cannot merge dictionary with non-dictionary element: %s' % '.'.join(path + [str(key)]))
        else:
            merge_into[key] = merge_from[key]
