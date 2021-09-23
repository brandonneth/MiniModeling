from pulp import *

coef_0_1 = 20613
coef_1_0 = 65409
iN = 1024
jN = 1024

a_0_0_1 = LpVariable('a_0_0_1', 0, 1, LpInteger)
a_0_1_0 = LpVariable('a_0_1_0', 0, 1, LpInteger)
b_0_0_1 = LpVariable('b_0_0_1', 0, 1, LpInteger)
b_0_1_0 = LpVariable('b_0_1_0', 0, 1, LpInteger)
b_1_0_1 = LpVariable('b_1_0_1', 0, 1, LpInteger)
b_1_1_0 = LpVariable('b_1_1_0', 0, 1, LpInteger)
c_1_0_1 = LpVariable('c_1_0_1', 0, 1, LpInteger)
c_1_1_0 = LpVariable('c_1_1_0', 0, 1, LpInteger)
d_2_0_1 = LpVariable('d_2_0_1', 0, 1, LpInteger)
d_2_1_0 = LpVariable('d_2_1_0', 0, 1, LpInteger)
b_2_0_1 = LpVariable('b_2_0_1', 0, 1, LpInteger)
b_2_1_0 = LpVariable('b_2_1_0', 0, 1, LpInteger)


prob = LpProblem('MiniModel2', LpMinimize)

print("Adding objective function")
prob += coef_0_1 * a_0_0_1 + coef_1_0 * a_0_1_0 + coef_0_1 * b_0_0_1 + coef_1_0 * b_0_1_0 + coef_1_0 * b_1_0_1 + coef_0_1 * b_1_1_0  + coef_0_1 * c_1_0_1  + coef_1_0 * c_1_1_0 + coef_1_0 * d_2_0_1 + coef_0_1 * d_2_1_0 + coef_1_0 * b_2_0_1 + coef_0_1 * b_2_1_0

print("Adding constraints")
prob += a_0_0_1 + a_0_1_0 == 1
prob += a_0_0_1 >= 0
prob += a_0_1_0 >= 0
prob += b_0_0_1 + b_0_1_0 == 1
prob += b_0_0_1 >= 0
prob += b_1_0_1 >= 0
prob += b_0_0_1 == b_1_0_1
prob += b_0_0_1 == b_2_0_1
prob += b_0_1_0 == b_1_1_0
prob += b_0_1_0 == b_2_1_0
prob += c_1_0_1 + c_1_1_0 == 1
prob += c_1_0_1 >= 0
prob += c_1_1_0 >= 0
prob += d_2_0_1 + d_2_1_0 == 1
prob += d_2_0_1 >= 0
prob += d_2_1_0 >= 0

print("Writing problem to file")
prob.writeMPS("MiniModel2.mps")

print("Solving")
prob.solve()

print("Status:", LpStatus[prob.status])

print("Solution")
for v in prob.variables():
	print(v.name, '=', v.varValue)
