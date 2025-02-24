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

import textwrap

import pytest

import pytest_bdd as bdd
bdd.scenarios('hints.feature')


@pytest.fixture(autouse=True)
def set_up_word_hints(tmpdir, quteproc):
    dict_file = tmpdir / 'dict'
    dict_file.write(textwrap.dedent("""
        one
        two
        three
        four
        five
        six
        seven
        eight
        nine
        ten
        eleven
        twelve
        thirteen
    """))
    quteproc.set_setting('hints.dictionary', str(dict_file))
