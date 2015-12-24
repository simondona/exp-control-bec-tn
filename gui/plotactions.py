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

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(FigureCanvas, self).__init__(self.fig)
        self.setParent(parent)

        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212, sharex=self.ax1)
        
        self.ax1_bis = self.ax1.twinx()


class PlotActionsDialog(QtGui.QDialog, object):

    def __init__(self, table, parent=None, system=None):
        super(PlotActionsDialog, self).__init__(parent=parent)

        self.table = table
        
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        plot = FigureCanvas(self)
        layout.addWidget(plot)

        self.setWindowTitle("Plot of program actions")
        self.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(600, 400)

