"""
equation_1: R**2 = (R+B)**2 + b**2 + 2*b*(R+B)*cos(theta-beta)
solved for R: R = sqrt((R+B)**2 + b**2 + 2*b*(R+B)*cos(theta-beta))

equation_2: (R+A)**2 = (R+B)**2 + a**2 + 2*a*(R+B)*cos(theta)
solved for R: R = sqrt((R+B)**2 + a**2 + 2*a*(R+B)*cos(theta) - 2*R*A - A**2)
"""

from sympy import symbols, cos, simplify, pprint, sqrt, acos, pi
from sympy.solvers import solve


# These are the constants
B, A, b, a, beta = symbols(("B", "A", "b", "a", "beta"))
# These are the variables
R, theta = symbols(("R", "theta"))

R_equation_1 = sqrt((R+B)**2 + b**2 + 2*b*(R+B)*cos(theta-beta))
R_equation_2 = sqrt((R+B)**2 + a**2 + 2*a*(R+B)*cos(theta) - 2*R*A - A**2)


def solve_eq_for_theta(R_equation):
    theta_1, theta_2 = solve(R_equation, "theta")
    # produces:
    # theta_1 = -acos((-A**2 + B**2 + a**2)/(2*B*a)) + 2*pi
    # theta_2 = acos((-A**2 + B**2 + a**2)/(2*B*a))
    return theta_1, theta_2


def solve_the_other_equation(the_other_equation, old_theta, theta_expressed):
    """
    Does not work :( IDK how sympy operates,
    so please use the concrete implementation!
    """
    substituted = simplify(the_other_equation.subs(old_theta, theta_expressed))
    new_R_equation = simplify(solve(substituted, "R"))
    return new_R_equation


def concrete_implementation():
    # th was expressed from R_equation_1
    th = -acos((-A**2 + B**2 + a**2)/(2*B*a)) + 2*pi
    # redefine R_equation_2 with th instead of theta
    re_R2 = sqrt((R + B)**2 + a**2 + 2*a*(R + B)*cos(th) - 2*R*A - A**2)
    print("Theta eliminated:", simplify(re_R2))
    print("Solved for R:", simplify(solve(re_R2, "R")))


if __name__ == '__main__':
    # The commented-out section is using the abstract implementation
    # --------------------------------------------------------------
    # th1, th2 = solve_eq_for_theta(R_equation_1)
    # print("theta_1 = ", th1)
    # print("theta_2 = ", th2)
    # new_R1 = solve_the_other_equation(R_equation_2, old_theta=theta, theta_expressed=th1)
    # print("new_R1 = ", new_R1)
    # new_R2 = solve_the_other_equation(R_equation_2, old_theta=theta, theta_expressed=th2)
    # print("new_R2 = ", new_R2)

    concrete_implementation()
