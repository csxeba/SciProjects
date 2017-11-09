import sympy
from sympy import Symbol, MatrixSymbol

"""
M = (x - mu_0 - alpha * mu_1)^T . (C_0 . alpha * T)^-1 . (x - mu_0 - alpha * mu_1)
"""


def eucl():
    m = Symbol("m")
    # m = 2
    x = MatrixSymbol("x", m, 1)
    mu_0 = MatrixSymbol("mu_0", m, 1)
    mu_1 = MatrixSymbol("mu_1", m, 1)
    alpha = Symbol("alpha")
    d = x - (mu_0 + alpha*mu_1)
    eucl = d.T @ d

    sympy.pprint(eucl)
    deriv = sympy.diff(eucl, alpha)
    sympy.pprint(sympy.solve(deriv, alpha))


def mahal():
    m = Symbol("m")
    # m = 2
    x = MatrixSymbol("x", m, 1)
    mu_0 = MatrixSymbol("mu_0", m, 1)
    mu_1 = MatrixSymbol("mu_1", m, 1)
    C_0 = MatrixSymbol("C_0", m, m)
    T = MatrixSymbol("T", m, m)
    alpha = Symbol("alpha")
    z = x - mu_0 - alpha*mu_1
    B = C_0 @ alpha * T
    mahal = z.T @ B**-1 @ z
    sympy.pprint(mahal)
    deriv = sympy.diff(mahal, alpha)
    sympy.pprint(sympy.simplify(deriv))
    solved = sympy.solve(deriv, alpha)
    sympy.pprint(solved)


if __name__ == "__main__":
    eucl()
