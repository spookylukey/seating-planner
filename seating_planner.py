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
MATRIX_DATA = [map(int, l.strip().split(" ")) for l in connection_matrix.strip().split("\n")]

NAMES = """
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
"""

NAMES = NAMES.strip().split("\n")

TABLE_SIZE = 9

PEOPLE_COUNT = len(NAMES)

TABLE_COUNT = int(math.ceil(PEOPLE_COUNT/TABLE_SIZE))

# A Plan is a list of Tables.
# A Table is a tuple of integers representing people

# We use tuples so that they are immutable, so that copying a whole plan is just
# shallow copying a list, without having to worry about substructures being
# modified by other copies.

Table = tuple
Plan = list

def normalise_plan(plan):
    return sorted(Table(sorted(table)) for table in plan)

def get_initial_plan():
    people = range(0, PEOPLE_COUNT)
    random.shuffle(people)
    return Plan(Table(people[i::TABLE_COUNT]) for i in range(TABLE_COUNT))

def plan_to_names(plan):
    return Plan(Table(NAMES[p] for p in table)
                for table in plan)


def connection(j, k):
    return MATRIX_DATA[j][k]

def seated_together(plan, table_num, j, k):
    t = plan[table_num]
    return int(j in t and k in t)


MAX_CONNECTION = 50
# Just need a value that is big enough to keep energy always positive
MAX_ENERGY = MAX_CONNECTION * TABLE_COUNT * PEOPLE_COUNT**2

def energy(plan):
    val = sum(
        connection(j, k) * seated_together(plan, table_num, j, k)
        for table_num in range(0, TABLE_COUNT)
        for j in range(0, PEOPLE_COUNT - 1)
        for k in range(j, PEOPLE_COUNT)
        )
    # Negative, because annealing module finds minimum
    return MAX_ENERGY - val

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

state = get_initial_plan()

from anneal import Annealer
annealer = Annealer(energy, move)
schedule = annealer.auto(state, minutes=0.1)
state, e = annealer.anneal(state,
                           schedule['tmax'], schedule['tmin'],
                           schedule['steps'], updates=6)

print normalise_plan(plan_to_names(state))
