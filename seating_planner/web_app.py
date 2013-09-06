#!/usr/bin/env python

import re

from flask import Flask, jsonify, render_template, request, Response

from seating_planner.solver import solve, normalise_plan

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def error(message):
    return jsonify({'error': message})


@app.route('/find-solution/', methods=['POST'])
def find_solution():

    # Parse data:
    connections = request.form.get('connections', "")
    table_size = request.form.get('tableSize', 0, type=int)
    table_count = request.form.get('tableCount', 0, type=int)
    annealing_time = request.form.get('annealingTime', 0, type=int)
    exploration_steps = request.form.get('explorationSteps', 0, type=int)
    rows = connections.strip("\n").split("\n")
    d = []
    for row in rows:
        d.append(row.split(","))

    # Manipulate into stuff we need:

    # Get names:
    names = d[0][:]
    names.pop(0)

    # Remove names
    d.pop(0)
    for row in d:
        row.pop(0)

    # Convert to ints
    matrix = []
    for r, row in enumerate(d):
        line = []
        for c, item in enumerate(row):
            item = item.strip()
            if item == "":
                item = 0
            else:
                try:
                    item = int(item)
                except ValueError:
                    return error("Data at row %s, column %s is not an integer"
                                 % (r + 1, c + 1))

            line.append(item)
        matrix.append(line)

    # Solve
    try:
        planning_data, plan = solve(names, matrix, table_size, table_count,
                                    annealing_time=annealing_time,
                                    exploration_steps=exploration_steps,
                                    )
    except Exception as e:
        return error("An error occurred trying to solve this matrix")

    return jsonify({'solution': normalise_plan(planning_data.plan_to_people(plan))})



# Download and upload are just echoing back data that is there client side,
# but this mechanism allows us to make use of:
#
# * file selection and upload in the browser
# * automatic saving of downloads in most browsers (using Content-Disposition)


@app.route('/download-form/')
def download_form():
    return render_template('download_iframe.html')


@app.route('/download-file/', methods=['POST'])
def download_file():
    filename = request.form.get('filename', '')
    re.subn("[^a-zA-Z0-9._]", "", filename)
    if not filename:
        filename = "file.txt"
    response = Response(mimetype="text/plain",
                        headers=[("Content-Disposition", "attachment; filename=%s" % filename),
                                 ])
    response.set_data(request.form.get('data'))
    return response


@app.route('/upload-connections/', methods=['POST'])
def upload_connections():
    response = Response(mimetype="text/plain")
    response.set_data(request.data)
    return response


if __name__ == '__main__':
    app.run(debug=True)
