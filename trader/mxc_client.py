# -*- coding: utf-8 -*-

import time
import requests
import hmac
import hashlib
from urllib import parse

from typing import Optional, Dict, Any, List
from requests import Request, Session, Response

import pprint
import logging

class MxcClient:

    _ROOT_URL = 'https://www.mexc.com'
    
    def __init__(self, api_key=None, api_secret=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, params=params)

    def _sign_request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        request_params = {
            'api_key': self._api_key,
            'req_time': int(time.time()),
        }
        
        if params is not None:
            request_params.update(params)

        params_str = '&'.join('{}={}'.format(k, request_params[k]) for k in sorted(request_params))
        to_sign = '\n'.join([method, path, params_str])
        request_params.update({'sign': hmac.new(self._api_secret.encode(),
                                        to_sign.encode(),
                                        hashlib.sha256).hexdigest()})
        return request_params

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if data['code'] != 200:
                raise Exception(data)
            return data['data']

    def _request(self, method: str, path: str, **kwargs) -> Any:
        params = kwargs.get("params")
        params = self._sign_request(method, path, params)
        kwargs.update({"params": params})
        logging.info("%s, %s" % (method, path))
        pprint.pprint(kwargs)
        request = Request(method, self._ROOT_URL + path, **kwargs)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def get_account_info(self) -> dict:
        return self._get(f'/open/api/v2/account/info')

    def list_symbols(self) -> List[dict]:
        return self._get(f'/open/api/v2/market/symbols')

    def list_trades(self, market: str, limit: int = None) -> List[dict]:
        return self._get(f'/open/api/v2/market/deals', {'symbol': market, 'limit': limit})

    def list_fills(self, market: str, limit: int = None) -> List[dict]:
        return self._get(f'/open/api/v2/order/deals', {'symbol': market, 'limit': limit})

    def get_open_orders(self, market: str) -> List[dict]:
        return self._get(f'/open/api/v2/order/open_orders', {'symbol': market})

    def place_order(self, market: str, price: int, quantity: int, trade_type: str, order_type: str) -> dict:
        return self._post(f'/open/api/v2/order/place', {
            'symbol': market,
            'price': price,
            'quantity': quantity,
            'trade_type': trade_type,
            'order_type': order_type,
        })

    # request with client order id
    def place_orders(self, orders: List[dict]) -> List[Any]:
        return self._post(f'/open/api/v2/order/place_batch', orders)
    
    def cancel_orders(self, order_ids: str) -> dict:
        return self._delete(f'/open/api/v2/order/cancel', {'order_ids': order_ids}) 

    def get_klines(self, market: str, interval: str, limit: int = 100, start_time: int = 0) -> List[dict]:
        return self._get(f'/open/api/v2/market/kline', {'symbol': market, 'interval': interval, 'limit': limit, 'start_time': start_time}) 
    
