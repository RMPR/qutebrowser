#!/usr/bin/env python3
# Copyright 2020-2021 Florian Bruhin (The Compiler) <mail@qutebrowser.org>

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

"""Show information about the OpenGL setup."""

from PyQt6.QtGui import QOpenGLContext, QOffscreenSurface, QGuiApplication
from PyQt6.QtOpenGL import QOpenGLVersionProfile, QOpenGLVersionFunctionsFactory

app = QGuiApplication([])

surface = QOffscreenSurface()
surface.create()

ctx = QOpenGLContext()
ok = ctx.create()
assert ok

ok = ctx.makeCurrent(surface)
assert ok

print(f"GLES: {ctx.isOpenGLES()}")

vp = QOpenGLVersionProfile()
vp.setVersion(2, 0)

vf = QOpenGLVersionFunctionsFactory.get(vp, ctx)
print(f"Vendor: {vf.glGetString(vf.GL_VENDOR)}")
print(f"Renderer: {vf.glGetString(vf.GL_RENDERER)}")
print(f"Version: {vf.glGetString(vf.GL_VERSION)}")
print(f"Shading language version: {vf.glGetString(vf.GL_SHADING_LANGUAGE_VERSION)}")

ctx.doneCurrent()
