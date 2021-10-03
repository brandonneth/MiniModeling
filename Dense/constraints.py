from names import *
import itertools


def one_layout_per_computation(computation_number, array_name, array_dimensionality):

	variables = computation_layout_variable_names(computation_number, array_name, array_dimensionality)

	variable_sum = " + ".join(variables)

	return [variable_sum + " == 1"]

def one_conversion_per_conversion(computation_number, array_name, array_dimensionality):
	variables = conversion_layout_variable_names(computation_number, array_name, array_dimensionality)

	variable_sum = " + ".join(variables)

	return [variable_sum + " == 1"]

def computation_conversion_matching(computation_number, array_name, array_dimensionality):

	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))


	constraints = []
	for layout in layout_permutations:
		comp_layout_variable = comp_layout_variable_name(computation_number, array_name, layout)

		conv_input_variables = [conv_layout_variable_name(computation_number, array_name, layout, l) for l in layout_permutations]

		conv_sum = " + ".join(conv_input_variables)

		constraints += [comp_layout_variable + " == " + conv_sum]
	return constraints

def conversion_computation_matching(conversion_number, array_name, array_dimensionality):

	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))


	constraints = []
	for layout in layout_permutations:
		comp_layout_variable = comp_layout_variable_name(conversion_number+1, array_name, layout)

		conv_input_variables = [conv_layout_variable_name(conversion_number, array_name, l, layout) for l in layout_permutations]

		conv_sum = " + ".join(conv_input_variables)

		constraints += [comp_layout_variable + " == " + conv_sum]
	return constraints

def comp_nonnegative(computation_number, array_name, array_dimensionality):
	variables = computation_layout_variable_names(computation_number, array_name, array_dimensionality)

	return [v + " >= 0" for v in variables]

def conv_nonnegative(computation_number, array_name, array_dimensionality):
	variables = conversion_layout_variable_names(computation_number, array_name, array_dimensionality)

	return [v + " >= 0" for v in variables]

def all_constraints(num_computations, name_dim_pairs):
	constraints = []
	for comp_num in range(0, num_computations):
		for (name,dim) in name_dim_pairs:
			constraints += one_layout_per_computation(comp_num, name, dim)

			if comp_num != num_computations - 1:
				constraints += conversion_computation_matching(comp_num, name, dim)
				constraints += one_conversion_per_conversion(comp_num, name, dim)
				constraints += computation_conversion_matching(comp_num, name, dim)
				constraints += conv_nonnegative(comp_num, name, dim)
			constraints += comp_nonnegative(comp_num, name, dim)
	return constraints
