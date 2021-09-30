
import itertools


def permutation_to_name(perm):
	strs = [str(i) for i in perm]
	return "_".join(strs)

def comp_layout_variable_name(computation_number, array_name, layout_perm):
	perm_string = permutation_to_name(layout_perm)
	return str(array_name) + "_" + str(computation_number) + "_" + perm_string


def conv_layout_variable_name(computation_number, array_name, input_perm, output_perm):
	p1 = permutation_to_name(input_perm)
	p2 = permutation_to_name(output_perm)

	return 'conv_' + str(array_name) + "_" + str(computation_number) + "_" + p1 + "_to_" + p2


def computation_layout_variable_names(computation_number, array_name, array_dimensionality):
	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))

	

	variable_names = [comp_layout_variable_name(computation_number, array_name, perm) for perm in layout_permutations]
	return variable_names

def conversion_layout_variable_names(computation_number, array_name, array_dimensionality):
	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))

	layout_pairs = itertools.product(layout_permutations, layout_permutations)

	variable_names = [conv_layout_variable_name(computation_number, array_name, p[0], p[1]) for p in layout_pairs]
	return variable_names


print(computation_layout_variable_names(0, 'a', 2))

print(conversion_layout_variable_names(0, 'a' ,2))

def all_variable_names(num_computations, name_dim_pairs):
	names = []
	for comp_num in range(0, num_computations):
		for (name,dim) in name_dim_pairs:
			names += computation_layout_variable_names(comp_num, name, dim)
			names += conversion_layout_variable_names(comp_num, name, dim)
	return names

variables = ['a', 'b']
dims = [2, 3]

print(all_variable_names(2, zip(variables, dims)))

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

def nonnegative(computation_number, array_name, array_dimensionality):
	variables = computation_layout_variable_names(computation_number, array_name, array_dimensionality)
	variables += conversion_layout_variable_names(computation_number, array_name, array_dimensionality)

	return [v + " >= 0" for v in variables]


print(one_layout_per_computation(2, 'a', 3))
print(one_conversion_per_conversion(2, 'a', 3))


for c in computation_conversion_matching(1, 'a', 2):
	print(c)

for c in conversion_computation_matching(1, 'a', 2):
	print(c)

def all_constraints(num_computations, name_dim_pairs):
	constraints = []
	for comp_num in range(0, num_computations):
		for (name,dim) in name_dim_pairs:
			constraints += one_layout_per_computation(comp_num, name, dim)
			constraints += one_conversion_per_conversion(comp_num, name, dim)
			constraints += computation_conversion_matching(comp_num, name, dim)
			if comp_num != num_computations - 1:
				constraints += conversion_computation_matching(comp_num, name, dim)
			constraints += nonnegative(comp_num, name, dim)
	return constraints
