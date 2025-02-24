# Copyright 2016-2021 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
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

"""Test hints based on html files with special comments."""

import pathlib
import textwrap
import dataclasses
from typing import Optional

import pytest
import bs4

from qutebrowser.utils import utils


def collect_tests():
    basedir = pathlib.Path(__file__).parent
    datadir = basedir / 'data' / 'hints' / 'html'
    files = [f.name for f in datadir.iterdir() if f.name != 'README.md']
    return files


@dataclasses.dataclass
class ParsedFile:

    target: Optional[str]
    qtwebengine_todo: Optional[str]


class InvalidFile(Exception):

    def __init__(self, test_name, msg):
        super().__init__("Invalid comment found in {}, please read "
                         "tests/end2end/data/hints/html/README.md - {}".format(
                             test_name, msg))


def _parse_file(test_name):
    """Parse the given HTML file."""
    file_path = (pathlib.Path(__file__).parent.resolve()
                 / 'data' / 'hints' / 'html' / test_name)
    with file_path.open('r', encoding='utf-8') as html:
        soup = bs4.BeautifulSoup(html, 'html.parser')

    comment = str(soup.find(string=lambda text: isinstance(text, bs4.Comment)))

    if comment is None:
        raise InvalidFile(test_name, "no comment found")

    data = utils.yaml_load(comment)

    if not isinstance(data, dict):
        raise InvalidFile(test_name, "expected yaml dict but got {}".format(
            type(data).__name__))

    allowed_keys = {'target', 'qtwebengine_todo'}
    if not set(data.keys()).issubset(allowed_keys):
        raise InvalidFile(test_name, "expected keys {} but found {}".format(
            ', '.join(allowed_keys),
            ', '.join(set(data.keys()))))

    if 'target' not in data:
        raise InvalidFile(test_name, "'target' key not found")

    qtwebengine_todo = data.get('qtwebengine_todo', None)

    return ParsedFile(target=data['target'], qtwebengine_todo=qtwebengine_todo)


@pytest.mark.parametrize('test_name', collect_tests())
@pytest.mark.parametrize('zoom_text_only', [True, False])
@pytest.mark.parametrize('zoom_level', [100, 66, 33])
@pytest.mark.parametrize('find_implementation', ['javascript', 'python'])
def test_hints(test_name, zoom_text_only, zoom_level, find_implementation,
               quteproc, request):
    if zoom_text_only and request.config.webengine:
        pytest.skip("QtWebEngine doesn't have zoom.text_only")
    if find_implementation == 'python' and request.config.webengine:
        pytest.skip("QtWebEngine doesn't have a python find implementation")

    parsed = _parse_file(test_name)
    if parsed.qtwebengine_todo is not None and request.config.webengine:
        pytest.xfail("QtWebEngine TODO: {}".format(parsed.qtwebengine_todo))

    url_path = 'data/hints/html/{}'.format(test_name)
    quteproc.open_path(url_path)

    # setup
    if not request.config.webengine:
        quteproc.set_setting('zoom.text_only', str(zoom_text_only))
        quteproc.set_setting('hints.find_implementation', find_implementation)
    quteproc.send_cmd(':zoom {}'.format(zoom_level))

    # follow hint
    quteproc.send_cmd(':hint all normal')

    if parsed.target is None:
        msg = quteproc.wait_for(message='No elements found.', category='message')
        msg.expected = True
    else:
        quteproc.wait_for(message='hints: a', category='hints')
        quteproc.send_cmd(':hint-follow a')
        quteproc.wait_for_load_finished('data/' + parsed.target)

    # reset
    quteproc.send_cmd(':zoom 100')
    if not request.config.webengine:
        quteproc.set_setting('zoom.text_only', 'false')
        quteproc.set_setting('hints.find_implementation', 'javascript')


@pytest.mark.skip  # Too flaky
def test_word_hints_issue1393(quteproc, tmp_path):
    dict_file = tmp_path / 'dict'
    dict_file.write_text(textwrap.dedent("""
        alph
        beta
        gamm
        delt
        epsi
    """))
    targets = [
        ('words', 'words.txt'),
        ('smart', 'smart.txt'),
        ('hinting', 'hinting.txt'),
        ('alph', 'l33t.txt'),
        ('beta', 'l33t.txt'),
        ('gamm', 'l33t.txt'),
        ('delt', 'l33t.txt'),
        ('epsi', 'l33t.txt'),
    ]

    quteproc.set_setting('hints.mode', 'word')
    quteproc.set_setting('hints.dictionary', str(dict_file))

    for hint, target in targets:
        quteproc.open_path('data/hints/issue1393.html')
        quteproc.send_cmd(':hint')
        quteproc.wait_for(message='hints: *', category='hints')
        quteproc.send_cmd(':hint-follow {}'.format(hint))
        quteproc.wait_for_load_finished('data/{}'.format(target))
