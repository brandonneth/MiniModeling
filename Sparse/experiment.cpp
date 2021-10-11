#include "sparse.hpp"

#include <iostream>
#include <ctime>
template <typename T>
CSR<double> construct_dep_rel_csr_csr(CSR<T> A) {
    CSR<double> deps(A.num_rows());

    std::size_t N = A.num_rows();

    for(auto i = 0; i < N; i++) {
        for(auto k = A.rowptr[i]; k < A.rowptr[i+1]; k++) {
            if(i > A.col[k]) {
                deps.random_insert(A.col[k], i, 1);
            }
        }
    }
    return deps;
}

template <typename T>
CSC<double> construct_dep_rel_csr_csc(CSR<T> A) {
    CSC<double> deps(A.num_rows());

    std::size_t N = A.num_rows();
    for(auto i = 0; i < N; i++) {
        for(auto k = A.rowptr[i]; k < A.rowptr[i+1]; k++) {
            if(i > A.col[k]) {
                deps.ordered_insert(A.col[k], i, 1);
            }
        }
    }
    return deps;
}

template <typename T>
CSR<double> construct_dep_rel_csc_csr(CSC<T> A) {
    CSR<double> deps(A.num_cols());

    std::size_t N = A.num_cols();
    for(auto i = 0; i < N; i++) {
        for(auto k = A.colptr[i]; k < A.colptr[i+1]; k++) {
            if(i < A.row[k]) {
                deps.ordered_insert(i, A.row[k], 1);
            }
        }
    }
    return deps;
}

template <typename T>
CSC<double> construct_dep_rel_csc_csc(CSC<T> A) {
    CSC<double> deps(A.num_cols());

    std::size_t N = A.num_cols();
    for(auto i = 0; i < N; i++) {
        for(auto k = A.colptr[i]; k < A.colptr[i+1]; k++) {
             if(i < A.row[k]) {
                deps.random_insert(i, A.row[k], 1);
            }
        }
    }
    return deps;
}

void compare_execution(std::string filename) {
    CSR<double> csr = read_csr<double>(filename);
    CSC<double> csc = read_csc<double>(filename);

    auto rr_start = clock();
    auto dep_rr = construct_dep_rel_csr_csr(csr);
    auto rr_end = clock();
    auto rr_time = rr_end - rr_start;

    auto rc_start = clock();
    auto dep_rc = construct_dep_rel_csr_csc(csr);
    auto rc_end = clock();
    auto rc_time = rc_end - rc_start;

    auto cr_start = clock();
    auto dep_cr = construct_dep_rel_csc_csr(csc);
    auto cr_end = clock();
    auto cr_time = cr_end - cr_start;

    auto cc_start = clock();
    auto dep_cc = construct_dep_rel_csc_csc(csc);
    auto cc_end = clock();
    auto cc_time = cc_end - cc_start;

    std::cout << "CSR CSR: " << rr_time << "\n";
    std::cout << "CSR CSC: " << rc_time << "\n";
    std::cout << "CSC CSR: " << cr_time << "\n";
    std::cout << "CSC CSC: " << cc_time << "\n";

}

int main() {
    compare_execution("smallA.sparse");
}