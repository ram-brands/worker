def get_order_weight(order_items, vol_weight):
    total_vol = 0
    total_weight = 0
    error_sku = set()
    for sku in order_items:
        try:
            total_vol += vol_weight[sku].volume
            total_weight += vol_weight[sku].weight
        except KeyError:
            error_sku.add(sku)
    return total_vol, total_weight, error_sku
