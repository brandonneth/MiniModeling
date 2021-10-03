
import itertools

from names import * 


coef_names_2_2 = all_computation_coefficient_names(max_depth=2, max_dimensionality=2)

print("All coefficient names for max depth = 2 max dimensionality = 2")
for c in coef_names_2_2:
	print(c)




def for_loop_nest(nesting_order, statement):
	decls = ['for(int i%(num)d = 0; i%(num)d < N%(num)d; i%(num)d++) {' % {'num' : i} for i in tuple(nesting_order)]

	nest = ''
	indent = 0
	for decl in decls:
		nest += indent * ' ' + decl + '\n'
		indent += 1

	nest += indent*' ' + statement + '\n'

	for decl in decls:
		indent -= 1
		nest += indent * " " + "}\n"

	return nest

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


def computation_coefficient_function(nesting_depth, access_order):
	order_str = "_".join([str(a) for a in access_order])

	template_line = 'template <typename VIEW>'
	func_name_line = 'void ' + computation_coefficient_function_name(nesting_depth, access_order)
	params_line = '(VIEW a, ' + bounds_declarations(nesting_depth) + ') {'	

	start_line = 'auto start = std::clock();'
	loop_nest = for_loop_nesting_start(nesting_depth) + "\n" + '  ' * nesting_depth + access_statement(access_order) + "\n" + for_loop_nesting_end(nesting_depth)
	stop_line = 'auto stop = std::clock();'
	t_line = 'auto t = stop - start;'
	print_line = 'std::cout << "{} = " << t << std::endl;'.format(computation_coefficient_name(nesting_depth, access_order))

	close_line = '}'

	function_body = '\n  '.join([])
	function_text = '\n'.join([template_line, func_name_line, params_line, start_line, loop_nest, stop_line, t_line, print_line , close_line])

	return function_text


f_d3_0_2_1 = computation_coefficient_function(4, (0,2,1))
print(f_d3_0_2_1)




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

	func_name = computation_coefficient_function_name(nesting_depth, access_order)
	return func_name + '({},{});'.format(vname, nest_sizes)

def computation_coefficient_function_invocation(nesting_depth, access_order):
	alloc_line = memory_allocation(nesting_depth, access_order)
	view_line = view_decl(nesting_depth, access_order)
	call_line = func_invocation(nesting_depth, access_order)
	free_line = 'free({});'.format("_" + view_name(nesting_depth,access_order))

	return '\n'.join([alloc_line, view_line, call_line, free_line])

invoke_d3_0_2_1 = computation_coefficient_function_invocation(4, (0,2,1))
print(invoke_d3_0_2_1)

def view_typedef(num_dims):
	return 'using VIEW{} = RAJA::View<double,RAJA::Layout<{}>>;'.format(num_dims, num_dims)





def conversion_coefficient_function(layout_in, layout_out, nesting_order):
	
	template_line = "template <typename VIEW>"

	func_name_line = 'void ' + conversion_coefficient_function_name(layout_in, layout_out, nesting_order)
	
	params = "VIEW in, VIEW out"
	params_line = "(" + params + ") {"


	start_line = 'auto start = std::clock();'
	

	in_access = ','.join(['i'+str(l) for l in layout_in])
	out_access = ','.join(['i'+str(l) for l in layout_out])

	statement = 'out(' + out_access + ") = in(" + in_access + ");"

	for_loop = for_loop_nest(nesting_order, statement)

	stop_line = 'auto stop = std::clock();'
	t_line = 'auto t = stop - start;'
	print_line = 'std::cout << "{} = " << t << std::endl;'.format(conversion_coefficient_name(layout_in, layout_out, nesting_order))

	close_line = '}'

	lines = [template_line, func_name_line, params_line, start_line, for_loop, stop_line, t_line, print_line, close_line]
	return '\n'.join(lines)

def conversion_coefficient_function_invocation(layout_in, layout_out, nesting_order):

	func_name = conversion_coefficient_function_name(layout_in, layout_out, nesting_order)
	in_view_name = func_name + "_in"
	out_view_name = func_name + "_out"

	in_mem = in_view_name + "_"
	out_mem = out_view_name + "_"

	mem_amount = '*'.join(['N'+str(l) for l in layout_in])

	in_alloc = 'double * ' + in_mem + ' = new double[' + mem_amount + '];'
	out_alloc = 'double * ' + out_mem + ' = new double[' + mem_amount + '];'

	in_view = 'VIEW{} {}({}, {});'.format(len(layout_in), in_view_name, in_mem, ', '.join(['N' + str(l) for l in layout_in]))
	out_view = 'VIEW{} {}({}, {});'.format(len(layout_out), out_view_name, out_mem, ', '.join(['N' + str(l) for l in layout_out]))

	call_line = func_name + "(" + in_view_name + "," + out_view_name + ");"

	frees = '\n'.join(['free(' + d + ");" for d in [in_mem, out_mem]])

	return '\n'.join([in_alloc, out_alloc, in_view, out_view, call_line, frees])

def write_eval_file(filename, max_depth=3, max_dimensionality=3, psize = 1024):
	includes = ['<iostream>', '<ctime>', '"RAJA.hpp"']
	header = '\n'.join(['#include ' + i for i in includes])

	view_defs = '\n'.join([view_typedef(i) for i in range(1, max_dimensionality+1)])
	comp_defs = ''
	for nesting_depth in range(1,max_depth+1):
		for array_dimensionality in range(1, max_dimensionality+1):
			comp_defs += '\n'.join([computation_coefficient_function(nesting_depth, access_order) for access_order in access_orders(nesting_depth, array_dimensionality)]) + "\n"
	
	conv_defs = ''
	for array_dimensionality in range(1, max_dimensionality + 1):
		dims = tuple(range(0,array_dimensionality))
		perms = list(itertools.permutations(dims))

		combos = itertools.product(perms, perms, perms)

		for (in_layout,out_layout,nesting_order) in combos:
			conv_defs += conversion_coefficient_function(in_layout, out_layout, nesting_order) + "\n\n"



	main_def = 'int main() {'

	n_defs = '\n'.join(['int N{} = {};'.format(i, psize) for i in range(0,max_depth)])

	comp_calls = ''
	for nesting_depth in range(1,max_depth+1):
		for array_dimensionality in range(1, max_dimensionality+1):
			comp_calls += '\n'.join([computation_coefficient_function_invocation(nesting_depth, access_order) for access_order in access_orders(nesting_depth, array_dimensionality)]) + "\n"

	conv_calls = ''
	for array_dimensionality in range(1, max_dimensionality + 1):
		dims = tuple(range(0,array_dimensionality))
		perms = list(itertools.permutations(dims))

		combos = itertools.product(perms, perms, perms)

		for (in_layout,out_layout,nesting_order) in combos:
			conv_calls += conversion_coefficient_function_invocation(in_layout, out_layout, nesting_order) + "\n\n"

	file_text = '\n'.join([header, n_defs, view_defs, comp_defs, conv_defs, main_def,  comp_calls, conv_calls, '}'])
	
	with open(filename, 'w') as f:
		f.write(file_text)

write_eval_file('coef_eval_2_2.cpp', max_depth=2, max_dimensionality=2)





