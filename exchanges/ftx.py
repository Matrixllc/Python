from typing import *
import requests
import logging
logger = logging.getLogger()


class FtxClient:

    def __init__(self):

        self._base_url = "https://ftx.com/api"
        self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):
        proxy = "104.19.109.209:80"
        proxies = {
            "http": "http://{0}".format(proxy),
            "https": "http://{0}".format(proxy),
        }
        try:
            response = requests.get(self._base_url + endpoint, proxies=proxies, params=query_parameters, timeout=20)
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)

        if response.status_code == 200:
            json_response = response["success"]
            if json_response["success"]:
                return json_response["result"]
            else:
                logger.error("Error while making requests to %s : %s (status code = %s)",
                         endpoint, response.json(), response.status_code)
                return None

    def _get_symbols(self) -> List[str]:
        params = dict()
        endpoint = "/markets"
        data = self._make_request(endpoint, params)
        symbols = [x["name"] for x in data]

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

