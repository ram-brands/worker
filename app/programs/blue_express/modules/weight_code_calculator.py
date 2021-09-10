


def get_weight_code(basecodes, ref_vol_weight, origin, ref):
    if origin == "Santiago":
        basecode = basecodes['santiago']
    else:
        basecode = basecodes["regiones"]
    vol = ref_vol_weight[ref].total_vol
    weight = ref_vol_weight[ref].total_weight
    max_value = round(max(vol, weight), 1)
    code = get_code(max_value, basecode)
    return code


def get_code(max_value, basecode):
    for bc in basecode:
        if bc.min <= max_value <= bc.max:
            return bc.weightcode
    # print("WEIGHT CODE was not found")
    # exit()

    # CHECK THIS
    return bc.weightcode