import json
import numpy as np
from multiprocessing import Value

COUNTER = Value("i", 0)


def incrementCounter():
    with COUNTER.get_lock():
        COUNTER.value += 1


def getFunctionResult(function, vargs, **flags):
    incrementCounter()
    numbers = vargs.split("/")
    try:
        if not flags:
            result = function(numbers)
        else:
            if function is sortNumbers:
                result = function(numbers, reverse=flags["reverse"])
        result = json.dumps(result)
        return result, 200
    except Exception as e:
        print(str(e))   # should I return this?
        return "Bad request", 400


def addition(numbers):
    result = float(numbers[0])
    for num in numbers[1:]:
        result += float(num)
    return result


def subtraction(numbers):
    result = float(numbers[0])
    for num in numbers[1:]:
        result -= float(num)
    return result


def multiplication(numbers):
    result = float(numbers[0])
    for num in numbers[1:]:
        result *= float(num)
    return result


def division(numbers):
    result = float(numbers[0])
    for num in numbers[1:]:
        result /= float(num)
    return result


def sine(numbers):
    result = list()
    for num in numbers:
        result.append(np.sin(float(num)))

    if len(result) == 1:
        return result[0]
    else:
        return result


def cosine(numbers):
    result = list()
    for num in numbers:
        result.append(np.cos(float(num)))

    if len(result) == 1:
        return result[0]
    else:
        return result


def tangent(numbers):
    result = list()
    for num in numbers:
        result.append(np.tan(float(num)))

    if len(result) == 1:
        return result[0]
    else:
        return result


def factorial(numbers):
    result = list()
    for num in numbers:
        result.append(np.factorial(int(num)))

    if len(result) == 1:
        return result[0]
    else:
        return result


def sortNumbers(numbers, reverse=False):
    numbers = list(map(float, numbers))
    result = sorted(numbers, reverse=reverse)
    return result


def sortNumbersIncreasing(numbers):
    result = sortNumbers(numbers)
    return result


def sortNumbersDecreasing(numbers):
    result = sortNumbers(numbers, reverse=True)
    return result


def getMatrices(numbers):  # url/nmatrices/ndims/dim1/.../dimn/num1...
    numbers = list(map(float, numbers))
    nmatrices = int(numbers[0])
    ndims = int(numbers[1])
    dims = [int(numbers[i]) for i in range(2, 2+ndims)]
    matrix_values = np.split(np.asarray(numbers[2+ndims:]), nmatrices)
    matrices = [np.reshape(m, dims).tolist() for m in matrix_values]

    if nmatrices == 1:
        return matrices[0]
    else:
        return matrices


def addMatrices(numbers):
    matrices = getMatrices(numbers)
    result = np.add(*matrices).tolist()
    return result


def subtractMatrices(numbers):
    matrices = getMatrices(numbers)
    result = np.subtract(*matrices).tolist()
    return result