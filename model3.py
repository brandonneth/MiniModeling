from pulp import *

coef_0_1 = 1
coef_1_0 = 3
iN = 1024
jN = 1024

conv_0_1_to_0_1 = 0
conv_1_0_to_1_0 = 0
conv_0_1_to_1_0 = 2
conv_1_0_to_0_1 = 2

prob = LpProblem('MiniModel3', LpMinimize)

print("Creating variables")
a_0_0_1 = LpVariable('a_0_0_1', 0, 1, LpInteger)
a_0_1_0 = LpVariable('a_0_1_0', 0, 1, LpInteger)
b_0_0_1 = LpVariable('b_0_0_1', 0, 1, LpInteger)
b_0_1_0 = LpVariable('b_0_1_0', 0, 1, LpInteger)
a_conv_0_1_to_0_1 = LpVariable('a_conv_0_1_to_0_1', 0, 1, LpInteger)
a_conv_0_1_to_1_0 = LpVariable('a_conv_0_1_to_1_0', 0, 1, LpInteger)
a_conv_1_0_to_0_1 = LpVariable('a_conv_1_0_to_0_1', 0, 1, LpInteger)
a_conv_1_0_to_1_0 = LpVariable('a_conv_1_0_to_1_0', 0, 1, LpInteger)
b_conv_0_1_to_0_1 = LpVariable('b_conv_0_1_to_0_1', 0, 1, LpInteger)
b_conv_0_1_to_1_0 = LpVariable('b_conv_0_1_to_1_0', 0, 1, LpInteger)
b_conv_1_0_to_0_1 = LpVariable('b_conv_1_0_to_0_1', 0, 1, LpInteger)
b_conv_1_0_to_1_0 = LpVariable('b_conv_1_0_to_1_0', 0, 1, LpInteger)
a_1_0_1 = LpVariable('a_1_0_1', 0, 1, LpInteger)
a_1_1_0 = LpVariable('a_1_1_0', 0, 1, LpInteger)
b_1_0_1 = LpVariable('b_1_0_1', 0, 1, LpInteger)
b_1_1_0 = LpVariable('b_1_1_0', 0, 1, LpInteger)


print("Adding objective function")
prob +=  a_0_0_1 * coef_0_1 + a_0_1_0 * coef_1_0 + b_0_0_1 * coef_0_1 + b_0_1_0 * coef_1_0 + a_1_0_1 * coef_1_0 + a_1_1_0 * coef_0_1 + b_1_0_1 * coef_1_0 + b_1_1_0 * coef_0_1 + conv_0_1_to_0_1 * a_conv_0_1_to_0_1 + conv_0_1_to_1_0 * a_conv_0_1_to_1_0 + conv_1_0_to_0_1 * a_conv_1_0_to_0_1 + conv_1_0_to_1_0 * a_conv_1_0_to_1_0 + conv_0_1_to_0_1 * b_conv_0_1_to_0_1  + conv_0_1_to_1_0 * b_conv_0_1_to_1_0  + conv_1_0_to_0_1 * b_conv_1_0_to_0_1 + conv_1_0_to_1_0 * b_conv_1_0_to_1_0

print("Adding constraints")
prob += a_0_0_1 + a_0_1_0 == 1
prob += b_0_0_1 + b_0_1_0 == 1
prob += a_1_0_1 + a_1_1_0 == 1
prob += b_1_0_1 + b_1_1_0 == 1
prob += a_conv_0_1_to_0_1 + a_conv_0_1_to_1_0 + a_conv_1_0_to_0_1 + a_conv_1_0_to_1_0 == 1
prob += b_conv_0_1_to_0_1 + b_conv_0_1_to_1_0 + b_conv_1_0_to_0_1 + b_conv_1_0_to_1_0 == 1
prob += a_0_0_1 == a_conv_0_1_to_0_1 + a_conv_0_1_to_1_0
prob += a_0_1_0 == a_conv_1_0_to_0_1 + a_conv_1_0_to_1_0
prob += a_1_0_1 == a_conv_0_1_to_0_1 + a_conv_1_0_to_0_1
prob += a_1_1_0 == a_conv_0_1_to_1_0 + a_conv_1_0_to_1_0
prob += b_0_0_1 == b_conv_0_1_to_0_1 + b_conv_0_1_to_1_0
prob += b_0_1_0 == b_conv_1_0_to_0_1 + b_conv_1_0_to_1_0
prob += b_1_0_1 == b_conv_0_1_to_0_1 + b_conv_1_0_to_0_1
prob += b_1_1_0 == b_conv_0_1_to_1_0 + b_conv_1_0_to_1_0



print("Writing problem to file")
prob.writeLP("MiniModel3.lp")

print("Solving")
prob.solve()

print("Status:", LpStatus[prob.status])

print("Solution")
for v in prob.variables():
	print(v.name, '=', v.varValue)
