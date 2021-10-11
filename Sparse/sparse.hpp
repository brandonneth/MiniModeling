#ifndef MINISPARSE_HPP
#define MINISPARSE_HPP

#include <vector>
#include <fstream>
#include <iostream>
template <typename T>
struct CSR
{
    std::vector<std::size_t> rowptr;
    std::vector<std::size_t> col;
    std::vector<T> val;

    CSR(std::size_t N) : rowptr(), col(), val(){
        rowptr.reserve(N+1);
        rowptr.push_back(0);
        rowptr.push_back(0);
    }
    /* data */

    std::size_t num_rows() {
        
        return rowptr.size() - 1;
    }
    void ordered_insert(std::size_t new_row, std::size_t new_col, T new_val) {
        //std::cout << "Ordered insert " << new_row << ", " << new_col << "\n";
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
        //std::cout << "Random insert " << new_row << " , " << new_col << "\n";
        //std::cout << "num rows: " << num_rows() << "\n";
        //std::cout << std::flush;
        if(new_row >= num_rows()) { //we haven't inserted something this far along yet
            ordered_insert(new_row, new_col, new_val);
            return;
        }

        auto insert_index = 0;
        auto start_of_row = rowptr.at(new_row);
        auto end_of_row = rowptr.at(new_row+1);

        //std::cout << "start and end of row: " << start_of_row << ", " << end_of_row << "\n" << std::flush;
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
        if(r > num_rows()) {
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
        int col_index = -1;
        for(int i = 0; i < col.size(); i++) {
            if (col[i] == c) {
                col_index = i;
            }
        }
        if(col_index == -1) {
            return -1;
        }

        // so we know the column we're after is at index col_index of the col array
        // to get that value's row, we can get the row index that comes after it
        int row_index = 0;
        for(int i = 0; i < num_rows(); i++) {
            if(rowptr[i] <= col_index) {
                row_index += 1;
            }
        }
        return row_index;
    }

    std::size_t col_of(std::size_t r) {
       int c = -1;
       for(int i = rowptr[r]; i < rowptr[r+1]; i++) {
           c = col[i];
       }
       return c;
    }
    
    friend std::ostream & operator <<(std::ostream & o, CSR<T> csr) {
        for(int i = 0; i < csr.num_rows(); i++) {
            for(int k = csr.rowptr[i]; k < csr.rowptr[i+1]; k++) {
                o << "(" << i << "," << csr.col[k] << "," << csr.val[k] << ")\n";
            }
        }
        return o;
    }
};

template <typename T>
CSR<T> read_csr(const std::string & filename) {
    std::ifstream file(filename);

    std::size_t cols, rows, vals;
    file >> rows >> cols >> vals;

    CSR<T> csr(rows);
    for(int i = 0; i < vals; i++) {
        std::size_t r, c;
        T v;
        file >> r >> c >> v;
        csr.ordered_insert(r,c,v);
    }
    return csr;
}


template <typename T>
struct CSC
{
    std::vector<std::size_t> colptr;
    std::vector<std::size_t> row;
    std::vector<T> val;

    CSC(std::size_t N) : colptr(), row(), val(){
        colptr.reserve(N+1);
        colptr.push_back(0);
        colptr.push_back(0);
    }
    /* data */

    std::size_t num_cols() {
        return colptr.size() - 1;
    }
    void ordered_insert(std::size_t new_row, std::size_t new_col, T new_val) {
        
        if(new_col == num_cols() - 1) {

        } else {
            for(auto i = num_cols() - 1; i < new_col; i++) {
                colptr.push_back(row.size());
            }
        }
        row.push_back(new_row);
        val.push_back(new_val);
        colptr[num_cols()] += 1;
    }

    void random_insert(std::size_t new_row, std::size_t new_col, T new_val) {
        if(new_col >= num_cols()) { //we haven't inserted something this far along yet
            ordered_insert(new_row, new_col, new_val);
            return;
        }

        auto insert_index = 0;
        auto start_of_col = colptr.at(new_col);
        auto end_of_col = colptr.at(new_col+1);
        for(auto i = start_of_col; i < end_of_col; i++) {
            if(new_row == row[i]) {
                val[i] = new_val;
                return;
            }
            if(new_row > row[i]) {
                insert_index = i+1;
            }
        }

        auto row_iterator = row.begin() + insert_index;
        auto val_iterator = val.begin() + insert_index;

        row.insert(row_iterator, new_row);
        val.insert(val_iterator, new_val);

        //update the col ptr values
        for(auto i = new_col + 1; i < colptr.size(); i++) {
            colptr[i] += 1;
        }
    }

    T random_retrieve(std::size_t r, std::size_t c) {
        if(c > num_cols()) {
            return T();
        }
        for(auto i = colptr[c]; i < colptr[c+1]; i++) {
            if(row[i] == r) {
                return val[i];
            }
        }
        return 0;
    }

    std::size_t row_of(std::size_t c) {
        int r = -1;
        for(int i = colptr[c]; i < colptr[c+1]; i++) {
            r = row[i];
        }
        return r;
        
    }

    std::size_t col_of(std::size_t r) {
       int row_index = -1;
       for(int i = 0; i < row.size(); i++) {
           if (row[i] == r){
               row_index = i;
           }
       }
       if(row_index == -1) {
           return -1;
       }

       int col_index = -1;
       for(int i = 0; i < num_cols(); i++) {
           if(colptr[i] <= row_index) {
               col_index += 1;
           }
       }
       return row_index;
    }
    
    friend std::ostream & operator <<(std::ostream & o, CSC<T> csc) {
        for(int i = 0; i < csc.num_cols(); i++) {
            for(int k = csc.colptr[i]; k < csc.colptr[i+1]; k++) {
                o << "(" << csc.row[k] << "," << i << "," << csc.val[k] << ")\n";
            }
        }
        return o;
    }
}; //CSC<T>

template <typename T>
CSC<T> read_csc(const std::string & filename) {
    std::ifstream file(filename);

    std::size_t cols, rows, vals;
    file >> rows >> cols >> vals;

    CSC<T> csc(cols);
    for(int i = 0; i < vals; i++) {
        std::size_t r, c;
        T v;
        file >> r >> c >> v;
        csc.random_insert(r,c,v);
    }
    return csc;
}

template <typename T>
void print_csr(CSR<T> csr) {
    std::cout << "rowptr: ";
    for(auto i = 0; i < csr.rowptr.size(); i++) {
        std::cout << csr.rowptr[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "   col: ";
    for(auto i = 0; i < csr.col.size(); i++) {
        std::cout << csr.col[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "   val: ";
    for(auto i = 0; i < csr.val.size(); i++) {
        std::cout << csr.val[i] << " ";
    }
    std::cout << std::endl;
}

template <typename T>
void print_csc(CSC<T> csc) {
    std::cout << "colptr: ";
    for(auto i = 0; i < csc.colptr.size(); i++) {
        std::cout << csc.colptr[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "   row: ";
    for(auto i = 0; i < csc.row.size(); i++) {
        std::cout << csc.row[i] << " ";
    }
    std::cout << std::endl;

    std::cout << "   val: ";
    for(auto i = 0; i < csc.val.size(); i++) {
        std::cout << csc.val[i] << " ";
    }
    std::cout << std::endl;
}




#endif