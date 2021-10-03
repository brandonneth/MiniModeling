#include <iostream>
#include <ctime>



void coef_0_1(double * a, int n0, int n1) {

  auto start = std::clock();
  for(int i0 = 0; i0 < n0; i0++) {
    for (int i1 = 0; i1 < n1; i1++) {
      a[i0*n0 + i1] = 1;
    }
  }
  auto stop = std::clock();
  auto t = stop - start;
  std::cout << "coef_0_1 = " << t <<  "\n";
}

void coef_1_0(double * a, int n1, int n0) {

  auto start = std::clock();
  for (int i1 = 0; i1 < n1; i1++) {
    for(int i0 = 0; i0 < n0; i0++) {
      a[i0*n0 + i1] = 1;
    }
  }
  auto stop = std::clock();
  auto t = stop - start;
  std::cout << "coef_1_0 = " << t << std::endl ;

}

int main() {

  int iN = 2048;
  int jN = 2048;

  double * a = new double[iN * jN];

  coef_0_1(a, iN, jN);

  coef_1_0(a, jN, iN);


}
