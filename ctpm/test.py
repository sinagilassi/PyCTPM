
import numpy as np
from scipy.optimize import fsolve
import matplotlib as mpl
import matplotlib.pyplot as plt
from core.utilities import roundNum, removeDuplicatesList


a = (1, 2, 3)


def showMe(*data):
    a, b, c = data[0]
    print(data, a, b, c)


# showMe(a)


def fZ(x, *data):
    print(data)
    alpha, beta, gamma = data
    print(f"alpha: {alpha} | beta: {beta} | gamma: {gamma}")
    fZSet = np.power(x, 3) + alpha*np.power(x, 2) + beta*x + gamma
    return fZSet


data = (1.0, 2.0, 3.0)
x0 = [1]
# res = fsolve(fZ, x0, args=data)
# print(res)

# x = np.linspace(0, 10, 5)


# def ft(x):
#     print(data)
#     alpha, beta, gamma = (1, 2, 3)
#     print(f"alpha: {alpha} | beta: {beta} | gamma: {gamma}")
#     fZSet = np.power(x, 3) + alpha*np.power(x, 2) + beta*x + gamma
#     return fZSet


# plt.plot(x, ft)

# zGuess = np.linspace(0, 2, 11)
zGuess = np.array([0.015, 0.235, 0.112])
z2 = 10.54875
print(zGuess)
z = roundNum(z2, 2)
print(z)

z0 = [1, 2, 2, 3]
z01 = removeDuplicatesList(z0)
print(z01)
