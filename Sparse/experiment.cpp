#include "sparse.hpp"

#include <iostream>
#include <ctime>
template <typename T>
CSR<double> construct_dep_rel_csr_csr(CSR<T> A) {
    CSR<double> deps(A.r,A.c);

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
    CSC<double> deps(A.r, A.c);

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
    CSR<double> deps(A.r, A.c);

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
    CSC<double> deps(A.r, A.c);

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

void compare_execution_dep_rel(std::string filename) {
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

template <typename T>
CSR<double> construct_wave_rel_csr_csr(CSR<T> deps) {
    CSR<double> waves(deps.r, deps.c);
    for(int i = 0; i < waves.r; i++) {
        waves.ordered_insert(i, 0, 1.0);
    }

    int converged = 0;
    while(!converged) {
        converged = 1;
        for(int i = 0; i < deps.num_rows(); i++) {
            for(int k = deps.rowptr[i]; k < deps.rowptr[i+1]; k++) {
                auto t0 = i;
                auto t1 = deps.col[k];

                auto wi = waves.col_of(t0);
                auto wj = waves.col_of(t1);

                if(wj <= wi) {
                    converged = 0;
                    waves.random_delete(t1,wj);
                    
                    waves.random_insert(t1, wi+1, 1.0);

                }
            }
        }
    }

    return waves;
}

template <typename T>
CSC<double> construct_wave_rel_csr_csc(CSR<T> deps) {
    CSC<double> waves(deps.r, deps.c);
    for(int i = 0; i < deps.num_rows(); i++) {
        waves.ordered_insert(i, 0, 1.0);
    }
    int converged = 0;
    while(!converged) {
        converged = 1;
        for(int i = 0; i < deps.num_rows(); i++) {
            for(int k = deps.rowptr[i]; k < deps.rowptr[i+1]; k++) {
                auto t0 = i;
                auto t1 = deps.col[k];
                auto wi = waves.col_of(t0);
                auto wj = waves.col_of(t1);

                if(wj <= wi) {
                    converged = 0;
                    waves.random_delete(t1, wj);
                    waves.random_insert(t1, wi+1, 1.0);
                }
            }
        }
    }

    return waves;
}

template <typename T>
CSR<double> construct_wave_rel_csc_csr(CSC<T> deps) {
    CSR<double> waves(deps.r, deps.c);
    for(int i = 0; i < deps.num_cols(); i++) {
        waves.ordered_insert(i, 0, 1.0);
    }
    int converged = 0;
    while(!converged) {
        converged = 1;
        for(int i = 0; i < deps.num_cols(); i++) {
            for(int k = deps.colptr[i]; k < deps.colptr[i+1]; k++) {
                auto t0 = deps.row[k];
                auto t1 = i;
                auto wi = waves.col_of(t0);
                auto wj = waves.col_of(t1);

                if(wj <= wi) {
                    converged = 0;
                    waves.random_delete(t1,wj);
                    waves.random_insert(t1, wi+1, 1.0);
                }
            }
        }
    }

    return waves;
}

template <typename T>
CSC<double> construct_wave_rel_csc_csc(CSC<T> deps) {
    CSC<double> waves(deps.r, deps.c);
    for(int i = 0; i < deps.num_cols(); i++) {
        waves.ordered_insert(i, 0, 1.0);
    }
    int converged = 0;
    while(!converged) {
        converged = 1;
        for(int i = 0; i < deps.num_cols(); i++) {
            for(int k = deps.colptr[i]; k < deps.colptr[i+1]; k++) {
                auto t0 = deps.row[k];
                auto t1 = i;
                auto wi = waves.col_of(t0);
                auto wj = waves.col_of(t1);

                if(wj <= wi) {
                    converged = 0;
                    waves.random_delete(t1,wj);
                    waves.random_insert(t1, wi+1, 1.0);
                }
            }
        }
    }

    return waves;
}

void compare_execution_wave_rel(std::string filename) {
    CSR<double> A = read_csr<double>(filename);
    
    CSR<double> csr = construct_dep_rel_csr_csr(A);
    CSC<double> csc = construct_dep_rel_csr_csc(A);


    auto rr_start = clock();
    auto wave_rr = construct_wave_rel_csr_csr(csr);
    auto rr_end = clock();
    auto rr_time = rr_end - rr_start;

    std::cout << "CSR CSR: " << rr_time << "\n";

    auto rc_start = clock();
    auto wave_rc = construct_wave_rel_csr_csc(csr);
    auto rc_end = clock();
    auto rc_time = rc_end - rc_start;

    std::cout << "CSR CSC: " << rc_time << "\n";

    auto cr_start = clock();
    auto wave_cr = construct_wave_rel_csc_csr(csc);
    auto cr_end = clock();
    auto cr_time = cr_end - cr_start;

    std::cout << "CSC CSR: " << cr_time << "\n";

    auto cc_start = clock();
    auto wave_cc = construct_wave_rel_csc_csc(csc);
    auto cc_end = clock();
    auto cc_time = cc_end - cc_start;

    
    
    
    std::cout << "CSC CSC: " << cc_time << "\n";

}



void run_experiment() {
    std::cout << "Small example\n";
    std::cout << "dep rel\n";
    compare_execution_dep_rel("smallA.sparse");
    std::cout << "wave rel\n";
    compare_execution_wave_rel("smallA.sparse");
    
    std::cout << "Large example\n";
    std::cout << "dep rel\n";
    compare_execution_dep_rel("bigA.sparse");
    std::cout << "wave rel\n";
    compare_execution_wave_rel("bigA.sparse");

    std::cout << "Huge example\n";
    std::cout << "dep rel\n";
    compare_execution_dep_rel("hugeA.sparse");
    std::cout << "wave rel\n";
    compare_execution_wave_rel("hugeA.sparse");
}

int main() {
    
    CSR<double> dep_rel = CSR<double>(5,5);

    dep_rel.ordered_insert(0,1,1.0);
    dep_rel.ordered_insert(0,2,1.0);
    dep_rel.ordered_insert(1,2,1.0);

    std::cout << "simple dep rel:\n" << dep_rel << "\n";
    print_csr(dep_rel);

    auto waves = construct_wave_rel_csr_csr(dep_rel);

    run_experiment();
}


