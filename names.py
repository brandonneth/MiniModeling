import itertools

def computation_coefficient_name(nesting_depth, access_order):
	order_strs = [str(a) for a in access_order]
	order_str = '_'.join(order_strs) 
	return 'coef_d' + str(nesting_depth) + "_" + order_str

def computation_coefficient_function_name(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])
	return 'computation_coefficient_evaluation_d{}_{}'.format(nesting_depth, order_str)

def view_name(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])
	return 'a_d{}_{}'.format(nesting_depth, order_str)


def conversion_coefficient_name(layout_in, layout_out, nesting_order):
	start = 'conv'
	in_part = "_".join([str(l) for l in layout_in])
	out_part = "_".join([str(l) for l in layout_out])
	by_part = "_".join([str(l) for l in nesting_order])
	return start + '_' + in_part + '_to_' + out_part + "_by_" + by_part

def optimal_conversion_coefficient_name(layout_in, layout_out):
	start = 'conv'
	in_part = "_".join([str(l) for l in layout_in])
	out_part = "_".join([str(l) for l in layout_out])
	return start + '_' + in_part + '_to_' + out_part

def conversion_coefficient_function_name(layout_in, layout_out, nesting_order):
	start = 'conversion_coefficient_evaluation'
	in_part = "_".join([str(l) for l in layout_in])
	out_part = "_".join([str(l) for l in layout_out])
	by_part = "_".join([str(l) for l in nesting_order])
	return start + '_' + in_part + '_to_' + out_part + "_by_" + by_part


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



def access_orders(nesting_depth, array_dimensionality):
	index_choices = list(range(0,nesting_depth))

	unpermuted_combinations = set(itertools.combinations_with_replacement(index_choices, array_dimensionality))

	permuted_combination_sets = [set(itertools.permutations(combo)) for combo in unpermuted_combinations]
	
	all_permuted_combos = itertools.chain.from_iterable(permuted_combination_sets)

	return all_permuted_combos

def computation_coefficient_names(nesting_depth, array_dimensionality):
	coef_names = [computation_coefficient_name(nesting_depth, combo) for combo in access_orders(nesting_depth, array_dimensionality)]
	return coef_names




def all_computation_coefficient_names(max_depth=5, max_dimensionality=5):
	names = []
	for d in range(1,max_depth+1):
		for array_dimensionality in range(1,max_dimensionality+1):
			names += computation_coefficient_names(d, array_dimensionality)
	return names


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


def all_variable_names(num_computations, name_dim_pairs):
	names = []
	for comp_num in range(0, num_computations):
		for (name,dim) in name_dim_pairs:
			names += computation_layout_variable_names(comp_num, name, dim)
			if(comp_num != num_computations-1):
				names += conversion_layout_variable_names(comp_num, name, dim)
	return names