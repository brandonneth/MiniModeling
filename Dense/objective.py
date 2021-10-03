import itertools 
from accesses import normalized_access
from names import * 


def computation_objective_function(kernel_datas):
	kernel_number = 0
	terms = ["0"]
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

				coefficient_access_order = normalized_access(parameters, arguments, nesting_order, layout)

				coefficient_variable = computation_coefficient_name(len(nesting_order), coefficient_access_order)

				term = coefficient_variable + " * " +  decision_variable
				terms += [term]
		kernel_number += 1
	func = " + ".join(terms)
	return func

def conversion_objective_function(kernel_datas):

	terms = ["0"]
	#first we need all the possible variable names, because the conversions are happening each time.
	array_details = []
	for kernel_data in kernel_datas:
		accesses = kernel_data['AccessArguments']
		array_details += [(a[0], len(a)-1) for a in accesses]
	array_details = set(array_details)

	for kernel_number in range(0,len(kernel_datas)-1):
		for array, dimensionality in array_details:

			layouts = list(itertools.permutations(range(0,dimensionality)))
			for in_l in layouts:
				for out_l in layouts:
					decision_variable = conv_layout_variable_name(kernel_number, array, in_l, out_l)

					coefficient_variable = optimal_conversion_coefficient_name(in_l, out_l)

					term = coefficient_variable + " * " + decision_variable
					terms += [term]

	func = " + ".join(terms)
	return func

def objective_function(kernel_datas):
	comps = computation_objective_function(kernel_datas)
	convs = conversion_objective_function(kernel_datas)
	return comps + " + " + convs

