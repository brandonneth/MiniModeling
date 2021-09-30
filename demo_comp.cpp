#include "RAJA.hpp"

int main() {

  using namespace RAJA;

  using VIEW = View<double, Layout<2>>;

  int N0 = 1024;
  int N1 = 1024;
  int N2 = 1024;

  VIEW a(new double[N0 * N2], N0, N2);
  VIEW b(new double[N0 * N1], N0, N1);
  VIEW c(new double[N1 * N2], N1, N2);

using KPOL1 = KernelPolicy<
  statement::For<2, loop_exec,
    statement::For<0, loop_exec,
      statement::For<1, loop_exec,
        statement::Lambda<0>
      >
    >
  >
>;

using KPOL2 = KernelPolicy<
  statement::For<0, loop_exec,
    statement::For<1, loop_exec,
      statement::For<2, loop_exec,
        statement::Lambda<0>
      >
    >
  >
>;

auto knl1 = make_kernel<KPOL>(make_tuple(RangeSegment(0,N0), RangeSegment(0,N1),RangeSegment(0,N2)), [=] (auto i, auto j, auto k) {
  a(i,k) += b(i,j) * c(j,k);
});
auto knl2 = make_kernel<KPOL>(make_tuple(RangeSegment(0,N0), RangeSegment(0,N1),RangeSegment(0,N2)), [=] (auto i, auto j, auto k) {
  a(i,k) += b(i,j) * c(j,k);
});
std::cout << "[\n";
std::cout << knl1.model_data();
std::cout << ",\n";
std::cout << knl2.model_data();
std::cout << "]";

}
