import itertools
#import accesses
from constraints import all_constraints, all_variable_names
from coefficients import write_eval_file
from objective import computation_objective_function
import json

def extract_kernel_data(filename):
	with open(filename,'r') as f:
		d = json.load(f)
		return d

kernel_data = extract_kernel_data('demo_comp.info')

kernel_number = 0
nesting_order = kernel_data['NestingOrder']
parameters = kernel_data['LambdaParameters']
access_args = kernel_data['AccessArguments']
layouts = kernel_data['DataLayouts']

name_dim_pairs = [(t[0], len(t)-1) for t in access_args]

variables = all_variable_names(1, name_dim_pairs)


constraints = all_constraints(1, name_dim_pairs)


write_eval_file('coef_eval_demo_comp.cpp', max_depth=len(nesting_order), max_dimensionality=2)


objective_function = computation_objective_function([kernel_data])


print('Variables:')
for v in variables:
	print(v)

print("\nconstraints")
for c in constraints:
	print(c)

print("Objective Function: ", objective_function)

