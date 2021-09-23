
import itertools

def permutation_to_name(perm):
	strs = [str(i) for i in perm]
	return "_".join(strs)

def computation_layout_variable_names(computation_number, array_name, array_dimensionality):
	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))

	layout_strings = [permutation_to_name(p) for p in layout_permutations]

	variable_names = [str(array_name) + "_" + str(computation_number) + "_" + layout for layout in layout_strings]
	return variable_names

def conversion_layout_variable_names(computation_number, array_name, array_dimensionality):
	dim_index_tuple = tuple(range(0,array_dimensionality))
	layout_permutations = list(itertools.permutations(dim_index_tuple))

	layout_strings = [permutation_to_name(p) for p in layout_permutations]

	layout_pairs = itertools.product(layout_strings, layout_strings)

	variable_names = ['conv_' + str(array_name) + "_" + str(computation_number) + "_" +p[0] + "_to_" + p[1] for p in layout_pairs]
	return variable_names
	pass

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