#
#
import sympy as sp

import deco
from deco.solver import Problem, Variable
from deco.solver import deSolve

x, y, z = sp.symbols("x,y,z")
symbols = [
    Variable(x, -100, 100),
    Variable(y, -100, 100),
    Variable(z, -100, 100)
    ]
constraints = [
    ]
objective = x**2+y**2+z**2 # for min
problem = Problem(symbols, constraints, objective)
solution = deSolve(problem, popsize=10, ngen=200, seed=64, verbose=True)

print()
print("The solution is at x={0}, y={1}, z={2}".format(solution[0], solution[1], solution[2]))
print()

