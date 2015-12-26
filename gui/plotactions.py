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
matplotlib.rcParams['font.size'] = 9
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
        self.fig.tight_layout(pad=2.5)


class DigitalCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        super(DigitalCanvas, self).__init__(*args, height=2, **kwargs)
        self.axis.set_yticks([])


class AnalogCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        super(AnalogCanvas, self).__init__(*args, height=6, **kwargs)
        self.axis2 = self.axis.twinx()


class AvaiableActions(QtGui.QTableWidget, object):
    def __init__(self, acts, parent=None):
        columns = [("name", 120),
                   ("A1", 40),
                   ("A2", 40),
                   ("B", 40),
                   ("col", 40),
                   ("sty", 40)]
        self.acts = acts

        super(AvaiableActions, self).__init__(len(self.acts), len(columns), parent=parent)

        self.setHorizontalHeaderLabels([c[0] for c in columns])
        for n, c in enumerate(columns):
            self.setColumnWidth(n, c[1])

        for n, a in enumerate(sorted(self.acts.keys())):
            i = QtGui.QTableWidgetItem(str(a))
            self.setItem(n, 0, i)
            check_a1 = QtGui.QCheckBox()
            check_a2 = QtGui.QCheckBox()
            check_b = QtGui.QCheckBox()
            self.setCellWidget(n, 1, check_a1)
            self.setCellWidget(n, 2, check_a2)
            self.setCellWidget(n, 3, check_b)

            combo_col = ColorCombo()
            self.setCellWidget(n, 4, combo_col)
            combo_sty = StyleCombo()
            self.setCellWidget(n, 5, combo_sty)


class ColorCombo(QtGui.QComboBox):
    def __init__(self):
        super(ColorCombo, self).__init__()

        colors = [("r", QtCore.Qt.red),
                  ("b", QtCore.Qt.blue),
                  ("c", QtCore.Qt.cyan),
                  ("g", QtCore.Qt.green),
                  ("m", QtCore.Qt.magenta),
                  ("y", QtCore.Qt.darkYellow),
                  ("k", QtCore.Qt.gray)]
        for n_col, col in enumerate(colors):
            self.addItem(col[0])
            self.setItemData(n_col,
                             QtGui.QColor(col[1]),
                             QtCore.Qt.BackgroundRole)


class StyleCombo(QtGui.QComboBox):
    def __init__(self):
        super(StyleCombo, self).__init__()

        styles = ["-", "--", "-.", ":"]
        self.addItems(styles)


class PlotActionsDialog(QtGui.QDialog, object):
    def __init__(self, table, parent=None, system=None):
        super(PlotActionsDialog, self).__init__(parent=parent)

        self.table = table
        self.avaiable_acts = dict((act["name"], dict(vars=act["vars"].keys())) for act in self.table.prg_list())

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        actions_table = AvaiableActions(self.avaiable_acts, parent=self)
        plot1 = AnalogCanvas(parent=self)
        plot2 = DigitalCanvas(parent_axis=plot1.axis, parent=self)
        toolbar = NavigationToolbar(plot1, self)

        layout.addWidget(actions_table, 0, 0, 5, 1)
        layout.addWidget(toolbar, 0, 1)
        layout.addWidget(plot1, 1, 1, 3, 1)
        layout.addWidget(plot2, 4, 1)

        self.setWindowTitle("Plot of program actions")
        self.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(800, 400)
