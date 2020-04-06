/*
    RC-Calc: An all-in-one R/C & FPV flying stuff calculator
    Copyright (C) 2020 Grégoire CAHUZAC <gregoire.cahuzac@outlook.fr>
    This file is part of RC-Calc. <https://github.com/Gregczc/RC-Calc>

    RC-Calc is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or any later version.

    RC-Calc is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with RC-Calc.  If not, see <http://www.gnu.org/licenses/>.
*/

function setLanguage(lang) {
    localStorage.setItem('language', lang);

     $.getJSON('/static/json/' + lang + '.json').done(function( data ) {

        Object.keys(data).forEach(function(key) {

            element = document.getElementById(key);

            if(element) {

                if(element.nodeName=="INPUT") {
                    element.placeholder = data[key];
                }

                else {
                    element.innerHTML = data[key];
                }
            }

        })

      });
}

function getString(id){
    lang = localStorage.getItem('language') == null ? localStorage.getItem('language') : 'en';
    $.getJSON('/static/json/' + lang + '.json').done(function( data ) {

        return Object.id;
        
      });
}