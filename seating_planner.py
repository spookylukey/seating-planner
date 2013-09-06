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
# A Table is a tuple of integers representing people

# We use tuples so that they are immutable, so that copying a whole plan is just
# shallow copying a list, without having to worry about substructures being
# modified by other copies.

Table = tuple
Plan = list


def seated_together(plan, table_num, j, k):
    t = plan[table_num]
    return int(j in t and k in t)


def move(plan):
    # This modifies the plan in place.

    # Swap two people on two tables
    t1 = random.choice(plan)
    plan.remove(t1)
    t2 = random.choice(plan)
    plan.remove(t2)
    p1 = random.choice(t1)
    p2 = random.choice(t2)

    t1 = list(t1)
    t1.remove(p1)
    t1.append(p2)
    t1 = Table(t1)

    t2 = list(t2)
    t2.remove(p2)
    t2.append(p1)
    t2 = Table(t2)

    plan.append(t1)
    plan.append(t2)
    return plan


def normalise_plan(plan):
    return sorted(Table(sorted(table)) for table in plan)


def empty(table):
    return all(p is None for p in table)

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

        people.extend([None] * (total_places - len(people)))

        s = self.TABLE_SIZE
        c = self.TABLE_COUNT
        return Plan(Table(people[i*s:(i+1)*s]) for i in range(c))

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

    def plan_to_names(self, plan):
        return Plan(Table(self.NAMES[p] for p in table
                          if p is not None)
                    for table in plan)



def solve(names, connections, table_size, table_count,
          annealing_time=6,
          exploration_steps=100,
          ):
    planning_data = PlanningData(names, connections, table_size, table_count)
    state = planning_data.get_initial_plan()
    annealer = Annealer(planning_data.energy, move)
    schedule = annealer.auto(state, minutes=annealing_time/60.0, steps=exploration_steps)
    state, e = annealer.anneal(state,
                               schedule['tmax'], schedule['tmin'],
                               schedule['steps'], updates=6)

    # Remove empty tables:
    state = [t for t in state if not empty(t)]
    return planning_data, state


if __name__ == '__main__':
    planning_data, plan = solve(EXAMPLE_NAMES, EXAMPLE_CONNECTIONS, 9, 2)
    print normalise_plan(planning_data.plan_to_names(plan))
