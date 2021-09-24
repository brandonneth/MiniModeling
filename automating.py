
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

print('all constraints')
for c in all_constraints(2, zip(['a','b'], [1, 2])):
	print(c)


def coefficient_name(nesting_depth, access_order):
	order_strs = [str(a) for a in access_order]
	order_str = '_'.join(order_strs) 
	return 'coef_d' + str(nesting_depth) + "_" + order_str


def access_orders(nesting_depth, array_dimensionality):
	index_choices = list(range(0,nesting_depth))

	unpermuted_combinations = set(itertools.combinations_with_replacement(index_choices, array_dimensionality))

	permuted_combination_sets = [set(itertools.permutations(combo)) for combo in unpermuted_combinations]
	
	all_permuted_combos = itertools.chain.from_iterable(permuted_combination_sets)

	return all_permuted_combos

def coefficient_names(nesting_depth, array_dimensionality):
	coef_names = [coefficient_name(nesting_depth, combo) for combo in access_orders(nesting_depth, array_dimensionality)]
	return coef_names




def all_coefficient_names(max_depth=5, max_dimensionality=5):
	names = []
	for d in range(1,max_depth+1):
		for array_dimensionality in range(1,max_dimensionality+1):
			names += coefficient_names(d, array_dimensionality)
	return names

coef_names_2_2 = all_coefficient_names(max_depth=2, max_dimensionality=2)

print("All coefficient names for max depth = 2 max dimensionality = 2")
for c in coef_names_2_2:
	print(c)



def bounds_declarations(nesting_depth):
	declarations = ['int N' + str(i) for i in range(0,nesting_depth)]
	return ', '.join(declarations)

def for_loop_nesting_start(nesting_depth):
	decls = ['  '*i + 'for(int i%(num)d = 0; i%(num)d < N%(num)d; i%(num)d++) {' % {'num' : i} for i in range(0,nesting_depth)]
	return '\n'.join(decls)

def for_loop_nesting_end(nesting_depth):
	brackets = ['  '*(nesting_depth-1-i) + "}" for i in range(0,nesting_depth)]
	return '\n'.join(brackets)

def access_statement(access_order):
	ivars = ['i'+str(a) for a in access_order]

	access_expression = ','.join(ivars)
	return 'a(' + access_expression + ') = 0;'

def coefficient_function(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])

	template_line = 'template <typename VIEW>'
	func_name_line = 'void coefficient_evaluation_d{}_{}'.format(nesting_depth, order_str)
	params_line = '(VIEW a, ' + bounds_declarations(nesting_depth) + ') {'	

	start_line = 'auto start = std::clock();'
	loop_nest = for_loop_nesting_start(nesting_depth) + "\n" + '  ' * nesting_depth + access_statement(access_order) + "\n" + for_loop_nesting_end(nesting_depth)
	stop_line = 'auto stop = std::clock();'
	t_line = 'auto t = stop - start;'
	print_line = 'std::cout << "{} = " << t << std::endl;'.format(coefficient_name(nesting_depth, access_order))

	close_line = '}'

	function_body = '\n  '.join([])
	function_text = '\n'.join([template_line, func_name_line, params_line, start_line, loop_nest, stop_line, t_line, print_line , close_line])

	return function_text


f_d3_0_2_1 = coefficient_function(4, (0,2,1))
print(f_d3_0_2_1)


def view_name(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])
	return 'a_d{}_{}'.format(nesting_depth, order_str)

def memory_allocation(nesting_depth, access_order):
	var_name = '_' + view_name(nesting_depth, access_order)

	extents = ['N' + str(a) for a in access_order]
	size_computation = ' * '.join(extents)

	return 'double * {} = new double [{}];'.format(var_name, size_computation)

def view_decl(nesting_depth, access_order):

	num_dims = len(access_order);

	extents = ['N' + str(i) for i in access_order]
	dim_sizes = ', '.join(extents)

	return 'VIEW{} {} ({}, {});'.format(num_dims, view_name(nesting_depth, access_order), '_'+view_name(nesting_depth,access_order), dim_sizes)

def func_invocation(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])

	vname = view_name(nesting_depth, access_order)
	ns = ['N' + str(i) for i in range(0,nesting_depth)]
	nest_sizes = ', '.join(ns)

	return 'coefficient_evaluation_d{}_{}({},{});'.format(nesting_depth, order_str, vname, nest_sizes)

def coefficient_function_invocation(nesting_depth, access_order):
	alloc_line = memory_allocation(nesting_depth, access_order)
	view_line = view_decl(nesting_depth, access_order)
	call_line = func_invocation(nesting_depth, access_order)
	free_line = 'free({});'.format("_" + view_name(nesting_depth,access_order))

	return '\n'.join([alloc_line, view_line, call_line, free_line])

invoke_d3_0_2_1 = coefficient_function_invocation(4, (0,2,1))
print(invoke_d3_0_2_1)

def view_typedef(num_dims):
	return 'using VIEW{} = RAJA::View<double,RAJA::Layout<{}>>;'.format(num_dims, num_dims)


def write_eval_file(filename, max_depth=3, max_dimensionality=3, psize = 1024):
	includes = ['<iostream>', '<ctime>', '"RAJA.hpp"']
	header = '\n'.join(['#include ' + i for i in includes])

	defs = ''
	for nesting_depth in range(1,max_depth+1):
		for array_dimensionality in range(1, max_dimensionality+1):
			defs += '\n'.join([coefficient_function(nesting_depth, access_order) for access_order in access_orders(nesting_depth, array_dimensionality)]) + "\n"
	
	main_def = 'int main() {'

	n_defs = '\n'.join(['int N{} = {};'.format(i, psize) for i in range(0,max_depth)])

	calls = ''
	for nesting_depth in range(1,max_depth+1):
		for array_dimensionality in range(1, max_dimensionality+1):
			calls += '\n'.join([coefficient_function_invocation(nesting_depth, access_order) for access_order in access_orders(nesting_depth, array_dimensionality)]) + "\n"

	file_text = '\n'.join([header, defs, main_def, n_defs, calls, '}'])
	
	with open(filename, 'w') as f:
		f.write(file_text)

write_eval_file('coef_eval_2_2.cpp', max_depth=2, max_dimensionality=2)

