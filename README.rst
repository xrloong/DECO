############################################################
DECO - Differential Evolution Constrained Optimizer
############################################################

DECO is a optimizer for general constraint satisfaction problem by using Differential Evolution,
which is a kind of evolutionary algorithm for optimization.

------------------------------------
Linear Programing
------------------------------------
Linear programing is a common constrained optimization problem. Its for is like

maximize
    .. math::
        40x+30y

subject to
    .. math::
        x &>= 0 \\
        y &>= 0 \\
        x+y &<= 240

There had already been some mature algorithms to solve LP like Simplex, Criss-cross algorithm, and Interior Point.

`lp.py <https://github.com/xrloong/DECO/blob/master/examples/lp.py>`_ shows how DECO solve it.

------------------------------------
Chicken with Rabbits Cage
------------------------------------

There is a cage with a number of chickens and rabbits.
There are 35 head and 94 feet.
The question is how many chickens and rabbits are in the cage.

To solve x, y when
    .. math::
        x + y &= 35 \\
        2x + 4y &= 94

We can consider an equation as a constraint, so that it can be defined by

minimize
    .. math::
        f(x,y) = 0

subject to
    .. math::
        x + y &= 35 \\
        2x + 4y &= 94

`chicken_rabbit.py <https://github.com/xrloong/DECO/blob/master/examples/chicken_rabbit.py>`_ shows how DECO solve it.

------------------------------------
Chinese Remainder Problem
------------------------------------
To solve x when
        x % 3 = 2

        x % 5 = 3

        x % 7 = 2

also, we can rewrite it to
    maximize
        f(x) = 0
    subject to
        x % 3 = 2

        x % 5 = 3

        x % 7 = 2

`chinese_remainder.py <https://github.com/xrloong/DECO/blob/master/examples/chinese_remainder.py>`_ shows how DECO solve it.

************************************
Non-Linear Programing
************************************

