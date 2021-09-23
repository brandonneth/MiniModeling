from pulp import *

coef_0_1 = 20613
coef_1_0 = 65409
iN = 1024
jN = 1024

d_a_0_1 = LpVariable('d_a_0_1')
d_a_1_0 = LpVariable('d_a_1_0')
d_b_0_1 = LpVariable('d_b_0_1')
d_b_1_0 = LpVariable('d_b_1_0')

prob = LpProblem('MiniModel', LpMinimize)

print("Adding objective function")
prob += coef_0_1 * iN * jN * d_a_0_1 + coef_1_0 * iN * jN * d_a_1_0 + coef_0_1 * iN * jN * d_b_0_1 + coef_1_0 * iN * jN * d_b_1_0

print("Adding constraints")
prob += d_a_0_1 + d_a_1_0 == 1
prob += d_b_0_1 + d_b_1_0 == 1
prob += d_a_0_1 >= 0
prob += d_a_1_0 >= 0
prob += d_b_0_1 >= 0
prob += d_b_1_0 >= 0

print("Writing problem to file")
prob.writeLP("MiniModel.lp")

print("Solving")
prob.solve()

print("Status:", LpStatus[prob.status])

print("Solution")
for v in prob.variables():
	print(v.name, '=', v.varValue)


print("Reading in second problem")
v2, prob2 = LpProblem.fromMPS('three_loops.lp')

print("variables:", v2)
print("Problem:", prob2)