#!/usr/bin/env python

from flask import Flask, jsonify, render_template, request

from seating_planner import solve, normalise_plan

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
    planning_data, plan = solve(names, matrix, table_size, table_count,
                                annealing_time=annealing_time,
                                exploration_steps=exploration_steps,
                                )

    return jsonify({'solution': normalise_plan(planning_data.plan_to_people(plan))})

if __name__ == '__main__':
    app.run(debug=True)
