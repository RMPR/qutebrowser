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

"""Various meta-tests for conftest.py."""


import os
import sys
import warnings

import pytest

import qutebrowser


def test_qapp_name(qapp):
    """Make sure the QApplication name is changed when we use qapp."""
    assert qapp.applicationName() == 'qute_test'


def test_no_qapp(request):
    """Make sure a test without qapp doesn't use qapp (via autouse)."""
    assert 'qapp' not in request.fixturenames


def test_fail_on_warnings():
    with pytest.raises(PendingDeprecationWarning):
        warnings.warn('test', PendingDeprecationWarning)


@pytest.mark.xfail(reason="https://github.com/qutebrowser/qutebrowser/issues/1070",
                   strict=False)
def test_installed_package():
    """Make sure the tests are running against the installed package."""
    print(sys.path)
    assert '.tox' in qutebrowser.__file__.split(os.sep)
