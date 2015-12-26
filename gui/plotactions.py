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


from functools import partial

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
    actions_updated = QtCore.pyqtSignal()
    def __init__(self, acts, parent=None):
        self.columns = [("name", 120),
                        ("y1", 40),
                        ("y2", 40),
                        ("col", 40),
                        ("sty", 40)]
        self.acts = acts

        super(AvaiableActions, self).__init__(len(self.acts), len(self.columns),
                                              parent=parent)

        self.setHorizontalHeaderLabels([col[0] for col in self.columns])
        for n_col, col in enumerate(self.columns):
            self.setColumnWidth(n_col, col[1])

        for n_row, row in enumerate(sorted(self.acts.keys())):
            itm = QtGui.QTableWidgetItem(str(row))
            itm.setFlags(itm.flags()&~QtCore.Qt.ItemIsEditable)
            self.setItem(n_row, 0, itm)

            check_y1 = QtGui.QCheckBox()
            check_y2 = QtGui.QCheckBox()
            self.setCellWidget(n_row, 1, check_y1)
            check_y1.stateChanged.connect(partial(self.on_state_changed,
                                                  n_row=n_row, n_col=1))
            self.setCellWidget(n_row, 2, check_y2)
            check_y2.stateChanged.connect(partial(self.on_state_changed,
                                                  n_row=n_row, n_col=2))

            combo_col = ColorCombo()
            combo_sty = StyleCombo()
            self.setCellWidget(n_row, 3, combo_col)
            combo_col.currentIndexChanged.connect(partial(self.on_state_changed,
                                                          n_row=n_row, n_col=3))
            self.setCellWidget(n_row, 4, combo_sty)
            combo_sty.currentIndexChanged.connect(partial(self.on_state_changed,
                                                          n_row=n_row, n_col=3))

    def on_state_changed(self, n_row, n_col):
        widget = self.cellWidget(n_row, n_col)
        item = sorted(self.acts.keys())[n_row]
        if n_col == 1:
            self.acts[item]["plot_y1"] = bool(widget.isChecked())
        elif n_col == 2:
            self.acts[item]["plot_y2"] = bool(widget.isChecked())
        elif n_col == 3:
            self.acts[item]["plot_col"] = str(widget.currentText())
        elif n_col == 4:
            self.acts[item]["plot_sty"] = str(widget.currentText())
        self.actions_updated.emit()


class ColorCombo(QtGui.QComboBox):
    def __init__(self):
        super(ColorCombo, self).__init__()

        colors = [("", QtCore.Qt.white),
                  ("r", QtCore.Qt.red),
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

        styles = ["", "-", "--", "-.", ":"]
        self.addItems(styles)


class PlotActionsDialog(QtGui.QDialog, object):
    def __init__(self, table, parent=None, system=None):
        super(PlotActionsDialog, self).__init__(parent=parent)

        self.table = table
        self.actions = self.table.get_all(lst=self.table.prg_list(),
                                          time=self.table.system.set_time(0.0),
                                          enable=True,
                                          enable_parent=True,
                                          extended=True)

        self.avaiable_acts = dict()
        for act in self.actions:
            name = act["name"]
            self.avaiable_acts[name] = dict(plot_y1=False,
                                            plot_y2=False,
                                            plot_col="",
                                            plot_sty="")

            var = act["vars"]
            if len(var) == 1:
                var = var.keys()[0]
            else:
                var = None
            self.avaiable_acts[name]["var"] = var

        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        actions_table = AvaiableActions(self.avaiable_acts, parent=self)
        self.plot1 = AnalogCanvas(parent=self)
        self.plot2 = DigitalCanvas(parent_axis=self.plot1.axis, parent=self)
        toolbar = NavigationToolbar(self.plot1, self)

        layout.addWidget(actions_table, 0, 0, 5, 1)
        layout.addWidget(toolbar, 0, 1)
        layout.addWidget(self.plot1, 1, 1, 3, 1)
        layout.addWidget(self.plot2, 4, 1)

        self.setWindowTitle("Plot of program actions")
        self.setFocus()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.resize(800, 400)

        actions_table.actions_updated.connect(self.plot)

    def plot(self):
        for act in self.avaiable_acts:
            if self.avaiable_acts[act]["plot_y1"] or self.avaiable_acts[act]["plot_y2"]:
                var_name = self.avaiable_acts[act]["var"]
                x = [a["time"] for a in self.actions if a["name"]==act]
                if var_name is not None:
                    y = [a["vars"][var_name] for a in self.actions if a["name"]==act]
                    self.plot1.axis.plot(x, y)
                self.plot2.axis.vlines(x, 0, 1)
