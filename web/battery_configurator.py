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
                                                    voltage real,
                                                    energy real,
                                                    capacity real,
                                                    max_current real,
                                                    weight real,
                                                    price text,
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
            'Name': cell[0],
            'Voltage': cell[1],
            'Energy': cell[2],
            'Capacity': cell[3],
            'Max Current': cell[4],
            'Weight': cell[5],
            'Price': cell[6],
            'Data-sheet': False if cell[7] == b"0" else True
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


def add_battery(request):

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    cell_id = c.execute("SELECT cell_id FROM Cells WHERE name = ?", (request.form['Cells'],)).fetchall()[0][0]

    battery = (request.form['Name'], request.form['S'], request.form['P'], request.form['AddWeight'], cell_id)

    c.execute("SELECT COUNT(*) FROM Batteries WHERE name = ?", (request.form['Name'],))
    if c.fetchall()[0][0] != 0:
        status = "alreadyExisting"

    else:
        c.execute("INSERT INTO Batteries VALUES (?, ?, ?, ?, ?)", battery)
        status = "successAdded"

    # Save (commit) the changes
    conn.commit()
    conn.close()

    return get_cells_and_batteries(status)


def delete_battery(name):

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DELETE FROM Batteries WHERE name = ?", (name,))

    c.execute("SELECT COUNT(*) FROM Batteries WHERE name = ?", (name,))
    if c.fetchall()[0][0] != 0:
        status = "errorDeleted"
    else:
        status = "successDeleted"

    conn.commit()
    conn.close()

    return get_cells_and_batteries(status)


def edit_battery(request):

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    cell_id = c.execute("SELECT cell_id FROM Cells WHERE name = ?", (request.form['Cells'],)).fetchall()[0][0]

    new_battery = c.execute("SELECT * FROM Batteries WHERE name = ?", (request.form['Name'],)).fetchall()
    initial_battery = c.execute("SELECT * FROM Batteries WHERE name = ?", (request.form['InitialName'],)).fetchall()

    if len(new_battery) != 0 and new_battery != initial_battery:
        status = "alreadyExisting"

    else:
        battery = (request.form['Name'],
                   request.form['S'],
                   request.form['P'],
                   request.form['AddWeight'],
                   cell_id,
                   request.form['InitialName'])

        c.execute('''UPDATE Batteries SET name = ?, s = ?, p = ?, add_weight = ?, cells = ? WHERE name = ?''', battery)
        status = "successUpdated"
        conn.commit()

    conn.close()

    return get_cells_and_batteries(status)


battery_configurator = Blueprint('battery-configurator', __name__)


@battery_configurator.route('/', methods=['GET', 'POST'])
def show():
    if request.method == 'GET' and request.args.get('Type') == 'get_cells_and_batteries':
        return get_cells_and_batteries()

    elif request.method == 'POST' and 'Type' in request.form:
        if request.form['Type'] == 'add':
            return add_battery(request)

        elif request.form['Type'] == 'edit':
            return edit_battery(request)

        elif request.form['Type'] == 'delete':
            return delete_battery(request.form['Name'])

        else:
            return render_template('battery-configurator.html')

    else:
        return render_template('battery-configurator.html')
