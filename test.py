import time
import numpy as np
import pandas as pd
from database import  Hdf5Client
from utils import *

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


# import and format teh data
h5_db = Hdf5Client("binance")
data = h5_db.get_data("BTCUSDT", from_time=0, to_time=int(time.time()*1000))
data = re_sample_timeframe(data, "1h")

data["high_low_average"] = (data["high"] + data["low"])/2

data["signal"] = np.where(data["close"] > data["high_low_average"], 1, -1)
print(data)