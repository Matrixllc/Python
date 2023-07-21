#include <iostream>
#include <hdf5.h>
#include "Utils.h"
#include "Database.h"
#include "strategies/Sma.h"
#include "strategies/Psar.h"

using namespace std;


int main(int, char**) {
  
    string symbol = "BTCUSDT";
    string exchange = "binance";
    string timeframe = "5m";

    char* symbol_char = strcpy((char*)malloc(symbol.length() +1), symbol.c_str()); 
    char* exchange_char = strcpy((char*)malloc(exchange.length() +1), exchange.c_str());
    char* tf_char = strcpy((char*)malloc(timeframe.length() +1), timeframe.c_str());

    // Sma sma(exchange_char, symbol_char, tf_char, 0, 1.68369312E12);
    Psar psar (exchange_char, symbol_char, tf_char, 0, 1.68369312E12);

    psar.execute_backtest(0.02, 0.02, 0.2);
    printf("%f | %f\n", psar.pnl, psar.max_dd);



    // for(int i=0; i< 100;i++){
    //     printf("%f %f %f %f %f %f \n", ts[i], open[i], low[i], close[i], volume[i]);
    // }
    // printf("%i \n", ts.size());

    // cout << "Hello, world!\n";
    // hid_t fapl = H5Pcreate(H5P_FILE_ACCESS);
    // hid_t fapl = H5Pcreate(H5P_FILE_ACCESS);
}
