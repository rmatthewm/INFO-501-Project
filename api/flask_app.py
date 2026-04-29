# Return data pulled from the RentCast API so we do not need to make so many requests

from flask import Flask, request as req
from random import randint
import json

app = Flask(__name__)

@app.route('/')
def controls():
    return 'hello there' 

@app.route('/v1/listings/rental/long-term')
def api():
    pass


if __name__ == '__main__':
    app.run(port=8080)
