#include <string>
#include<vector>

using namespace std;
class Psar{
    public:
        Psar(char* exchange_c, char* symbol_c, char* timeframe_c,  long long from_time, long long to_time);
        void execute_backtest(double initial_acc, double acc_increment, double max_acc);

        string exchange;
        string symbol;
        string timeframe;

        vector<double> ts, open, high, low,close, volume;

        double pnl =0;
        double max_dd =0.0;

};