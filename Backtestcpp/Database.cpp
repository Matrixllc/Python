#include "Database.h"
#include <chrono>
#include <cstdlib>
using namespace std;
Database::Database(const string& file_name){
  string FILE_NAME = "../../data/" +file_name +".h5";
  hid_t fapl = H5Pcreate(H5P_FILE_ACCESS);

  herr_t status = H5Pset_libver_bounds(fapl, H5F_LIBVER_LATEST, H5F_LIBVER_LATEST);
  status = H5Pset_fclose_degree(fapl, H5F_CLOSE_STRONG);

  printf("Opening %s", FILE_NAME.c_str());
  h5_file = H5Fopen(FILE_NAME.c_str(), H5F_ACC_RDONLY, fapl);

  if(h5_file < 0 ){

    FILE_NAME = "data/" +file_name +".h5";
     h5_file = H5Fopen(FILE_NAME.c_str(), H5F_ACC_RDONLY, fapl);
     if(h5_file < 0){
        printf("Error while opening %s\n", FILE_NAME.c_str());
     }
    
  }
}

void Database::close_file(){
    H5Fclose(h5_file);
}

double** Database:: get_data(const string&symbol, const string& exchange, int& array_size){
    double** result = {};
    hid_t dataset = H5Dopen2(h5_file, symbol.c_str(), H5P_DEFAULT);
    if(dataset == -1){
        return result;
    }
    auto start_ts = chrono:: high_resolution_clock:: now();
    hid_t dspace = H5Dget_space(dataset);
    hsize_t dims[2];
    H5Sget_simple_extent_dims(dspace,dims,NULL);
    array_size = (int) dims[0];
    result = new double*[dims[0]];
    for(size_t i =0; i < dims[0]; ++i){
        result[i] = new double[dims[1]];
    }
    double* candles_arr = new double[dims[0] * dims[1]];
    H5Dread(dataset, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL,H5P_DEFAULT, candles_arr);

    int j = 0;
    for(int i=0;i <  dims[0]* dims[1]; i+=6){
        result[j][0] = candles_arr[i];
        result[j][1] = candles_arr[i+1];
        result[j][2] = candles_arr[i+2];
        result[j][3] = candles_arr[i+3];
        result[j][4] = candles_arr[i+4];
        result[j][5] = candles_arr[i+5];
        j++;
    }
    delete[] candles_arr;

    qsort(result, dims[0],sizeof(result[0]),compare);

    
    H5Sclose(dspace);
    H5Dclose(dataset);
    auto end_ts = chrono:: high_resolution_clock:: now();
    
    auto read_duration = chrono:: duration_cast<chrono::microseconds>(end_ts-start_ts);
    printf("Fetched %i %s %s data in  %i ms\n", (int)dims[0],exchange.c_str(), symbol.c_str(),(int)read_duration.count());
    return result;


}

int compare(const void* pa, const void* pb){
    const double* a = *(const double**) pa;
    const double* b= *(const double**) pb;
    if(a[0] == b[0]){
        return 0;
    }else if(a[0]< b[0]){
        return -1;
    }else{
        return 1;
    }

}