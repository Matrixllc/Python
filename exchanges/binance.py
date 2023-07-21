from typing import *
import requests
import logging
import time
logger = logging.getLogger()


class BinanceClient:

    def __init__(self, futures=False):
        self.futures = futures

        if self.futures:
            self._base_url = "https://fapi.binance.com"
        else:
            self._base_url = "https://api.binance.com"

        # self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):
        proxy = "115.144.102.39:10080"

        proxies = {
            "http": "http://{0}".format(proxy),
            "https": "http://{0}".format(proxy),
        }
        try:
            response = requests.get(self._base_url + endpoint, proxies=proxies, params=query_parameters, timeout=10)
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making requests to %s : %s (status code = %s)",
                         endpoint, response.json(), response.status_code)
            return None

    def _get_symbols(self) -> List[str]:
        params = dict()
        endpoint = "/api/v1/exchangeInfo" if self.futures else "/api/v1/exchangeInfo"
        data = self._make_request(endpoint, params)
        symbols = [x["symbol"] for x in data["symbols"]]

        print(symbols)

        return symbols

    def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None):
        params = dict()

        params["symbol"] = symbol
        params["interval"] = '1m'
        params['limit'] = 1500

        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        endpoint = "/api/v1/exchangeInfo" if self.futures else "/api/v3/klines"

        raw_candles = self._make_request(endpoint, params)

        candles = []
        if raw_candles is not None:
            for c in raw_candles:
                candles.append((float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])))

            return candles
        else:
            return None



