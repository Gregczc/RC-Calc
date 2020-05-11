# coding: utf-8

# RC-Calc: An all-in-one R/C & FPV flying stuff calculator
# Copyright (C) 2020 Grégoire CAHUZAC <gregoire.cahuzac@outlook.fr>
# This file is part of RC-Calc. <https://github.com/Gregczc/RC-Calc>

# RC-Calc is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.

# RC-Calc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with RC-Calc.  If not, see <http://www.gnu.org/licenses/>.


from flask import Blueprint, render_template, request
import sqlite3
import json


def initialize_db():
    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute('''CREATE TABLE IF NOT EXISTS Cells ( name text,
                                                    voltage_min real,
                                                    voltage_nom real,
                                                    voltage_max real,
                                                    energy real,
                                                    capacity real,
                                                    max_current real,
                                                    weight real,
                                                    price real,
                                                    currency text,
                                                    datasheet blob,
                                                    cell_id INTEGER PRIMARY KEY)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Batteries (
                name text,
                s integer,
                p integer,
                add_weight real,
                cells INTEGER REFERENCES Cells(cell_id) ON UPDATE CASCADE ON DELETE CASCADE)''')

    # Save (commit) the changes
    conn.commit()
    conn.close()


def get_cells_and_batteries(status='ok'):
    initialize_db()

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    cells = []
    for cell in c.execute("SELECT * FROM Cells"):
        cells.append({
            'Name':         cell[0],
            'Voltage Min':  cell[1],
            'Voltage Nom':  cell[2],
            'Voltage Max':  cell[3],
            'Energy':       cell[4],
            'Capacity':     cell[5],
            'Max Current':  cell[6],
            'Weight':       cell[7],
            'Price':        cell[8],
            'Currency':     cell[9],
            'Data-sheet':   False if cell[10] == b"0" else True
        })

    cellID2Name = dict(c.execute("SELECT cell_id, name FROM Cells").fetchall())
    batteries = []
    for battery in c.execute("SELECT * FROM Batteries"):
        batteries.append({
            'Name': battery[0],
            'S': battery[1],
            'P': battery[2],
            'AddWeight': battery[3],
            'Cells': cellID2Name[battery[4]]
        })

    conn.commit()
    conn.close()

    return json.dumps({'cells': cells, 'batteries': batteries, 'Status': status})


battery_comparator = Blueprint('battery-comparator', __name__)


@battery_comparator.route('/')
def show():
    if request.method == 'GET' and request.args.get('Type') == 'get_cells_and_batteries':
        return get_cells_and_batteries()
    else:
        return render_template('battery-comparator.html')
