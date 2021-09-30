import itertools 
import accesses
from constraints import comp_layout_variable_name
from coefficients import computation_coefficient_name, conversion_coefficient_name
def computation_objective_function(kernel_datas):
	kernel_number = 0
	terms = []
	for kernel_data in kernel_datas:
		nesting_order = kernel_data['NestingOrder']
		parameters = kernel_data['LambdaParameters']
		access_args = kernel_data['AccessArguments']
		layouts = kernel_data['DataLayouts']

		for access_arg in access_args:
			name = access_arg[0]
			arguments = access_arg[1:]

			for layout in itertools.permutations(range(0,len(arguments))):
				decision_variable = comp_layout_variable_name(kernel_number, name, layout)

				coefficient_access_order = accesses.normalized_access(parameters, arguments, nesting_order, layout)

				coefficient_name = computation_coefficient_name(len(nesting_order), coefficient_access_order)

				term = coefficient_name + " * " +  decision_variable
				terms += [term]
		kernel_number += 1
	func = " + ".join(terms)
	return func

