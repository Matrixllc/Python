

from typing import *
import time
import utils
from exchanges.binance import BinanceClient
from utils import *
from exchanges.ftx import FtxClient
from database import Hdf5Client
import logging

logger = logging.getLogger()


def data_collect(client: Union[BinanceClient, FtxClient], exchange: str, symbol: str):

    h5_db = Hdf5Client(exchange)
    h5_db.create_dataset(symbol)

    # data = h5_db.get_data(symbol, from_time=0, to_time=int(time.time()*1000))
    # data = re_sample_timeframe(data, "15m")
    # print(data)

    oldest_ts, most_recent_ts = h5_db.get_first_last_timestamp(symbol)
    print(oldest_ts, most_recent_ts)
    # Initial Request
    if oldest_ts is None:
        data = client.get_historical_data(symbol, end_time=int(time.time()*1000) - 60000)

        if len(data) == 0:
            logger.warning("%s %s: no initial data found", exchange, symbol)
        else:
            logger.info("%s %s: Collected %s initial data from %s to %s", exchange, symbol, len(data),
                        ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))
        oldest_ts = data[0][0]
        most_recent_ts = data[-1][0]

        h5_db.write_data(symbol, data)

    data_to_insert = []

    # most recent
    while True:
        data = client.get_historical_data(symbol, start_time=int(most_recent_ts + 60000))
        if data is None:
            time.sleep(4)
            continue
        if len(data) < 2:
            break
        data = data[:-1]
        data_to_insert = data_to_insert + data
        if len(data_to_insert) > 500:
            h5_db.write_data(symbol, data)
            data_to_insert.clear()

        if data[-1][0] > most_recent_ts:
            most_recent_ts = data[-1][0]
        logger.info("%s %s: Collected %s recent  data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)
    h5_db.write_data(symbol, data)
    data_to_insert.clear()
    # older
    while True:
        data = client.get_historical_data(symbol, end_time=int(oldest_ts - 60000))
        if data is None:
            time.sleep(4)
            continue
        if len(data) == 0:
            logger.info("%s %s: Stopped older data collection because no data was found before %s", exchange, symbol,
                        ms_to_dt(oldest_ts))
            break

        data_to_insert = data_to_insert + data
        if len(data_to_insert) > 10000:
            h5_db.write_data(symbol, data)
            data_to_insert.clear()

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]
        logger.info("%s %s: Collected %s order data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)
    h5_db.write_data(symbol, data)