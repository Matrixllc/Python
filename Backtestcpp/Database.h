#include <string>
#include <hdf5.h>
using namespace std;

class Database
{
private:
    /* data */
public:
    Database(const string& file_name);
    void close_file();
    double **get_data(const string &symbol, const string &exchange,int& array_size);
    hid_t h5_file;
  
};

int compare(const void* pa, const void* pb);


