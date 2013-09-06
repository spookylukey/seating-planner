Seating planner
===============

This app attempts to solve the problem of seating a group of guests at a wedding
(or other occasion) so that everyone knows people on their table.

The approach taken involves:

* Using a connection matrix that defines the strength of connections between all
  the guests, and using that to score a given arrangement. Credit for this goes to
  Meghan L. Bellows and J. D. Luc Peterson2

  http://www.improbable.com/news/2012/Optimal-seating-chart.pdf

* Using simmulated annealing to attempt to find a good solution.

  The code for this comes from https://github.com/perrygeo/python-simulated-annealing


seating_planner/solver.py contains the main entry point for the algorithm

seating_planner/web_app.py contains a Flask web app as a UI, including a
relatively nice interface for entering the connection matrix.

Installation and running
------------------------

Preferably in a virtualenv:

* Add the current directory to the Python path

* $ pip install -r requirements.txt

* ./seating_planner/web_app.py

Access on localhost:5000

It can be run under PyPy for significant speedups (about 5-10x)

It can de deployed using any WSGI container e.g. gunicorn:

$ gunicorn  -b 127.0.0.1:12345 -D -w 4 seating_planner.web_app:app


License
-------

seating_planner/anneal.py has its own copyright licence.

Other code is put into the public domain.
