#include "sparse.hpp"

#include <iostream>
int main() {

    CSR<int> a(5);

    a.ordered_insert(0,1,1);
    a.ordered_insert(1,2,1);
    a.ordered_insert(3,3,1);
    a.ordered_insert(3,4,1);
    a.ordered_insert(4,0,1);

    std::cout << "row ptr: ";
    for(auto r : a.rowptr) {
        std::cout << r << " ";
    }
    std::cout << "\n";

    std::cout << "col: ";
    for(auto r : a.col) {
        std::cout << r << " ";
    }
    std::cout << "\n";

    std::cout << "val: ";
    for(auto r : a.val) {
        std::cout << r << " ";
    }
    std::cout << "\n";

    return 0;
}