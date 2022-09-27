# -*- coding: utf-8 -*-

import requests

def _main():
    data = {
        "strategy_id": 3,
        "balance": {
            "total_value": 2323232
        },
        "position": {
            "size": 0.001,
            "side": "buy",
            "price": 34343,
            "liquidation_price": 88888
        }
    }
    res = requests.post("http://localhost:8069/cryptocurrency/update_pnl", json=data)
    print(res.text)
    return


if __name__ == "__main__":
    _main()
