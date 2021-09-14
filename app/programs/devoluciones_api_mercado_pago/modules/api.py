import requests

import env
from status import Status


def refund(_, TID, AMOUNT):
    TOKEN = env.API_MP_TOKEN
    API_URL = f"https://api.mercadopago.com/v1/payments/{TID}/refunds"

    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    data = str({"amount": AMOUNT})
    response = requests.post(API_URL, headers=headers, data=data)

    res = response.json()
    try:
        payment_id = res["payment_id"]
        amount = res["amount"]
        status = res["status"]
        _.warning("\nDevolución de:")
        _.warning(f"TID: {payment_id}\nAmount: {amount}\nStatus: {status}")
        if status == "approved":
            return 1, None
        else:
            return 0, [TID, AMOUNT]
    except KeyError:
        _.warning(f"ERROR: TID {TID}")
        _.log(response.text)
        _.status = Status.WARNING
    return 0, [TID, AMOUNT]


if __name__ == "__main__":
    pass
