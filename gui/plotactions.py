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

import matplotlib
matplotlib.use("Qt4Agg")
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT


class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if \
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, parent_axis=None, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(FigureCanvas, self).__init__(self.fig)
        self.setParent(parent)

        self.axis = self.fig.add_subplot(111, sharex=parent_axis)


class PlotActionsDialog(QtGui.QDialog, object):

    def __init__(self, table, parent=None, system=None):
        super(PlotActionsDialog, self).__init__(parent=parent)

        self.table = table

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        plot1 = FigureCanvas(parent=self)
        plot2 = FigureCanvas(parent_axis=plot1.axis, parent=self)
        toolbar = NavigationToolbar(plot1, self)

        layout.addWidget(toolbar, 0, 0)
        layout.addWidget(plot1, 1, 0)
        layout.addWidget(plot2, 2, 0, 2, 1)

        self.setWindowTitle("Plot of program actions")
        self.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(600, 400)
