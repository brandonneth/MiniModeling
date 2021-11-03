#include "RAJA.hpp"

int main() {

  using namespace RAJA;

  using VIEW = View<double, Layout<2>>;

  int N = 1024;

  VIEW a(new double[N*N], N,N);
  VIEW b(new double[N*N], N,N);
  VIEW c(new double[N*N], N,N);
  VIEW d(new double[N*N], N,N);
  VIEW e(new double[N*N], N,N);

using KPOL = using KPOL2 = KernelPolicy<
  statement::For<0, loop_exec,
    statement::For<1, loop_exec,
      statement::For<2, loop_exec,
        statement::Lambda<0>
      >
    >
  >
>;
  auto lambda1 = [&](auto i0, auto i1, auto i2) {
    c(i0,i2) += a(i0,i1) * b(i1, i2);
  };

  auto lambda2 = [&](auto i0, auto i1, auto i2) {
    e(i1,i0) += d(i0,i2) * c(i2,i0);
  };
  auto bounds = make_tuple(RangeSegment(0,N), RangeSegment(0,N), RangeSegment(0,N));
  auto knl1 = make_kernel<KPOL>(bounds, lambda1);
  auto knl2 = make_kernel<KPOL>(bounds, lambda2);

  auto named_kernels = all_variants(tie(c), knl1, knl2);

  

  })
}