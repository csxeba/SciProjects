from sympy import symbols, cos, simplify, pprint, acos, pi
from sympy.solvers import solve

R, B, A, b, a, beta = symbols(
    ("R", "B", "A", "b", "a", "beta"))

# R = (-A**2/2 + B**2/2 - B*a*cos(theta) + a**2/2)/(A - B + a*cos(theta))
# R = B*(B**2 + b**2 - b*cos(beta - theta))/(B + b*cos(beta - theta))

theta = -acos((-A**2 - 2*A*R + B**2 + 2*B*R + a**2)/(2*a*(B + R))) + 2*pi

# R1 = ((2*R*B + B**2 + a**2 - 2*a*cos(theta)*(R+B) - A**2) / (2*A)) - R
R2 = (B**2 + b**2 - 2*b*cos(beta - theta)*(R+B) / (2*B)) - R

pprint(simplify(R2))
print(solve(R2, "theta"))

# theta = -acos((-A**2 - 2*A*R + B**2 + 2*B*R + a**2)/(2*a*(B + R)))
#         + 2*pi, acos((-A**2 - 2*A*R + B**2 + 2*B*R + a**2)/(2*a*(B + R)))
# theta = beta - acos(B*(B**2 - R + b**2)/(b*(B + R))), beta
#         + acos(B*(B**2 - R + b**2)/(b*(B + R))) - 2*pi
