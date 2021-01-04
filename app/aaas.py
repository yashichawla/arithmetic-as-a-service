from utils import *
from flask import Flask
from multiprocessing import Value

COUNTER = Value("i", 0)

app = Flask(__name__)


'''def sortOrder():
    pass
'''


def getFunctionReference():
    pass


@app.route("/", methods=["GET"])
def home(*vargs):
    s = f'''Hello there stranger! It seems you do not know how to use my AaaS. 
    There are currently {COUNTER.value} clients successfully using my AaaS for their apps.
    To learn more about my AaaS, visit https://github.com/aditeyabaral/arithmetic-as-a-service'''
    return s, 200


@app.route("/add/<path:vargs>", methods=["GET"])
def add(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = addition(numbers)
    return result


@app.route("/sub/<path:vargs>", methods=["GET"])
def sub(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = subtraction(numbers)
    return result


@app.route("/mul/<path:vargs>", methods=["GET"])
def mul(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = multiplication(numbers)
    return result


@app.route("/div/<path:vargs>", methods=["GET"])
def div(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = division(numbers)
    return result


@app.route("/sin/<path:vargs>", methods=["GET"])
def sin(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = sine(numbers)
    return result


@app.route("/cos/<path:vargs>", methods=["GET"])
def cos(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = cosine(numbers)
    return result


@app.route("/tan/<path:vargs>", methods=["GET"])
def tan(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = tangent(numbers)
    return result


@app.route("/fact/<path:vargs>", methods=["GET"])
def fact(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = factorial(numbers)
    return result


'''@app.route("/sort/<path:vargs>", methods=["GET"])
def sortIncreasingOrder(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = sortNumbers(numbers)
    return result'''


@app.route("/sort/inc/<path:vargs>", methods=["GET"])
def sortIncreasingOrder(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = sortNumbers(numbers)
    return result


@app.route("/sort/dec/<path:vargs>", methods=["GET"])
def sortDecreasingOrder(vargs):
    incrementCounter(COUNTER)
    numbers = vargs.split("/")
    result = sortNumbers(numbers, reverse=True)
    return result


if __name__ == "__main__":
    app.run()
