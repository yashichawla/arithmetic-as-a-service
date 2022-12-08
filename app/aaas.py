import os
import dotenv
import pytz
import flask
from datetime import datetime
from flask import Flask, request, render_template
from flask_table import Table, Col
from utils import *
from db import LoggingDatabase

dotenv.load_dotenv()
IST = pytz.timezone("Asia/Kolkata")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

function_mapper = {
    "add": addition,
    "sub": subtraction,
    "mul": multiplication,
    "div": division,
    "sin": sine,
    "cos": cosine,
    "tan": tangent,
    "fact": factorialNumber,
    "exp": exponent,
    "log": logarithm,
    "ln": natural_log,
    "sort": sortNumbersIncreasing,
    "sort-inc": sortNumbersIncreasing,
    "sort-dec": sortNumbersDecreasing,
    "mat": getMatrices,
    "mat-add": addMatrices,
    "mat-sub": subtractMatrices,
    "diff": differentiateExpression,
    "int-def": integrateExpressionDefinite,
    "int-indef": integrateExpressionIndefinite,
    "limit": getLimit,
    "series": getSeries,
    "fourier": getFourierSeries,
}


class loggingInfoTable(Table):
    __id = Col("__id", show=False)
    time = Col("time")
    ip = Col("ip")
    browser = Col("browser")
    platform = Col("platform")
    site = Col("site")


def getFunctionCall(url):
    function_name = url.split("/")[3]
    function_reference = function_mapper[function_name]
    return function_name, function_reference


@app.route("/", methods=["GET"])
def home(*vargs):
    db.log("home", request)
    accesses = db.uniqueCount(start_time)
    print(accesses)
    total = db.getCount(start_time)
    result = f"""Hello stranger!<br/>
    It seems you do not know how to use my AaaS.<br/>
    My AaaS has been used by over {accesses} clients for their daily needs.
    In fact, a total of {total} requests have been made to my AaaS.<br/>
    What are you waiting for? Join all these developers and start useing my AaaS today!<br/>
    To learn more about my AaaS, visit https://github.com/aditeyabaral/arithmetic-as-a-service"""
    return result, 200


@app.route("/logging", methods=["GET"])
def getLogging(*vargs):
    result = db.getlogginginfo()
    table = loggingInfoTable(result)
    table.border = True
    return render_template("table.html", table=table), 200


@app.route("/add/<path:vargs>", methods=["GET"])
@app.route("/sub/<path:vargs>", methods=["GET"])
@app.route("/mul/<path:vargs>", methods=["GET"])
@app.route("/div/<path:vargs>", methods=["GET"])
@app.route("/sin/<path:vargs>", methods=["GET"])
@app.route("/cos/<path:vargs>", methods=["GET"])
@app.route("/tan/<path:vargs>", methods=["GET"])
@app.route("/fact/<path:vargs>", methods=["GET"])
@app.route("/exp/<path:vargs>", methods=["GET"])
@app.route("/log/<path:vargs>", methods=["GET"])
@app.route("/ln/<path:vargs>", methods=["GET"])
@app.route("/sort/<path:vargs>", methods=["GET"])
@app.route("/sort-inc/<path:vargs>", methods=["GET"])
@app.route("/sort-dec/<path:vargs>", methods=["GET"])
@app.route("/mat/<path:vargs>", methods=["GET"])
@app.route("/mat-add/<path:vargs>", methods=["GET"])
@app.route("/mat-sub/<path:vargs>", methods=["GET"])
@app.route("/diff/<path:vargs>", methods=["GET"])
@app.route("/int-def/<path:vargs>", methods=["GET"])
@app.route("/int-indef/<path:vargs>", methods=["GET"])
@app.route("/limit/<path:vargs>", methods=["GET"])
@app.route("/series/<path:vargs>", methods=["GET"])
@app.route("/fourier/<path:vargs>", methods=["GET"])
def call(vargs):
    function_name, function_reference = getFunctionCall(flask.request.base_url)
    db.log(function_name, request)
    return getFunctionResult(function_reference, vargs)


if __name__ == "__main__":
    db = LoggingDatabase()
    start_time = datetime.now(IST)
    app.run(host="0.0.0.0", port=5000)
