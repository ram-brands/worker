def consolidate(raw_data):
    header = [
        "SKU",
        "Cant",
        "Tienda",
        "Status",
        "Tracking",
        "Voucher",
        "Fecha",
        "Hora",
        "ASN",
    ]
    data = []
    for asn in raw_data:
        details = asn.details
        format_line = [None] * len(header)
        format_line[header.index("Tienda")] = details.store
        format_line[header.index("Tracking")] = details.tracking_code
        format_line[header.index("Voucher")] = details.voucher_code
        format_line[header.index("Fecha")] = details.date
        format_line[header.index("Hora")] = details.time
        format_line[header.index("ASN")] = details.asn_code
        for sku in asn.faltantes:
            line = format_line.copy()
            line[header.index("SKU")] = sku[0]
            line[header.index("Cant")] = sku[2]
            line[header.index("Status")] = "faltante"
            data.append(line)
        for sku in asn.sobrantes:
            line = format_line.copy()
            line[header.index("SKU")] = sku[0]
            line[header.index("Cant")] = sku[2]
            line[header.index("Status")] = "sobrantes"
            data.append(line)
        return header, data
