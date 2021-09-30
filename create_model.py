import itertools
from names import * 
from constraints import all_constraints, all_variable_names
from objective import objective_function
from coefficients import optimal_conversion_coefficient_declarations

def optimal_conversion_coefficient_declarations(max_depth=3, max_dimensionality=3):

	declarations = []
	for array_dimensionality in range(1, max_dimensionality + 1):
		dims = tuple(range(0,array_dimensionality))
		perms = list(itertools.permutations(dims))

		
		for in_layout in perms:
			for out_layout in perms:
				potential_coefficients = []
				for nesting_order in perms:
					potential_coefficients += [conversion_coefficient_name(in_layout, out_layout, nesting_order)]

				final_coef_name = optimal_conversion_coefficient_name(in_layout, out_layout)

				minimized = 'min(' + ' , '.join(potential_coefficients) + ')'

				declaration = final_coef_name + " = " + minimized
				declarations += [declaration]

	return '\n'.join(declarations)

def variable_declarations(variables):
	return '\n'.join([v + ' = LpVariable("' + v + '")' for v in variables])


def add_constraints(pvar_name, constraints):
	additions = [pvar_name + ' += ' + c for c in constraints]
	return '\n'.join(additions)

def create_model(kernel_datas, problem_name="Problem"):
	array_details = []
	loop_depth = 0
	for kernel_data in kernel_datas:
		accesses = kernel_data['AccessArguments']
		array_details += [(a[0], len(a)-1) for a in accesses]
		loop_depth = max(loop_depth, len(kernel_data['NestingOrder']))
	array_details = set(array_details)
	max_dimensionality = max([a[1] for a in array_details])





	variables = all_variable_names(len(kernel_datas), array_details)
	constraints = all_constraints(len(kernel_datas), array_details)

	objective = objective_function(kernel_datas)

	model = optimal_conversion_coefficient_declarations(max_depth=loop_depth, max_dimensionality=max_dimensionality)
	model += '\n\n'
	model += 'from pulp import *'
	model += '\n\n'
	
	model += variable_declarations(variables)
	model += '\n\n'

	model += 'p = LpProblem("' + problem_name + '", LpMinimize)'
	model += '\n\n'

	model += 'p += ' + objective
	model += '\n\n'

	model += add_constraints('p', constraints)
	model += '\n\n'

	model += 'p.solve()'
	model += '\n\n'

	model += 'for v in p.variables():\n'
	model += '\tprint(v.name, "=", v.varValue)'


	return model
