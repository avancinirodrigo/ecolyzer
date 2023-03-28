[![Build Status](https://travis-ci.com/avancinirodrigo/ecolyzer.svg?token=5ZEHUCMbsFiYovGrh5Hp&branch=master)](https://travis-ci.com/avancinirodrigo/ecolyzer)
[![codecov](https://codecov.io/gh/avancinirodrigo/ecolyzer/branch/master/graph/badge.svg?token=s6IQehSnnQ)](https://codecov.io/gh/avancinirodrigo/ecolyzer)
[![BCH compliance](https://bettercodehub.com/edge/badge/avancinirodrigo/ecolyzer?branch=master&token=6d8614cbef4cf7651e3c754b572d8e7fcee2f018)](https://bettercodehub.com/)

# Ecolyzer
Ecolyzer is a tool that aims to explore dependencies of software components from the point of view of software ecosystem, providing visualization of software involved and their relationships.

## Overview
[Software Visualization Tool for Evaluating API Usage in the Context of Software Ecosystems: A Proof of Concept](https://doi.org/10.1007/978-3-030-58817-5_26)

## Environment
* Ubuntu >= 18.04
* PostgreSQL >= 10
* Python >= 3.6

## How to Install
Suppose it has been downloaded to `~` (home/$USER/ecolyzer).
```bash
cd ~/ecolyzer
python3 -m venv venv
source ~/ecolyzer/venv/bin/activate
pip install -r requirements.txt
pip install -r flask_ecolyzer/requirements.txt
```
## How to Use
Run some script e.g.
```bash
cd ~/ecolyzer/scripts
export PYTHONPATH=~/ecolyzer
python ~/ecolyzer/scripts/jfreechart_ecosystem_top5.py
export FLASK_APP=~/ecolyzer/flask_ecolyzer/main.py
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jfreechart_ecosystem_top5
flask run
```
After that, open on browser: `http://127.0.0.1:5000`

See in [tests](https://github.com/avancinirodrigo/ecolyzer/tree/master/tests) and [scripts](https://github.com/avancinirodrigo/ecolyzer/tree/master/scripts) for more examples.

## How to Contribute
[Fork & Pull Request](https://docs.github.com/en/github/collaborating-with-pull-requests/getting-started/about-collaborative-development-models)

## Style Guide for Python Code
https://www.python.org/dev/peps/pep-0008

## Third Party Systems
* [PyDriller MSR](https://pydriller.readthedocs.io/en/latest)
* [GitPython](https://gitpython.readthedocs.io/en/stable/index.html)
* [SQLAlchemy ORM](https://www.sqlalchemy.org)
* [Flask](https://github.com/pallets/flask)
* [PyLuaParser](https://github.com/boolangery/py-lua-parser)
* [Javalang](https://github.com/c2nes/javalang)
