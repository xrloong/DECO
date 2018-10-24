import sympy
import numpy
import array

from deap import base
from deap import creator
from deap import tools

class Variable:
    def __init__(self, symbol, initLB, initUB):
        self.symbol=symbol
        self.initBounds = (initLB, initUB)

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return repr(self.symbol)

    def getSymbol(self):
        return self.symbol

    def getInitBounds(self):
        return self.initBounds

REQUIRED = 1001001000
STRONG = 1000000
MEDIUM = 1000
WEAK = 1

class Constraint:
    def __init__(self, constraint, strength=REQUIRED):
        self.constraint=constraint
        self.strength=strength

    def __str__(self):
        return str(self.constraint)

    def __repr__(self):
        return repr(self.constraint)

    def getConstraint(self):
        return self.constraint

    def getStrength(self):
        return self.strength

class Problem:
    def __init__(self, variables=[], constraints=[], objective=0):
        self.variables = variables
        self.constraints = constraints
        self.objective = objective

    def getVariables(self):
        return self.variables

    def getConstraints(self):
        return self.constraints

    def getObjective(self):
        return self.objective

    def dump(self):
        print("The problem:")
        print("    Variables: {0}".format(self.getVariables()))
        print("    Constraints: {0}".format(self.getConstraints()))
        print("    Min Objective: {0}".format(self.getObjective()))

NGEN = 200
POPSIZE = 200
F = 0.8
CR = 0.8

def computeRamp(f):
    """
    The ramp function is defined as
    r(x) = f if f(x)>=0
           0 if f(x)<0
    which is equal to max(x, 0)
    """
    return (f+abs(f))/2

def computeSingularityAt0(f):
    """
    The returned function is defined as
    r(x) = 1 if f(x)=0
           0 if f(x)<>0
    which is equal to max(x, 0)
    """
    if hasattr(f, "free_symbols"):
        # Guess it's for SymPy
        import sympy
        return 1-abs(sympy.sign(f))
    else:
        return lambda x: math.floor(1/(abs(x)+1))

def convertConstraintToPenalty(constraint):
    rel_op = constraint.rel_op
    l_minus_r = constraint.lhs - constraint.rhs
    if rel_op == '==':
        violated=abs(l_minus_r)
    elif rel_op in ['<=']:
        violated=l_minus_r
    elif rel_op in ['>=']:
        violated=-l_minus_r
    elif rel_op in ['!=']:
        violated=computeSingularityAt0(l_minus_r)
    elif rel_op in ['<']:
        violated=l_minus_r + computeSingularityAt0(l_minus_r)
    elif rel_op in ['>']:
        violated=-l_minus_r + computeSingularityAt0(l_minus_r)
    else:
        assert False

    penalty = computeRamp(violated)
    return penalty

def mutate(r, a, b, c, f):
    size = len(r)
    for i in range(size):
        r[i] = a[i] + f*(b[i]-c[i])
    return r

class DESolver:
    def __init__(self, cr=CR, f=F, random=None, seed=None, **kwargs):
        assert 0<=f<=2
        self.cr = cr
        self.f = f

        if not random:
            import random
            if seed:
                r = random.Random(seed)
            else:
                r = random.Random()
        self.random = r

    def getMate(self):
        def mate(v, u, cr=self.cr):
            size = len(v)
            rnbr = self.random.randrange(size)
            for i in range(size):
                if self.random.random() < cr or i==rnbr:
                    v[i] = u[i]
            return v
        return mate

    def solve(self, problem, popsize=None, ngen=None, verbose=False, **kwargs):
        if verbose:
            problem.dump()

        variables = problem.getVariables()
        constraints = problem.getConstraints()
        objective = problem.getObjective()
        symbols = [_.getSymbol() for _ in variables]
        variableCount = len(variables)

        if popsize is None:
            popsize = max(len(constraints)*6, 6)

        if ngen is None:
            ngen = len(variables) * max(len(constraints), 6) * 10

        penalties = tuple(convertConstraintToPenalty(c.getConstraint()) for c in constraints)
        cWeights = tuple(c.getStrength() for c in constraints)

        targetObjective = objective + sum(map(lambda _: _[0]*_[1], zip(cWeights, penalties)))
        lambdifiedObjective = sympy.lambdify(symbols, objective)
        lambdifiedTargetObjective = sympy.lambdify(symbols, targetObjective)

        evaluateTarget = lambda params: (lambdifiedTargetObjective(*params),)
        evaluate = lambda params: (lambdifiedObjective(*params),)

        if verbose:
            print("The final objective to be minimized:", targetObjective)

        if objective.is_constant():
            evaluateForStats = lambda ind: ind.fitness.values
        else:
            evaluateForStats = lambda ind: evaluate(ind)

        creator.create("FitnessMin", base.Fitness, weights=(-1, ))
        creator.create("Individual", array.array, typecode='f', fitness=creator.FitnessMin)

        # Attribute generator
        toolbox = base.Toolbox()

        def genIndividual():
            return [self.random.uniform(*_.getInitBounds()) for _ in variables]

        # Structure initializers
        toolbox.register("individual", tools.initIterate, creator.Individual, genIndividual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", evaluateTarget)
        toolbox.register("mutate", mutate, f=self.f)
        toolbox.register("mate", self.getMate())
        toolbox.register("select", self.random.sample, k=3)

        # Prepare population
        pop = toolbox.population(n=popsize)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(evaluateForStats)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        fitnesses = toolbox.map(toolbox.evaluate, pop)
        for ind, fitValues in zip(pop, fitnesses):
            ind.fitness.values = fitValues

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(pop), **record)
        if verbose:
            print(logbook.stream)

        for g in range(1, ngen):
            children = []
            for p in pop:
                a, b, c = [toolbox.clone(ind) for ind in toolbox.select(pop)]
                u = toolbox.clone(p)
                u = toolbox.mutate(u, a, b, c)

                v = toolbox.clone(p)
                v = toolbox.mate(v, u)
                del v.fitness.values
                children.append(v)

            fitnesses = toolbox.map(toolbox.evaluate, children)
            for ind, fitValues in zip(children, fitnesses):
                ind.fitness.values = fitValues

            for i, child in enumerate(children):
                p = pop[i]
                pop[i] = max(pop[i], child, key=lambda p: p.fitness)

            hof.update(pop)
            record = stats.compile(pop)
            logbook.record(gen=g, evals=len(pop), **record)
            if verbose:
                print(logbook.stream)

        del creator.FitnessMin
        del creator.Individual

        individual = hof[0]

        return individual.tolist()

def deSolve(problem, **kwargs):
    solver = DESolver(**kwargs)
    return solver.solve(problem, **kwargs)

