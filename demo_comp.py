import itertools
#import accesses
from constraints import all_constraints, all_variable_names
from coefficients import write_eval_file
from objective import computation_objective_function
import json

from create_model import create_model
def extract_kernel_data(filename):
	with open(filename,'r') as f:
		d = json.load(f)
		return d

kernel_datas = extract_kernel_data('demo_comp.info')

array_details = []
loop_depth = 0
for kernel_data in kernel_datas:
	accesses = kernel_data['AccessArguments']
	array_details += [(a[0], len(a)-1) for a in accesses]
	loop_depth = max(loop_depth, len(kernel_data['NestingOrder']))
array_details = set(array_details)
max_dimensionality = max([a[1] for a in array_details])



write_eval_file('coef_eval_demo_comp.cpp', max_depth=loop_depth, max_dimensionality=max_dimensionality)


model = create_model([kernel_data])

print("Writing Model File")
with open('demo_comp_model.py', 'w') as f:
	f.write(model)
