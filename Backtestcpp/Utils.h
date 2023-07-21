#include <string>
#include<tuple>
#include<vector>
using namespace std;



tuple<vector<double>,vector<double>,vector<double>,vector<double>,
vector<double>,vector<double>> rearrange_candles(double** candles, string tf, long long from_time, long long to_time, int array_size);