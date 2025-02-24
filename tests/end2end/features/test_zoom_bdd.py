# Copyright 2015-2021 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <https://www.gnu.org/licenses/>.

import pytest_bdd as bdd
bdd.scenarios('zoom.feature')


@bdd.then(bdd.parsers.parse("the zoom should be {zoom}%"))
def check_zoom(quteproc, zoom):
    data = quteproc.get_session()
    histories = data['windows'][0]['tabs'][0]['history']
    value = next(h for h in histories if 'zoom' in h)['zoom'] * 100
    assert abs(value - float(zoom)) < 0.0001
