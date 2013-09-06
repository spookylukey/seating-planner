#!/usr/bin/env python

# Credit to:
#
# http://www.improbable.com/news/2012/Optimal-seating-chart.pdf
# https://github.com/perrygeo/python-simulated-annealing

from __future__ import division

import math
import random

from anneal import Annealer

connection_matrix = """
1 50 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
50 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
1 1 1 50 1 1 1 1 10 0 0 0 0 0 0 0 0
1 1 50 1 1 1 1 1 1 0 0 0 0 0 0 0 0
1 1 1 1 1 50 1 1 1 0 0 0 0 0 0 0 0
1 1 1 1 50 1 1 1 1 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 50 1 0 0 0 0 0 0 0 0
1 1 1 1 1 1 50 1 1 0 0 0 0 0 0 0 0
1 1 10 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 50 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 50 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
"""
EXAMPLE_CONNECTIONS = [map(int, l.strip().split(" ")) for l in connection_matrix.strip().split("\n")]

EXAMPLE_NAMES = """
Deb
John
Martha
Travis
Allan
Lois
Jayne
Brad
Abby
Mary
Lee
Annika
Carl
Colin
Shirley
DeAnn
Lori
""".strip().split("\n")


#### Plans and Tables ####

# A Plan is a list of Tables.
# A Table is a list of integers representing people


def seated_together(plan, table_num, j, k):
    t = plan[table_num]
    return int(j in t and k in t)


def move(plan):
    # This modifies the plan in place.

    # Swap two people on two tables
    t1 = plan.pop(random.randrange(0, len(plan)))
    t2 = plan.pop(random.randrange(0, len(plan)))

    p1 = t1.pop(random.randrange(0, len(t1)))
    p2 = t2.pop(random.randrange(0, len(t2)))

    t1.append(p2)
    t2.append(p1)

    plan.append(t1)
    plan.append(t2)

    if p1 == -1 and p2 == -1:
        # We just swapped two empty seats. Try again:
        move(plan)


def normalise_plan(plan):
    return sorted([sorted(table, key=lambda p: p['name']) for table in plan],
                  key=lambda t: t[0]['name'])


def empty(table):
    return all(p == -1 for p in table)

### People who are coming, and information about connections

MAX_CONNECTION = 50

CONSERVE_TABLE_COEFFICIENT = 50

class PlanningData(object):
    def __init__(self, names, connections, table_size, table_count):
        self.NAMES = names
        self.CONNECTIONS = connections
        for row in connections:
            for col in row:
                assert col <= MAX_CONNECTION

        self.TABLE_SIZE = table_size
        self.PEOPLE_COUNT = len(names)
        self.TABLE_COUNT = table_count
        # Just need a value that is big enough to keep energy always positive
        self.MAX_ENERGY = MAX_CONNECTION * self.TABLE_COUNT * self.PEOPLE_COUNT**2


    def get_initial_plan(self):
        people = range(0, self.PEOPLE_COUNT)
        random.shuffle(people)

        # We need extra items, to represent spare places.  This allows us the
        # flexibility to have different sized tables.  To avoid fruitless
        # searches, we put them at the end *after* shuffling, and group such
        # that we get empty tables at the end.
        total_places = self.TABLE_SIZE * self.TABLE_COUNT

        people.extend([-1] * (total_places - len(people)))

        s = self.TABLE_SIZE
        c = self.TABLE_COUNT
        return [people[i*s:(i+1)*s] for i in range(c)]

    def energy(self, plan):
        val = sum(
            self.CONNECTIONS[j][k] * seated_together(plan, table_num, j, k)
            for table_num in range(0, self.TABLE_COUNT)
            for j in range(0, self.PEOPLE_COUNT - 1)
            for k in range(j, self.PEOPLE_COUNT)
            )


        # Better score if fewer tables used (for more friendliness even with
        # strangers). If table_size and table_count are chosen better this
        # isn't necessary.
        val += len([t for t in plan if empty(t)]) * CONSERVE_TABLE_COEFFICIENT * self.PEOPLE_COUNT

        # Negative, because annealing module finds minimum
        return self.MAX_ENERGY - val

    def plan_to_people(self, plan):
        return [[
                dict(name=self.NAMES[p],
                     friends=sum(1 if self.CONNECTIONS[p][k] > 0 else 0
                                 for k in table if k != p and k != -1)
                     )
                for p in table
                if p != -1]
                    for table in plan]



def solve(names, connections, table_size, table_count,
          annealing_time=6,
          exploration_steps=100,
          ):
    planning_data = PlanningData(names, connections, table_size, table_count)
    state = planning_data.get_initial_plan()
    annealer = Annealer(planning_data.energy, move)
    schedule = annealer.auto(state, seconds=annealing_time, steps=exploration_steps)
    state, e = annealer.anneal(state,
                               schedule['tmax'], schedule['tmin'],
                               schedule['steps'], updates=6)

    # Remove empty tables:
    state = [t for t in state if not empty(t)]
    return planning_data, state


if __name__ == '__main__':
    planning_data, plan = solve(EXAMPLE_NAMES, EXAMPLE_CONNECTIONS, 9, 2)
    print normalise_plan(planning_data.plan_to_people(plan))
