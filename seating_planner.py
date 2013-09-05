#!/usr/bin/env python

# Credit to:
#
# http://www.improbable.com/news/2012/Optimal-seating-chart.pdf
# https://github.com/perrygeo/python-simulated-annealing

from __future__ import division

import math
import random

import anneal

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
    t1 = Table(p for p in t1 if p != p1) + Table([p2])
    t2 = Table(p for p in t2 if p != p2) + Table([p1])
    plan.append(t1)
    plan.append(t2)
    return plan


def normalise_plan(plan):
    return sorted(Table(sorted(table)) for table in plan)


### People who are coming, and information about connections

MAX_CONNECTION = 50

class PlanningData(object):
    def __init__(self, names, connections, table_size):
        self.NAMES = names
        self.CONNECTIONS = connections
        for row in connections:
            for col in row:
                assert col <= MAX_CONNECTION

        self.TABLE_SIZE = table_size
        self.PEOPLE_COUNT = len(names)
        self.TABLE_COUNT = int(math.ceil(self.PEOPLE_COUNT/self.TABLE_SIZE))
        # Just need a value that is big enough to keep energy always positive
        self.MAX_ENERGY = MAX_CONNECTION * self.TABLE_COUNT * self.PEOPLE_COUNT**2


    def get_initial_plan(self):
        people = range(0, self.PEOPLE_COUNT)
        random.shuffle(people)
        return Plan(Table(people[i::self.TABLE_COUNT]) for i in range(self.TABLE_COUNT))

    def energy(self, plan):
        val = sum(
            self.CONNECTIONS[j][k] * seated_together(plan, table_num, j, k)
            for table_num in range(0, self.TABLE_COUNT)
            for j in range(0, self.PEOPLE_COUNT - 1)
            for k in range(j, self.PEOPLE_COUNT)
            )
        # Negative, because annealing module finds minimum
        return self.MAX_ENERGY - val

    def plan_to_names(self, plan):
        return Plan(Table(self.NAMES[p] for p in table)
                    for table in plan)



example = PlanningData(
    EXAMPLE_NAMES,
    EXAMPLE_CONNECTIONS,
    4,
)
state = example.get_initial_plan()

from anneal import Annealer
annealer = Annealer(example.energy, move)
schedule = annealer.auto(state, minutes=0.1, steps=100)
state, e = annealer.anneal(state,
                           schedule['tmax'], schedule['tmin'],
                           schedule['steps'], updates=6)

print normalise_plan(example.plan_to_names(state))
