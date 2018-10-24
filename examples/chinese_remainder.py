#
# 《孫子算經》(https://zh.wikipedia.org/wiki/孫子算經)
# 有物不知其數，三三數之剩二，五五數之剩三，七七數之剩二。問物幾何？
#
# Chinese remainder theorem(https://en.wikipedia.org/wiki/Chinese_remainder_theorem)
# There are certain things whose number is unknown.
# If we count them by threes, we have two left over;
# by fives, we have three left over;
# and by sevens, two are left over.
# How many things are there?
#
# Here is the equations:
# x % 3 = 2
# x % 5 = 3
# x % 7 = 2

import sympy as sp

import deco
from deco.solver import Problem, Variable, Constraint
from deco.solver import deSolve

x = sp.symbols("x")

variables = [Variable(x, 0, 105)]
constraints = [
    Constraint(sp.Eq(x%3, 2, evaluate=False)),
    Constraint(sp.Eq(x%5, 3, evaluate=False)),
    Constraint(sp.Eq(x%7, 2, evaluate=False)),
    Constraint(sp.Eq(x%1, 0, evaluate=False)),
    Constraint(x>=0),
    Constraint(x<105),
    ]
objective = sp.numbers.Zero()
problem = Problem(variables, constraints, objective)
solution = deSolve(problem, seed=64, verbose=True)

print()
print("The number is {0}.".format(int(solution[0]+0.5)))
print()


