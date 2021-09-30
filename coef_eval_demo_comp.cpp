#include <iostream>
#include <ctime>
#include "RAJA.hpp"
int N0 = 1024;
int N1 = 1024;
int N2 = 1024;
using VIEW1 = RAJA::View<double,RAJA::Layout<1>>;
using VIEW2 = RAJA::View<double,RAJA::Layout<2>>;
template <typename VIEW>
void computation_coefficient_evaluation_d1_0
(VIEW a, int N0) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  a(i0) = 0;
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d1_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d1_0_0
(VIEW a, int N0) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  a(i0,i0) = 0;
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d1_0_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_0
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i0) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_1
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i1) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_0_1
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i0,i1) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_0_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_1_0
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i1,i0) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_1_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_1_1
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i1,i1) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_1_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d2_0_0
(VIEW a, int N0, int N1) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    a(i0,i0) = 0;
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d2_0_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_0
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i0) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_1
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i1) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_2
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i2) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_2 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_0_1
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i0,i1) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_0_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_1_0
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i1,i0) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_1_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_1_2
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i1,i2) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_1_2 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_2_1
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i2,i1) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_2_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_0_0
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i0,i0) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_0_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_1_1
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i1,i1) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_1_1 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_0_2
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i0,i2) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_0_2 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_2_0
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i2,i0) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_2_0 = " << t << std::endl;
}
template <typename VIEW>
void computation_coefficient_evaluation_d3_2_2
(VIEW a, int N0, int N1, int N2) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
  for(int i1 = 0; i1 < N1; i1++) {
    for(int i2 = 0; i2 < N2; i2++) {
      a(i2,i2) = 0;
    }
  }
}
auto stop = std::clock();
auto t = stop - start;
std::cout << "coef_d3_2_2 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_0_to_0_by_0
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
 out(i0) = in(i0);
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_0_to_0_by_0 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_0_1_to_0_1_by_0_1
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
 for(int i1 = 0; i1 < N1; i1++) {
  out(i0,i1) = in(i0,i1);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_0_1_to_0_1_by_0_1 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_0_1_to_0_1_by_1_0
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i1 = 0; i1 < N1; i1++) {
 for(int i0 = 0; i0 < N0; i0++) {
  out(i0,i1) = in(i0,i1);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_0_1_to_0_1_by_1_0 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_0_1_to_1_0_by_0_1
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
 for(int i1 = 0; i1 < N1; i1++) {
  out(i1,i0) = in(i0,i1);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_0_1_to_1_0_by_0_1 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_0_1_to_1_0_by_1_0
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i1 = 0; i1 < N1; i1++) {
 for(int i0 = 0; i0 < N0; i0++) {
  out(i1,i0) = in(i0,i1);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_0_1_to_1_0_by_1_0 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_1_0_to_0_1_by_0_1
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
 for(int i1 = 0; i1 < N1; i1++) {
  out(i0,i1) = in(i1,i0);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_1_0_to_0_1_by_0_1 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_1_0_to_0_1_by_1_0
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i1 = 0; i1 < N1; i1++) {
 for(int i0 = 0; i0 < N0; i0++) {
  out(i0,i1) = in(i1,i0);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_1_0_to_0_1_by_1_0 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_1_0_to_1_0_by_0_1
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i0 = 0; i0 < N0; i0++) {
 for(int i1 = 0; i1 < N1; i1++) {
  out(i1,i0) = in(i1,i0);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_1_0_to_1_0_by_0_1 = " << t << std::endl;
}

template <typename VIEW>
void conversion_coefficient_evaluation_1_0_to_1_0_by_1_0
(VIEW in, VIEW out) {
auto start = std::clock();
for(int i1 = 0; i1 < N1; i1++) {
 for(int i0 = 0; i0 < N0; i0++) {
  out(i1,i0) = in(i1,i0);
 }
}

auto stop = std::clock();
auto t = stop - start;
std::cout << "conv_1_0_to_1_0_by_1_0 = " << t << std::endl;
}


int main() {
double * _a_d1_0 = new double [N0];
VIEW1 a_d1_0 (_a_d1_0, N0);
computation_coefficient_evaluation_d1_0(a_d1_0,N0);
free(_a_d1_0);
double * _a_d1_0_0 = new double [N0 * N0];
VIEW2 a_d1_0_0 (_a_d1_0_0, N0, N0);
computation_coefficient_evaluation_d1_0_0(a_d1_0_0,N0);
free(_a_d1_0_0);
double * _a_d2_0 = new double [N0];
VIEW1 a_d2_0 (_a_d2_0, N0);
computation_coefficient_evaluation_d2_0(a_d2_0,N0, N1);
free(_a_d2_0);
double * _a_d2_1 = new double [N1];
VIEW1 a_d2_1 (_a_d2_1, N1);
computation_coefficient_evaluation_d2_1(a_d2_1,N0, N1);
free(_a_d2_1);
double * _a_d2_0_1 = new double [N0 * N1];
VIEW2 a_d2_0_1 (_a_d2_0_1, N0, N1);
computation_coefficient_evaluation_d2_0_1(a_d2_0_1,N0, N1);
free(_a_d2_0_1);
double * _a_d2_1_0 = new double [N1 * N0];
VIEW2 a_d2_1_0 (_a_d2_1_0, N1, N0);
computation_coefficient_evaluation_d2_1_0(a_d2_1_0,N0, N1);
free(_a_d2_1_0);
double * _a_d2_1_1 = new double [N1 * N1];
VIEW2 a_d2_1_1 (_a_d2_1_1, N1, N1);
computation_coefficient_evaluation_d2_1_1(a_d2_1_1,N0, N1);
free(_a_d2_1_1);
double * _a_d2_0_0 = new double [N0 * N0];
VIEW2 a_d2_0_0 (_a_d2_0_0, N0, N0);
computation_coefficient_evaluation_d2_0_0(a_d2_0_0,N0, N1);
free(_a_d2_0_0);
double * _a_d3_0 = new double [N0];
VIEW1 a_d3_0 (_a_d3_0, N0);
computation_coefficient_evaluation_d3_0(a_d3_0,N0, N1, N2);
free(_a_d3_0);
double * _a_d3_1 = new double [N1];
VIEW1 a_d3_1 (_a_d3_1, N1);
computation_coefficient_evaluation_d3_1(a_d3_1,N0, N1, N2);
free(_a_d3_1);
double * _a_d3_2 = new double [N2];
VIEW1 a_d3_2 (_a_d3_2, N2);
computation_coefficient_evaluation_d3_2(a_d3_2,N0, N1, N2);
free(_a_d3_2);
double * _a_d3_0_1 = new double [N0 * N1];
VIEW2 a_d3_0_1 (_a_d3_0_1, N0, N1);
computation_coefficient_evaluation_d3_0_1(a_d3_0_1,N0, N1, N2);
free(_a_d3_0_1);
double * _a_d3_1_0 = new double [N1 * N0];
VIEW2 a_d3_1_0 (_a_d3_1_0, N1, N0);
computation_coefficient_evaluation_d3_1_0(a_d3_1_0,N0, N1, N2);
free(_a_d3_1_0);
double * _a_d3_1_2 = new double [N1 * N2];
VIEW2 a_d3_1_2 (_a_d3_1_2, N1, N2);
computation_coefficient_evaluation_d3_1_2(a_d3_1_2,N0, N1, N2);
free(_a_d3_1_2);
double * _a_d3_2_1 = new double [N2 * N1];
VIEW2 a_d3_2_1 (_a_d3_2_1, N2, N1);
computation_coefficient_evaluation_d3_2_1(a_d3_2_1,N0, N1, N2);
free(_a_d3_2_1);
double * _a_d3_0_0 = new double [N0 * N0];
VIEW2 a_d3_0_0 (_a_d3_0_0, N0, N0);
computation_coefficient_evaluation_d3_0_0(a_d3_0_0,N0, N1, N2);
free(_a_d3_0_0);
double * _a_d3_1_1 = new double [N1 * N1];
VIEW2 a_d3_1_1 (_a_d3_1_1, N1, N1);
computation_coefficient_evaluation_d3_1_1(a_d3_1_1,N0, N1, N2);
free(_a_d3_1_1);
double * _a_d3_0_2 = new double [N0 * N2];
VIEW2 a_d3_0_2 (_a_d3_0_2, N0, N2);
computation_coefficient_evaluation_d3_0_2(a_d3_0_2,N0, N1, N2);
free(_a_d3_0_2);
double * _a_d3_2_0 = new double [N2 * N0];
VIEW2 a_d3_2_0 (_a_d3_2_0, N2, N0);
computation_coefficient_evaluation_d3_2_0(a_d3_2_0,N0, N1, N2);
free(_a_d3_2_0);
double * _a_d3_2_2 = new double [N2 * N2];
VIEW2 a_d3_2_2 (_a_d3_2_2, N2, N2);
computation_coefficient_evaluation_d3_2_2(a_d3_2_2,N0, N1, N2);
free(_a_d3_2_2);

double * conversion_coefficient_evaluation_0_to_0_by_0_in_ = new double[N0];
double * conversion_coefficient_evaluation_0_to_0_by_0_out_ = new double[N0];
VIEW1 conversion_coefficient_evaluation_0_to_0_by_0_in(conversion_coefficient_evaluation_0_to_0_by_0_in_, N0);
VIEW1 conversion_coefficient_evaluation_0_to_0_by_0_out(conversion_coefficient_evaluation_0_to_0_by_0_out_, N0);
conversion_coefficient_evaluation_0_to_0_by_0(conversion_coefficient_evaluation_0_to_0_by_0_in,conversion_coefficient_evaluation_0_to_0_by_0_out);
free(conversion_coefficient_evaluation_0_to_0_by_0_in_);
free(conversion_coefficient_evaluation_0_to_0_by_0_out_);

double * conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_in_ = new double[N0*N1];
double * conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_out_ = new double[N0*N1];
VIEW2 conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_in(conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_in_, N0, N1);
VIEW2 conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_out(conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_out_, N0, N1);
conversion_coefficient_evaluation_0_1_to_0_1_by_0_1(conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_in,conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_out);
free(conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_in_);
free(conversion_coefficient_evaluation_0_1_to_0_1_by_0_1_out_);

double * conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_in_ = new double[N0*N1];
double * conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_out_ = new double[N0*N1];
VIEW2 conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_in(conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_in_, N0, N1);
VIEW2 conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_out(conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_out_, N0, N1);
conversion_coefficient_evaluation_0_1_to_0_1_by_1_0(conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_in,conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_out);
free(conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_in_);
free(conversion_coefficient_evaluation_0_1_to_0_1_by_1_0_out_);

double * conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_in_ = new double[N0*N1];
double * conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_out_ = new double[N0*N1];
VIEW2 conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_in(conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_in_, N0, N1);
VIEW2 conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_out(conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_out_, N1, N0);
conversion_coefficient_evaluation_0_1_to_1_0_by_0_1(conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_in,conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_out);
free(conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_in_);
free(conversion_coefficient_evaluation_0_1_to_1_0_by_0_1_out_);

double * conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_in_ = new double[N0*N1];
double * conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_out_ = new double[N0*N1];
VIEW2 conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_in(conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_in_, N0, N1);
VIEW2 conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_out(conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_out_, N1, N0);
conversion_coefficient_evaluation_0_1_to_1_0_by_1_0(conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_in,conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_out);
free(conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_in_);
free(conversion_coefficient_evaluation_0_1_to_1_0_by_1_0_out_);

double * conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_in_ = new double[N1*N0];
double * conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_out_ = new double[N1*N0];
VIEW2 conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_in(conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_in_, N1, N0);
VIEW2 conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_out(conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_out_, N0, N1);
conversion_coefficient_evaluation_1_0_to_0_1_by_0_1(conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_in,conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_out);
free(conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_in_);
free(conversion_coefficient_evaluation_1_0_to_0_1_by_0_1_out_);

double * conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_in_ = new double[N1*N0];
double * conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_out_ = new double[N1*N0];
VIEW2 conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_in(conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_in_, N1, N0);
VIEW2 conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_out(conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_out_, N0, N1);
conversion_coefficient_evaluation_1_0_to_0_1_by_1_0(conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_in,conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_out);
free(conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_in_);
free(conversion_coefficient_evaluation_1_0_to_0_1_by_1_0_out_);

double * conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_in_ = new double[N1*N0];
double * conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_out_ = new double[N1*N0];
VIEW2 conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_in(conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_in_, N1, N0);
VIEW2 conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_out(conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_out_, N1, N0);
conversion_coefficient_evaluation_1_0_to_1_0_by_0_1(conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_in,conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_out);
free(conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_in_);
free(conversion_coefficient_evaluation_1_0_to_1_0_by_0_1_out_);

double * conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_in_ = new double[N1*N0];
double * conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_out_ = new double[N1*N0];
VIEW2 conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_in(conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_in_, N1, N0);
VIEW2 conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_out(conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_out_, N1, N0);
conversion_coefficient_evaluation_1_0_to_1_0_by_1_0(conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_in,conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_out);
free(conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_in_);
free(conversion_coefficient_evaluation_1_0_to_1_0_by_1_0_out_);


}