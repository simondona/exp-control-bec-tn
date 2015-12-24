#!/usr/bin/python
# -*- coding: utf-8 -*-

# Experiment Control BEC TN
# Copyright (C) 2015  Simone Donadello
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui


class PlotActionsDialog(QtGui.QDialog, object):

    def __init__(self, parent=None, system=None):
        super(PlotActionsDialog, self).__init__(parent=parent)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        
        self.setWindowTitle("Plot of program actions")
        self.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(600, 400)