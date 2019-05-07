
from flask import Flask
from flask import request
from lib import utils

from databases.face_demographics import face_demographics

import json
import databases as db

app = Flask(__name__)



@app.route("/data/venue/<venueId>/demographics", methods=["GET"])
def demographics(venueId):
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    s_timestamp = utils.date_to_timestamp(start_date)
    e_timestamp = utils.date_to_timestamp(end_date)
    fd = face_demographics()
    result = fd.get_summary_demographics(s_timestamp, e_timestamp, venueId)

    return json.dumps(
        {
        "success": "true",
        "data": result
        }
    )




@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port = int("5050"))