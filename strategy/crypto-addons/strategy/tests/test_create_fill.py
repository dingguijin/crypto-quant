# -*- coding: utf-8 -*-

import requests

def _main():
    data = {
        "strategy_id": 3,
        "size": 0.001,
        "side": "buy",
        "price": 34343,        
    }
    res = requests.post("http://localhost:8069/cryptocurrency/create_fill", json=data)
    print(res.text)
    return

if __name__ == "__main__":
    _main()
