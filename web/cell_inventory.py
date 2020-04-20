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

import os
from flask import Blueprint, render_template, request
from collections import OrderedDict
import json

cell_inventory = Blueprint('cell-inventory', __name__)


def get_json(file):
    try:
        f = open(file, 'r+', encoding="utf-8")
        json_cells = json.loads(f.read(), object_pairs_hook=OrderedDict)
        f.close()
        return json_cells

    except IOError as e:
        print(e)
        return None


def update_json(file, content):
    try:
        # Clearing the json file
        open(file, 'w').close()

        # Updating the json file
        f = open(file, 'r+', encoding="utf-8")
        f.write(content)
        f.close()

    except IOError as e:
        print(e)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ["pdf"]


def add_cell(request):

    status = "successAdded"
    print(request.files)

    if request.files['Data-sheet'].filename != "":
        try:
            if allowed_file(request.files['Data-sheet'].filename):
                # Using io since I can't figure why request.files['Data-sheet'].save([...]) throws an Errno 13
                f = open('web/static/datasheets/' + request.form['Name'] + ".pdf", "wb+")
                f.write(request.files['Data-sheet'].read())
                f.close()
                has_datasheet = True

            else:
                has_datasheet = False
                print("Unauthorized file name / type.")
                status = "datasheet"

        except IOError as e:
            print(e)
            has_datasheet = False
            status = "datasheet"
    else:
        has_datasheet = False
    # Not very elegant, but to ensure that the data are written in the json in a consistent order
    # to make it easier to read by a human
    cell_dict = OrderedDict([
        ('Name', request.form['Name']),
        ('Voltage', request.form['Voltage']),
        ('Energy', request.form['Energy']),
        ('Capacity', request.form['Capacity']),
        ('Max Current', request.form['Max Current']),
        ('Weight', request.form['Weight']),
        ('Price', request.form['Price'] + request.form['Currency']),
        ('Data-sheet', has_datasheet)
    ])

    json_cells = get_json('web/static/json/cells.json')

    if request.form['Name'] in [cell['Name'] for cell in json_cells]:
        status = "alreadyExisting"
    else:
        # Adding the new cell
        json_cells.append(cell_dict)

    update_json('web/static/json/cells.json', json.dumps(json_cells, indent=2, ensure_ascii=False))

    json_cells.append({'Status': status})

    return json.dumps(json_cells)


def delete_cell(name):
    status = "errorDeleted"

    json_cells = get_json('web/static/json/cells.json')

    for cell in json_cells:
        if name == cell['Name']:
            if cell['Data-sheet']:
                try:
                    os.remove('web/static/datasheets/' + name + ".pdf")
                except IOError as e:
                    print(e)

            json_cells.remove(cell)
            status = 'successDeleted'
            break

    update_json('web/static/json/cells.json', json.dumps(json_cells, indent=2, ensure_ascii=False))

    json_cells.append({'Status': status})

    return json.dumps(json_cells)


def edit_cell(request):
    print(request.files)
    status = "successUpdated"

    json_cells = get_json('web/static/json/cells.json')

    for cell in json_cells:
        if request.form['InitialName'] == cell['Name']:
            json_cells.remove(cell)
            break

    if request.form['Name'] in [cell['Name'] for cell in json_cells]:
        # sending back the previous tab
        status = "alreadyExisting"
        json_cells = get_json('web/static/json/cells.json')
        json_cells.append({'Status': status})
        return json.dumps(json_cells)

    else:
        if request.form['HadDatasheet'] == 'true' and request.form['DatasheetAction'] == "delete":
            try:
                os.remove('web/static/datasheets/' + request.form['InitialName'] + ".pdf")
                has_datasheet = False
            except IOError as e:
                print(e)
                status = "errorUpdated"

        elif request.form['HadDatasheet'] == 'true' and request.form['DatasheetAction'] == "none":
            try:
                os.rename('web/static/datasheets/' + request.form['InitialName'] + ".pdf", 'web/static/datasheets/' + request.form['Name'] + ".pdf")
                has_datasheet = True
            except IOError as e:
                print(e)
                status = "errorUpdated"

        elif request.form['DatasheetAction'] == "add":
            try:
                if request.form['HadDatasheet'] == 'true':
                    os.remove('web/static/datasheets/' + request.form['InitialName'] + ".pdf")

                if allowed_file(request.files['Data-sheet'].filename):
                    # Using io since I can't figure why request.files['Data-sheet'].save([...]) throws an Errno 13
                    f = open('web/static/datasheets/' + request.form['Name'] + ".pdf", "wb+")
                    f.write(request.files['Data-sheet'].read())
                    f.close()
                    has_datasheet = True
                else:
                    has_datasheet = False
                    status = "errorUpdated"
            except IOError as e:
                print(e)
                status = "errorUpdated"

        else:
            has_datasheet = False

        cell_dict = OrderedDict([
            ('Name', request.form['Name']),
            ('Voltage', request.form['Voltage']),
            ('Energy', request.form['Energy']),
            ('Capacity', request.form['Capacity']),
            ('Max Current', request.form['Max Current']),
            ('Weight', request.form['Weight']),
            ('Price', request.form['Price'] + request.form['Currency']),
            ('Data-sheet', has_datasheet)
        ])

        json_cells.append(cell_dict)

        update_json('web/static/json/cells.json', json.dumps(json_cells, indent=2, ensure_ascii=False))

        json_cells.append({'Status': status})

        return json.dumps(json_cells)


@cell_inventory.route('/', methods=['GET', 'POST'])
def show():
    print(request.form)
    if request.method == 'POST' and 'Type' in request.form:
        if request.form['Type'] == 'add':
            return add_cell(request)

        elif request.form['Type'] == 'edit':
            return edit_cell(request)

        elif request.form['Type'] == 'delete':
            return delete_cell(request.form['Name'])

        else:
            return render_template('cell-inventory.html')

    else:
        return render_template('cell-inventory.html')

