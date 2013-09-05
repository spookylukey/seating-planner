#!/usr/bin/env python

import json

from flask import Flask, jsonify, render_template, request

from seating_planner import solve, normalise_plan

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find-solution/', methods=['POST'])
def find_solution():

    # Parse data:
    connections = request.form.get('connections', "")
    table_size = request.form.get('tableSize', 0, type=int)
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
    matrix = [map(int, row) for row in d]

    # Solve
    planning_data, plan = solve(names, matrix, table_size)

    return jsonify({'solution': normalise_plan(planning_data.plan_to_names(plan))})

if __name__ == '__main__':
    app.run(debug=True)
