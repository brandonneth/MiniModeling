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

def conversion_coefficient_function_name(layout_in, layout_out, nesting_order):
	start = 'conversion_coefficient_evaluation'
	in_part = "_".join([str(l) for l in layout_in])
	out_part = "_".join([str(l) for l in layout_out])
	by_part = "_".join([str(l) for l in nesting_order])
	return start + '_' + in_part + '_to_' + out_part + "_by_" + by_part