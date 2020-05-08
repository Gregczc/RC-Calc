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
import json
import sqlite3

cell_inventory = Blueprint('cell-inventory', __name__)


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
    # Save (commit) the changes
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ["pdf"]


def get_cells(status='ok'):

    initialize_db()

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    json_cells = []
    for cell in c.execute("SELECT * FROM Cells"):
        json_cells.append({
            'Name': cell[0],
            'Voltage': cell[1],
            'Energy': cell[2],
            'Capacity': cell[3],
            'Max Current': cell[4],
            'Weight': cell[5],
            'Price': cell[6],
            'Data-sheet': False if cell[7] == b"0" else True
        })

    conn.commit()
    conn.close()

    json_cells.append({'Status': status})

    return json.dumps(json_cells)


def get_datasheet(name):

    initialize_db()

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    for cell in c.execute("SELECT datasheet FROM Cells WHERE name = ?", (name,)):
        datasheet = cell[0]

    conn.commit()
    conn.close()

    return datasheet


def add_cell(request):

    datasheet_error = False

    print(request.files)

    if request.files['Data-sheet'].filename != "":
        if allowed_file(request.files['Data-sheet'].filename):

            blob = sqlite3.Binary(request.files['Data-sheet'].read())

        else:
            blob = sqlite3.Binary(b"0")
            print("Unauthorized file name / type.")
            datasheet_error = True

    else:
        blob = sqlite3.Binary(b"0")

    cell = (request.form['Name'], request.form['Voltage'], request.form['Energy'], request.form['Capacity'],
            request.form['Max Current'], request.form['Weight'], request.form['Price'] + request.form['Currency'],
            blob.tobytes(), None)

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("SELECT COUNT(*) FROM Cells WHERE name = ?", (request.form['Name'],))
    if c.fetchall()[0][0] != 0:
        conn.close()
        status = "alreadyExisting"

    else:
        # Insert a row of data
        c.execute("INSERT INTO Cells VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", cell)

        # Save (commit) the changes
        conn.commit()
        conn.close()

        status = "successAdded" if not datasheet_error else "datasheet"

    return get_cells(status)


def delete_cell(name):

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DELETE FROM Cells WHERE name = ?", (name,))

    c.execute("SELECT COUNT(*) FROM Cells WHERE name = ?", (name,))
    if c.fetchall()[0][0] != 0:
        status = "errorDeleted"
    else:
        status = "successDeleted"

    conn.commit()
    conn.close()

    return get_cells(status)


def edit_cell(request):
    datasheet_error = False

    conn = sqlite3.connect('db/user.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    if request.form['DatasheetAction'] == "delete":
        update = (sqlite3.Binary(b"0").tobytes(), request.form['InitialName'])
        c.execute('''UPDATE Cells SET datasheet = ? WHERE name = ?''', update)

    elif request.form['DatasheetAction'] == "add":
        if request.files['Data-sheet'].filename != "":
            if allowed_file(request.files['Data-sheet'].filename):
                blob = sqlite3.Binary(request.files['Data-sheet'].read())

            else:
                blob = sqlite3.Binary(b"0")
                print("Unauthorized file name / type.")
                datasheet_error = True

        else:
            blob = sqlite3.Binary(b"0")

        update = (blob.tobytes(), request.form['InitialName'])
        c.execute('''UPDATE Cells SET datasheet = ? WHERE name = ?''', update)

    new_cell = c.execute("SELECT * FROM Cells WHERE name = ?", (request.form['Name'],)).fetchall()
    initial_cell = c.execute("SELECT * FROM Cells WHERE name = ?", (request.form['InitialName'],)).fetchall()

    if len(new_cell) != 0 and new_cell != initial_cell:
        status = "alreadyExisting"

    else:
        update = (request.form['Name'], request.form['Voltage'], request.form['Energy'], request.form['Capacity'],
                  request.form['Max Current'], request.form['Weight'], request.form['Price'] + request.form['Currency'],
                  request.form['InitialName'])

        c.execute('''UPDATE Cells SET name = ?, voltage = ?, energy = ?, capacity = ?, max_current = ?, weight = ?,
                price = ? WHERE name = ?''', update)
        status = "datasheet" if datasheet_error else "successUpdated"
        conn.commit()

    conn.close()

    return get_cells(status)


@cell_inventory.route('/', methods=['GET', 'POST'])
def show():
    print(request.form)
    if request.method == 'POST' and 'Type' in request.form:
        if request.form['Type'] == 'get_cells':
            return get_cells()

        elif request.form['Type'] == 'add':
            return add_cell(request)

        elif request.form['Type'] == 'edit':
            return edit_cell(request)

        elif request.form['Type'] == 'delete':
            return delete_cell(request.form['Name'])

        else:
            return render_template('cell-inventory.html')

    elif request.method == 'GET' and request.args.get('Type') == 'get_datasheet':
        return get_datasheet(request.args.get('Name'))

    else:
        return render_template('cell-inventory.html')
