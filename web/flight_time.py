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


import io
from flask import Blueprint


def new_entry_form(plane):

    return """
            <div class="card">
                <div class="card-header text-center">New Entry</div>
                <div class="card-body">
                    <form class="form-group row" method="POST" action="" novalidate>
                    <div class="form-group text-center">
                        <label for="formFlightNumber-""" + plane + """">#</label>
                        <input type="text" class="form-control form-control-sm formFlightNumber" id="formFlightNumber-""" + plane + """" placeholder="1" readonly name="formFlightNumber-""" + plane + """">
                    </div>

                    <div class="form-group text-center">
                        <label for="formFlightTime-""" + plane + """">Flight Time</label>
                        <div class="input-group input-group-sm">
                            <input type="time" class="form-control formFlightTime" id="formFlightTime-""" + plane + """" name="formFlightTime-""" + plane + """">
                            <div class="invalid-tooltip">Please enter the flight time.</div>
                        </div>
                    </div>

                    <div class="form-group text-center">
                        <label for="formDistance-""" + plane + """">Distance</label>
                        <div class="input-group input-group-sm">
                            <input type="number" step="0.1" min="0" class="form-control formDistance" id="formDistance-""" + plane + """" placeholder="45.4" name="formDistance-""" + plane + """">
                            <div class="input-group-append">
                               <span class="input-group-text">km</span>
                            </div>
                            <div class="invalid-tooltip">Please enter the distance flown.</div>
                        </div>
                    </div>

                    <div class="form-group text-center">
                        <label for="formEnergy-""" + plane + """">Energy</label>
                        <div class="input-group input-group-sm">
                            <input type="number" step="0.1" min="0" class="form-control formEnergy" id="formEnergy-""" + plane + """" placeholder="53.2" name="formEnergy-""" + plane + """">
                            <div class="input-group-append">
                               <span class="input-group-text">Wh</span>
                            </div>
                            <div class="invalid-tooltip">Please enter the energy used.</div>
                        </div>
                    </div>

                    <div class="form-group text-center">
                        <label for="formBattery-""" + plane + """">Battery</label>
                        <div class="input-group input-group-sm">
                            <input type="number" step="0.1" min="0" class="form-control formBattery" id="formBattery-""" + plane + """" placeholder="125.2" name="formBattery-""" + plane + """">
                            <div class="input-group-append">
                                <div class="input-group-text">Wh</div>
                            </div>
                            <div class="invalid-tooltip">Please enter the battery energy.</div>
                        </div>
                    </div>

                    <div class="form-group text-center">
                        <label for="formDescription-""" + plane + """">Description </label>
                        <div class="input-group input-group-sm">
                            <textarea class="form-control formDescription" id="formDescription-""" + plane + """" placeholder="eg. With 12x6 propeller, without wind, pretty aggressive flight etc." name="formDescription-""" + plane + """"></textarea>
                            <div class="invalid-tooltip">Please enter a description.</div>
                        </div>
                    </div>

                    <div class="form-group text-center">
                        <label for="formSave-""" + plane + """" class="invisible">Save</label>
                        <div class="input-group">
                            <button type="submit" class="btn btn-primary btn-sm form-control-sm text-bottom formSave" id="formSave-""" + plane + """" name="formSave-""" + plane + """" value="clicked">Save</button>
                        </div>
                    </div>
                    </form>
                </div>
            </div>
            """


flight_time = Blueprint('flight-time', __name__)


@flight_time.route('/')
def show():
    # Getting the usual content of flight-time.html as a string
    html = io.open("./web/templates/flight-time.html", "r", encoding="utf-8").read()

    plane_list = ["Skyhunter", "S800", "Easystar"]

    for number, plane in enumerate(plane_list):
        tab_header = "<a class=\"nav-item nav-link "
        tab_header += "active\"" if not number else "\""
        tab_header += (" id=\"nav-" + plane + "-tab\" data-toggle=\"tab\" href=\"#nav-"
                       + plane + "\" role=\"tab\" aria-controls=\"nav-")
        tab_header += plane + "\" aria-selected=\""
        tab_header += "true" if not number else "false"
        tab_header += "\">" + plane + "</a>\n\t\t\t\t\t<!-- Plane tab header marker -->"

        html = html.replace("""<!-- Plane tab header marker -->""", tab_header)

        tab_content = "<div class=\"tab-pane fade show "
        tab_content += "active\"" if not number else "\""
        tab_content += " id=\"nav-" + plane + "\" role=\"tabpanel\" aria-labelledby=\"nav-" + plane + "-tab\">"
        tab_content += new_entry_form(plane) + "</div>\n\t\t\t\t<!-- Plane tab content marker -->"

        html = html.replace("""<!-- Plane tab content marker -->""", tab_content)

    return html
