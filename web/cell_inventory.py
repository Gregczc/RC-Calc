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


from flask import Blueprint, render_template
import io
import sqlite3


def open_database():
    # Needs to be redone

    # Open the database
    conn = sqlite3.connect('../db/RC-Calc.db')

    # Creating the flight-time table if it does not exists
    conn.execute('''CREATE TABLE IF NOT EXISTS cell_table
                 (name text, voltage real, energy real, weight real, max_current real, price real)''')

    # Save changes
    conn.commit()

    html = io.open("./py/web/html/cell-inventory.html", "r", encoding="utf-8").read()

    # Closing database
    conn.close()


cell_inventory = Blueprint('cell-inventory', __name__)


@cell_inventory.route('/')
def show():
    return render_template('cell-inventory.html')
