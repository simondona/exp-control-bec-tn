#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2017  Simone Donadello, Carmelo Mordini
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

import os
from functools import partial
import numpy as np

import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter as conv
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from PySide import QtGui, QtCore

from .ui.rampgendialog_ui import Ui_RampGenDialog

class QPushButtonIndexed(QtGui.QPushButton):
    indexSignal = QtCore.Signal(int)
    nextIndexSignal = QtCore.Signal(int)
    def __init__(self, index, *args, **kwargs):
        super(QPushButtonIndexed, self).__init__(*args, **kwargs)
        self.index = index
        self.clicked.connect(self.emit_index)
        self.clicked.connect(self.emit_next_index)
        
    def emit_index(self):
        self.indexSignal.emit(self.index)
    def emit_next_index(self):
        self.nextIndexSignal.emit(self.index + 1)

class RampRow():
    def __init__(self, index=0, **kwargs):
        self._ix = index
        self._npoints = 100
        self._t0 = 0.0
        self._t1 = 100.0
        self._x0 = 60.0
        self._x1 = 40.0
        self._amp0 = 1000
        self._amp1 = 1000
        self._omit = False
        self.updateValues(kwargs)
        
    @property
    def ix(self):
        return self._ix
    @ix.setter
    def ix(self, value):
        try:
            self._ix = int(value)
        except ValueError as e:
            print(e)
            return self._ix
        
    @property
    def t0(self):
        return self._t0
    @t0.setter
    def t0(self, value):
        try:
            self._t0 = float(value)
        except ValueError as e:
            print(e)
            return self._t0
        
    @property
    def t1(self):
        return self._t1
    @t1.setter
    def t1(self, value):
        try:
            self._t1 = float(value)
        except ValueError as e:
            print(e)
            return self._t1
    
    @property
    def x0(self):
        return self._x0
    @x0.setter
    def x0(self, value):
        try:
            self._x0 = float(value)
        except ValueError as e:
            print(e)
            return self._x0
    
    @property
    def x1(self):
        return self._x1
    @x1.setter
    def x1(self, value):
        try:
            self._x1 = float(value)
        except ValueError as e:
            print(e)
            return self._x1
        
    @property
    def npoints(self):
        return self._npoints
    @npoints.setter
    def npoints(self, value):
        try:
            self._npoints = int(value)
        except ValueError as e:
            print(e)
            return self._npoints
        
    @property
    def amp0(self):
        return self._amp0
    @amp0.setter
    def amp0(self, value):
        try:
            self._amp0 = int(value)
        except ValueError as e:
            print(e)
            return self._amp0
    
    @property
    def amp1(self):
        return self._amp1
    @amp1.setter
    def amp1(self, value):
        try:
            self._amp1 = int(value)
        except ValueError as e:
            print(e)
            return self._amp1
        
    @property
    def omit(self):
        return self._omit
    @omit.setter
    def omit(self, value):
        try:
            self._omit = bool(value)
        except ValueError as e:
            print(e)
            return self._omit
        
    @property
    def slope(self):
        return (self.x1 - self.x0)/(self.t1 - self.t0)
    
    @property
    def times(self):
        return np.linspace(self.t0, self.t1, self.npoints)
    
    @property
    def freqs(self):
        return np.linspace(self.x0, self.x1, self.npoints)
    
    @property
    def amps(self):
        return np.linspace(self.amp0, self.amp1, self.npoints)

        
    def updateValues(self, dictV): # è più corretto settare gli attributi uno a uno
        for k in dictV:
            if hasattr(self, k):
                setattr(self, k, dictV[k])
    
    

class RampGenDialog(QtGui.QDialog, Ui_RampGenDialog):
    def __init__(self, parent, *args, **kwargs):
        super(RampGenDialog, self).__init__(parent=parent, *args, **kwargs)
        self.setupUi(self)
        self.setupPlotWidget(self.rampPlotWidget)
        
        self.headers = ['ix', 'npoints', 't0', 't1', 'x0', 'x1', 'slope', 'amp0', 'amp1', 'omit', 'Add', 'Remove']
        self.rowsList = []
        self.setupTable(self.table)
        
        
    @property
    def times_ramp(self):
        try:
            return np.concatenate([r.times for r in self.rowsList if r.omit is not True])
        except ValueError:
            return np.asarray([])
    
    @property
    def freqs_ramp(self):
        try:
            return np.concatenate([r.freqs for r in self.rowsList if r.omit is not True])
        except ValueError:
            return np.asarray([])
    
    @property
    def amps_ramp(self):
        try:
            return np.concatenate([r.amps for r in self.rowsList if r.omit is not True])
        except ValueError:
            return np.asarray([])
        
        
        
    def insertRow(self, index, initV=None):
        if initV is None and index > 0:
            print(index)
            lastRow = self.rowsList[index-1]
            initV = {'t0': lastRow.t1,
                     't1': lastRow.t1 + 100.0,
                     'x0': lastRow.x1,
                     'x1': lastRow.x1 - 10.0,}
            newRow = RampRow(index, **initV)
        else:
            newRow = RampRow(index)
        self.table.insertRow(index)
        self.table.blockSignals(True)
        self.writeTableRow(index, newRow)
        self.table.blockSignals(False)
        self.rowsList.insert(index, newRow)
        print('Added the {:d} row'.format(index))
        self.plotRamps()

    
    def removeRow(self, index):
        if self.table.rowCount() == 1:
            print("You shouldn't remove the last row!\n")
            return
        self.table.removeRow(index)
        self.rowsList.pop(index)
        print('Removed the {:d} row'.format(index))
        print('There are {:d} rows left\n'.format(self.table.rowCount()))
        self.plotRamps()
        
    def writeTableRow(self, index, row):
        for col_index, head in enumerate(self.headers):
            if hasattr(row, head):
    #            print('writing ',head)
                item = getattr(row, head)
                if head in ['omit',]:
                    witem = QtGui.QTableWidgetItem()
                    witem.setCheckState(QtCore.Qt.CheckState(item))
                    self.table.setItem(index, col_index, witem)
                elif head in ['ix', 'npoints', 'amp0', 'amp1',]:
                    witem = QtGui.QTableWidgetItem('{:d}'.format(item))
                    self.table.setItem(index, col_index, witem)
                elif head in ['t0', 't1', 'x0', 'x1',]:
                    witem = QtGui.QTableWidgetItem('{:.2f}'.format(item))
                    self.table.setItem(index, col_index, witem)
                elif head in ['slope',]:
                    witem = QtGui.QTableWidgetItem('{:.4f}'.format(item))
                    witem.setFlags(QtCore.Qt.ItemIsEnabled)
    #                witem.setTextColor(QtGui.QColor('gray'))
                    self.table.setItem(index, col_index, witem)
            elif head == 'Add':
#                    void_item = QtGui.QTableWidgetItem()
#                    self.setItem(index, col_index, void_item)
                witem = QPushButtonIndexed(index, text='Add',)
                self.table.setCellWidget(index, col_index, witem)
                witem.nextIndexSignal.connect(self.insertRow)
            else: # head == 'Add':
                witem = QPushButtonIndexed(index, text='Remove')
                self.table.setCellWidget(index, col_index, witem)
                witem.indexSignal.connect(self.removeRow)
#        [self.table.resizeColumnToContents(j) for j in [0,1,2]]
        
        
    @QtCore.Slot(QtGui.QTableWidgetItem)
    def update_row(self, item):
        #TODO: handle exceptions for wrong data typed in
        dicV = {}
#        item = self.sender()
        print(item)
        index = item.row()
        col_index = item.column()
        head = self.headers[col_index]
#        for col_index, head in enumerate(self.headers):
        if head in ['omit']:
            dicV.update({head: bool(item.checkState())})

        else:
#                item = self.item(index, col_index)                
            dicV.update({head: float(item.text())})
        print("I'm changing row ", index)
        print('dic:', dicV)
        row = self.rowsList[index]
        row.updateValues(dicV)
#        self.table.blockSignals(True)
#        self.writeTableRow(index, row)
#        self.table.blockSignals(False)
        self.plotRamps()

            
        
    def setupTable(self, table):
        horizHeader = table.horizontalHeader()
#        horizHeader.setStretchLastSection(True)
        table.setColumnCount(len(self.headers))
        table.setHorizontalHeaderLabels(self.headers)                
        table.itemChanged.connect(self.update_row)
        table.blockSignals(True)
        self.insertRow(0)
        self.setFixedWidth(horizHeader.length() + 60)
    
    def setupPlotWidget(self, plotwidget):
        self.plot_kwargs = {'marker': 'o',
                            'ms': 4
                            }
        self.figure, self.axes = plt.subplots(1,1, figsize=(4,3))
        self.axes.plot(np.random.rand(10))
        self.figure.set_facecolor('none')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, plotwidget, coordinates=False)
        self.toolbar.setOrientation(QtCore.Qt.Horizontal)
        self.plotwidgetLayout = QtGui.QVBoxLayout(plotwidget)
        self.plotwidgetLayout.addWidget(self.canvas)
        self.plotwidgetLayout.addWidget(self.toolbar)
        plotwidget.setLayout(self.plotwidgetLayout)
        self.canvas.draw()
        
    def plotRamps(self,):
        self.axes.cla()
        self.axes.plot(self.times_ramp, self.freqs_ramp, **self.plot_kwargs)
        self.axes.grid(True)
        self.canvas.draw()
        

