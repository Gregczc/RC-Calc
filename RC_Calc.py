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


import webbrowser
from flask import Flask
from web.battery_comparator import battery_comparator
from web.battery_configurator import battery_configurator
from web.cell_inventory import cell_inventory
from web.current_sensor import current_sensor
from web.exit import exit
from web.flight_time import flight_time
from web.flying_wing_design import flying_wing_design
from web.index import index
from web.motor import motor

app = Flask(__name__, static_folder="web/static", template_folder="web/templates", static_url_path='/static/')

app.register_blueprint(battery_comparator, url_prefix='/battery-comparator')
app.register_blueprint(battery_configurator, url_prefix='/battery-configurator')
app.register_blueprint(cell_inventory, url_prefix='/cell-inventory')
app.register_blueprint(current_sensor, url_prefix='/current-sensor')
app.register_blueprint(exit, url_prefix='/exit')
app.register_blueprint(flight_time, url_prefix='/flight-time')
app.register_blueprint(flying_wing_design, url_prefix='/flying-wing-design')
app.register_blueprint(index, url_prefix='/')
app.register_blueprint(motor, url_prefix='/motor')

if __name__ == '__main__':

    webbrowser.open('http://localhost:8888/', new=2)
    print(app.url_map)
    app.run(port=8888, debug=False)
    print("Server shutdown. Bye!")
