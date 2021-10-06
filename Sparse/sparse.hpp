#ifndef MINISPARSE_HPP
#define MINISPARSE_HPP

#include <vector>
template <typename T>
struct CSR
{
    std::vector<std::size_t> rowptr;
    std::vector<std::size_t> col;
    std::vector<T> val;

    CSR(std::size_t N) : rowptr(), col(), val(){
        rowptr.reserve(N);
        rowptr.push_back(0);
        rowptr.push_back(0);
    }
    /* data */

    std::size_t num_rows() {
        return rowptr.size() - 1;
    }
    void ordered_insert(std::size_t new_row, std::size_t new_col, T new_val) {
        if(new_row == num_rows() - 1) {

        } else {
            for(auto i = num_rows() - 1; i < new_row; i++) {
                rowptr.push_back(col.size());
            }
        }
        col.push_back(new_col);
        val.push_back(new_val);
        rowptr[num_rows()] += 1;
    }

    void random_insert(std::size_t new_row, std::size_t new_col, T new_val) {
        if(new_row >= num_rows()) { //we haven't inserted something this far along yet
            ordered_insert(new_row, new_col, new_val);
            return;
        }

        auto insert_index = -1;
        auto start_of_row = rowptr.at(new_row);
        auto end_of_row = rowptr.at(new_row+1);
        for(auto i = start_of_row; i < end_of_row; i++) {
            if(new_col == col[i]) {
                val[i] = new_val;
                return;
            }
            if(new_col > col[i]) {
                insert_index = i+1;
            }
        }

        auto col_iterator = col.begin() + insert_index;
        auto val_iterator = val.begin() + insert_index;

        col.insert(col_iterator, new_col);
        val.insert(val_iterator, new_val);

        //update the row ptr values
        for(auto i = new_row + 1; i < rowptr.size(); i++) {
            rowptr[i] += 1;
        }
    }

    T random_retrieve(std::size_t r, std::size_t c) {
        if(r > num_rows) {
            return T();
        }
        for(auto i = rowptr[r]; i < rowptr[r+1]; i++) {
            if(col[i] == c) {
                return val[i];
            }
        }
        return 0;
    }

    std::size_t row_of(std::size_t c) {
        
        return -1;
    }

    std::size_t col_of(std::size_t r) {
        return -1;
    }
    
};




#endif