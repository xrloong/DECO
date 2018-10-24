#
# maximize 40x+30y
# x>=0, y>=0
# x+y<=240
#
import sympy as sp

import deco
from deco.solver import Problem, Variable, Constraint
from deco.solver import deSolve

x, y = sp.symbols("x,y")
variables = [Variable(x, 0, 240), Variable(y, 0, 240)]
constraints = [
        Constraint(x>=0),
        Constraint(y>=0),
        Constraint(x+y<=240),
    ]
objective = -(x*40+y*30) # for min
problem = Problem(variables, constraints, objective)
solution = deSolve(problem, seed=64, verbose=True)

print()
print("The solution is at x={0}, y={1}".format(int(solution[0]+0.5), int(solution[1]+0.5)))
print()

