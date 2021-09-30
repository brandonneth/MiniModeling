from typing import *
import itertools
import pandas as pd
LambdaParameters = List[str]
LayoutPolicy = List[int]
KernelPolicy = List[int]
AccessArguments = List[str]
StrideOrder = List[int]
AccessIndices = List[int]

#The input data is the access arguments for each access
#The input transformations (also sort of data) are the view's layout, the lambda paramaters, and the kernel policy
def apply_lambda(params: LambdaParameters, args: AccessArguments) -> AccessIndices:
	#apply_lambda args access = foldr (++) [] [elemIndices acc args | acc <- access]
	return [params.index(arg) for arg in args]


def apply_kpol(kpol: KernelPolicy, indices: AccessIndices) -> StrideOrder:
	return [kpol.index(index) for index in indices]


def apply_lpol(lpol: LayoutPolicy, l: List[Any]) -> List[Any]:
	assert len(lpol) == len(l)
	return [l[i] for i in lpol]

def normalized_access(params: LambdaParameters, args: AccessArguments, kpol: KernelPolicy, lpol: LayoutPolicy):
	return apply_kpol(kpol, apply_lpol(lpol, apply_lambda(params, args)))

#
# Tests
#

lambda_params = ["nm", "d", "g", "z"]

phi_access = ["nm", "g", "z"]
ell_access = ["nm", "d"]
psi_access = ["d", "g", "z"]

policy0 = [0,1,2,3]
policy1 = [0,2,3,1]
policy2 = [3,2,1,0]

phi_layout1 = [0,2,1]
ell_layout1 = [1,0]
psi_layout1 = [2,0,1]

phi_layout2 = [0,1,2]
ell_layout2 = [0,1]
psi_layout2 = [0,1,2]

accesses = [phi_access, ell_access, psi_access]
layouts1 = [phi_layout1, ell_layout1, psi_layout1]

print("apply_lambda tests")
assert([0,2,3] == apply_lambda(lambda_params, phi_access))
assert([0,1] == apply_lambda(lambda_params, ell_access))
assert([1,2,3] == apply_lambda(lambda_params, psi_access))

print("apply_kpol tests")
assert([0,1,2] == apply_kpol(policy1, apply_lambda(lambda_params, phi_access)))
assert([3,1,0] == apply_kpol(policy2, apply_lambda(lambda_params, phi_access)))
assert([0,3] == apply_kpol(policy1, apply_lambda(lambda_params, ell_access)))
assert([3,2] == apply_kpol(policy2, apply_lambda(lambda_params, ell_access)))
assert([3,1,2] == apply_kpol(policy1, apply_lambda(lambda_params, psi_access)))
assert([2,1,0] == apply_kpol(policy2, apply_lambda(lambda_params, psi_access)))

print("apply_lpol tests")
assert [0,2,1] == apply_lpol(phi_layout1, apply_kpol(policy1, apply_lambda(lambda_params, phi_access)))
