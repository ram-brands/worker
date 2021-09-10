def compare_vol_weight(bill, tariffs, ref_key, ref_vol_weight):
    differences = []
    negative_dif = 0
    count_dif = 0
    ref_errors = []
    error_cost = 0
    positive_dif = 0
    for ref in bill:
        # my_key = ref_key[ref]
        try:
            my_key = ref_key[ref]
            my_cost = tariffs[my_key]
            bill_cost = bill[ref].cost

            if bill_cost != my_cost:
                count_dif += 1
                bill_vol = bill[ref].volume
                bill_weight = bill[ref].weight
                my_vol = round(ref_vol_weight[ref].total_vol, 2)
                my_weight = round(ref_vol_weight[ref].total_weight, 2)
                differences.append([ref, bill_vol, my_vol, bill_weight, my_weight, bill_cost, my_cost])
                if my_cost > bill_cost:
                    positive_dif += (my_cost - bill_cost)
                else:
                    negative_dif += (bill_cost - my_cost)
        except Exception:
            error_cost += bill[ref].cost
            # if 'P' in ref:
            #     pass
            #     print(ref)
            #     # # exit()
            #     # print(tariffs[my_key])
            #     # exit()
            # formatted_key = f"{my_key.origin}-{my_key.zone}-{my_key.dest_code}-{my_key.weight_code}"
            # ref_errors.append([ref, formatted_key])
            ref_errors.append([ref])
    if len(ref_errors):
        print(f"Cantidad de ref con error: {len(ref_errors)}")
        print(f"Costo total con ref con error: {error_cost}")
    # print(f"Diferencia en {count_dif}/{len(bill)} referencias")
    print(f"Una diferencia negativa de: ${negative_dif}")
    print(f"Una diferencia postiva de: ${positive_dif}")
    print(f"Una diferencia neta de: ${negative_dif - positive_dif}")
    return differences, ref_errors
