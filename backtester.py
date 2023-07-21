from database import Hdf5Client
from ctypes import *
import strategies.obv
import strategies.ichimoku
import strategies.support_resistance
from utils import *


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):

    params_des = START_PARAMS[strategy]
    params = dict()
    for p_code, p in params_des.items():
        while True:
            try:
                 params[p_code] = p["type"](input(p["name"] + ": "))
                 break
            except ValueError:
                continue

    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = re_sample_timeframe(data, tf)

        pnl = strategies.obv.backtest(data, ma_peroid=params["ma_period"])
        return pnl
    elif strategy == "ichimoku":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = re_sample_timeframe(data, tf)

        pnl = strategies.ichimoku.backtest(data, tenkan_period=params["tenkan"], kijun_period=params["kijun"])
        return pnl

    elif strategy == "sup_res":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = re_sample_timeframe(data, tf)

        pnl = strategies.support_resistance.backtest(data, min_points=params["min_points"],
                                                     min_diff_points=params["min_diff_points"],
                                                     rounding_nb=params["rounding_nb"],
                                                     trade_profit=params["take_profit"],
                                                     stop_loss=params["stop_loss"])
        return pnl

    elif strategy == "sma":
        lib = CDLL("Backtestcpp/build/libbacttestingcpp.dylib", winmode=0)
        lib.Sma_new.restype = c_void_p
        lib.Sma_new.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_longlong]
        lib.Sma_execute_backtest.restype = c_void_p
        lib.Sma_execute_backtest.argtypes = [c_void_p, c_int, c_int]

        lib.Sma_get_pnl.restype = c_double
        lib.Sma_get_pnl.argtypes = [c_void_p]
        lib.Sma_get_max_dd.restype = c_double
        lib.Sma_get_max_dd.argtypes = [c_void_p]

        obj = lib.Sma_new(exchange.encode(), symbol.encode(), tf.encode(), from_time, to_time)
        lib.Sma_execute_backtest(obj, 15, 8)
        pnl = lib.Sma_get_pnl(obj)
        max_drawdown = lib.Sma_get_max_dd(obj)
        print(pnl)
        print(max_drawdown)





