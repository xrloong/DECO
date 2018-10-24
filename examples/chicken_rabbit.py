#
# 《孫子算經》(https://zh.wikipedia.org/wiki/孫子算經)
# 今有雉、兔同籠，上有三十五頭，下九十四足。問雉、兔各幾何？
#
# Sun Zi Suan Jing (https://en.wikipedia.org/wiki/Sunzi_Suanjing)
# There is a cage with a number of chickens and rabbits.
# There are 35 head and 94 feet.
# The question is how many chickens and rabbits are in the cage.
#

import sympy as sp

import deco
from deco.solver import Problem, Variable, Constraint
from deco.solver import deSolve

chicken, rabbit = sp.symbols("x,y")

variables = [Variable(chicken, 0, 100), Variable(rabbit, 0, 100)]
constraints = [
    Constraint(sp.Eq(chicken+rabbit, 35, evaluate=False)),
    Constraint(sp.Eq(chicken*2+rabbit*4, 94, evaluate=False)),
    Constraint(sp.Eq(chicken%1, 0, evaluate=False)),
    ]
objective = sp.numbers.Zero()
problem = Problem(variables, constraints, objective)
solution = deSolve(problem, seed=64, verbose=True)

print()
print("{0} chicken and {1} rabbits".format(int(solution[0]+0.5), int(solution[1]+0.5)))
print()

