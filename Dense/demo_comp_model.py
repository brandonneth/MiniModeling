conv_0_to_0 = min(conv_0_to_0_by_0 , conv_0_to_0_by_0)
conv_0_1_to_0_1 = min(conv_0_1_to_0_1_by_0_1 , conv_0_1_to_0_1_by_0_1 , conv_0_1_to_0_1_by_1_0 , conv_0_1_to_0_1_by_1_0)
conv_0_1_to_1_0 = min(conv_0_1_to_1_0_by_0_1 , conv_0_1_to_1_0_by_0_1 , conv_0_1_to_1_0_by_1_0 , conv_0_1_to_1_0_by_1_0)
conv_1_0_to_0_1 = min(conv_1_0_to_0_1_by_0_1 , conv_1_0_to_0_1_by_0_1 , conv_1_0_to_0_1_by_1_0 , conv_1_0_to_0_1_by_1_0)
conv_1_0_to_1_0 = min(conv_1_0_to_1_0_by_0_1 , conv_1_0_to_1_0_by_0_1 , conv_1_0_to_1_0_by_1_0 , conv_1_0_to_1_0_by_1_0)

from pulp import *

arr2_0_0_1 = LpVariable("arr2_0_0_1")
arr2_0_1_0 = LpVariable("arr2_0_1_0")
conv_arr2_0_0_1_to_0_1 = LpVariable("conv_arr2_0_0_1_to_0_1")
conv_arr2_0_0_1_to_1_0 = LpVariable("conv_arr2_0_0_1_to_1_0")
conv_arr2_0_1_0_to_0_1 = LpVariable("conv_arr2_0_1_0_to_0_1")
conv_arr2_0_1_0_to_1_0 = LpVariable("conv_arr2_0_1_0_to_1_0")
arr1_0_0_1 = LpVariable("arr1_0_0_1")
arr1_0_1_0 = LpVariable("arr1_0_1_0")
conv_arr1_0_0_1_to_0_1 = LpVariable("conv_arr1_0_0_1_to_0_1")
conv_arr1_0_0_1_to_1_0 = LpVariable("conv_arr1_0_0_1_to_1_0")
conv_arr1_0_1_0_to_0_1 = LpVariable("conv_arr1_0_1_0_to_0_1")
conv_arr1_0_1_0_to_1_0 = LpVariable("conv_arr1_0_1_0_to_1_0")
arr0_0_0_1 = LpVariable("arr0_0_0_1")
arr0_0_1_0 = LpVariable("arr0_0_1_0")
conv_arr0_0_0_1_to_0_1 = LpVariable("conv_arr0_0_0_1_to_0_1")
conv_arr0_0_0_1_to_1_0 = LpVariable("conv_arr0_0_0_1_to_1_0")
conv_arr0_0_1_0_to_0_1 = LpVariable("conv_arr0_0_1_0_to_0_1")
conv_arr0_0_1_0_to_1_0 = LpVariable("conv_arr0_0_1_0_to_1_0")
arr2_1_0_1 = LpVariable("arr2_1_0_1")
arr2_1_1_0 = LpVariable("arr2_1_1_0")
arr1_1_0_1 = LpVariable("arr1_1_0_1")
arr1_1_1_0 = LpVariable("arr1_1_1_0")
arr0_1_0_1 = LpVariable("arr0_1_0_1")
arr0_1_1_0 = LpVariable("arr0_1_1_0")

p = LpProblem("Problem", LpMinimize)

p += 0 + coef_d3_2_0 * arr0_0_0_1 + coef_d3_0_2 * arr0_0_1_0 + coef_d3_1_0 * arr1_0_0_1 + coef_d3_0_1 * arr1_0_1_0 + coef_d3_1_2 * arr2_0_0_1 + coef_d3_2_1 * arr2_0_1_0 + coef_d3_1_2 * arr0_1_0_1 + coef_d3_2_1 * arr0_1_1_0 + coef_d3_0_2 * arr1_1_0_1 + coef_d3_2_0 * arr1_1_1_0 + coef_d3_0_1 * arr2_1_0_1 + coef_d3_1_0 * arr2_1_1_0 + 0 + conv_0_1_to_0_1 * conv_arr2_0_0_1_to_0_1 + conv_0_1_to_1_0 * conv_arr2_0_0_1_to_1_0 + conv_1_0_to_0_1 * conv_arr2_0_1_0_to_0_1 + conv_1_0_to_1_0 * conv_arr2_0_1_0_to_1_0 + conv_0_1_to_0_1 * conv_arr1_0_0_1_to_0_1 + conv_0_1_to_1_0 * conv_arr1_0_0_1_to_1_0 + conv_1_0_to_0_1 * conv_arr1_0_1_0_to_0_1 + conv_1_0_to_1_0 * conv_arr1_0_1_0_to_1_0 + conv_0_1_to_0_1 * conv_arr0_0_0_1_to_0_1 + conv_0_1_to_1_0 * conv_arr0_0_0_1_to_1_0 + conv_1_0_to_0_1 * conv_arr0_0_1_0_to_0_1 + conv_1_0_to_1_0 * conv_arr0_0_1_0_to_1_0

p += arr2_0_0_1 + arr2_0_1_0 == 1
p += arr2_1_0_1 == conv_arr2_0_0_1_to_0_1 + conv_arr2_0_1_0_to_0_1
p += arr2_1_1_0 == conv_arr2_0_0_1_to_1_0 + conv_arr2_0_1_0_to_1_0
p += conv_arr2_0_0_1_to_0_1 + conv_arr2_0_0_1_to_1_0 + conv_arr2_0_1_0_to_0_1 + conv_arr2_0_1_0_to_1_0 == 1
p += arr2_0_0_1 == conv_arr2_0_0_1_to_0_1 + conv_arr2_0_0_1_to_1_0
p += arr2_0_1_0 == conv_arr2_0_1_0_to_0_1 + conv_arr2_0_1_0_to_1_0
p += conv_arr2_0_0_1_to_0_1 >= 0
p += conv_arr2_0_0_1_to_1_0 >= 0
p += conv_arr2_0_1_0_to_0_1 >= 0
p += conv_arr2_0_1_0_to_1_0 >= 0
p += arr2_0_0_1 >= 0
p += arr2_0_1_0 >= 0
p += arr1_0_0_1 + arr1_0_1_0 == 1
p += arr1_1_0_1 == conv_arr1_0_0_1_to_0_1 + conv_arr1_0_1_0_to_0_1
p += arr1_1_1_0 == conv_arr1_0_0_1_to_1_0 + conv_arr1_0_1_0_to_1_0
p += conv_arr1_0_0_1_to_0_1 + conv_arr1_0_0_1_to_1_0 + conv_arr1_0_1_0_to_0_1 + conv_arr1_0_1_0_to_1_0 == 1
p += arr1_0_0_1 == conv_arr1_0_0_1_to_0_1 + conv_arr1_0_0_1_to_1_0
p += arr1_0_1_0 == conv_arr1_0_1_0_to_0_1 + conv_arr1_0_1_0_to_1_0
p += conv_arr1_0_0_1_to_0_1 >= 0
p += conv_arr1_0_0_1_to_1_0 >= 0
p += conv_arr1_0_1_0_to_0_1 >= 0
p += conv_arr1_0_1_0_to_1_0 >= 0
p += arr1_0_0_1 >= 0
p += arr1_0_1_0 >= 0
p += arr0_0_0_1 + arr0_0_1_0 == 1
p += arr0_1_0_1 == conv_arr0_0_0_1_to_0_1 + conv_arr0_0_1_0_to_0_1
p += arr0_1_1_0 == conv_arr0_0_0_1_to_1_0 + conv_arr0_0_1_0_to_1_0
p += conv_arr0_0_0_1_to_0_1 + conv_arr0_0_0_1_to_1_0 + conv_arr0_0_1_0_to_0_1 + conv_arr0_0_1_0_to_1_0 == 1
p += arr0_0_0_1 == conv_arr0_0_0_1_to_0_1 + conv_arr0_0_0_1_to_1_0
p += arr0_0_1_0 == conv_arr0_0_1_0_to_0_1 + conv_arr0_0_1_0_to_1_0
p += conv_arr0_0_0_1_to_0_1 >= 0
p += conv_arr0_0_0_1_to_1_0 >= 0
p += conv_arr0_0_1_0_to_0_1 >= 0
p += conv_arr0_0_1_0_to_1_0 >= 0
p += arr0_0_0_1 >= 0
p += arr0_0_1_0 >= 0
p += arr2_1_0_1 + arr2_1_1_0 == 1
p += arr2_1_0_1 >= 0
p += arr2_1_1_0 >= 0
p += arr1_1_0_1 + arr1_1_1_0 == 1
p += arr1_1_0_1 >= 0
p += arr1_1_1_0 >= 0
p += arr0_1_0_1 + arr0_1_1_0 == 1
p += arr0_1_0_1 >= 0
p += arr0_1_1_0 >= 0

p.solve()

for v in p.variables():
	print(v.name, "=", v.varValue)