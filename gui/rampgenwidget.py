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
#from matplotlib.colors import colorConverter as conv
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



class RampGenDialog(QtGui.QDialog, Ui_RampGenDialog):
    def __init__(self, parent, *args, **kwargs):
        super(RampGenDialog, self).__init__(parent=parent, *args, **kwargs)
        self.setupUi(self)
        self.connectButtons()
        self.setupPlotWidget(self.rampPlotWidget)
        
        self.currentRampName = '---'
        
        self.headers = ['npoints', 't0', 't1', 'x0', 'x1', 'amp0', 'amp1', 'omit', 'dt', 'slope', 'Add', 'Remove']
        self.headers_row = self.headers[:8]
        self.default_row = dict(zip(self.headers_row,
                                    [100, 0., 100., 60., 50., 1000, 1000, False, ]))
        self.setupTable(self.table)
        
        
    @property
    def times(self):
        v = []
        for index in range(self.table.rowCount()):
            row = self.readTableRow(index)
            if not row['omit']:
                v.append(np.linspace(row['t0'], row['t1'], row['npoints']))
        try:
            return np.concatenate(v)
        except ValueError:
            return np.asarray([])
    
    @property
    def freqs(self):
        v = []
        for index in range(self.table.rowCount()):
            row = self.readTableRow(index)
            if not row['omit']:
                v.append(np.linspace(row['x0'], row['x1'], row['npoints']))
        try:
            return np.concatenate(v)
        except ValueError:
            return np.asarray([])
    
    @property
    def amps(self):
        v = []
        for index in range(self.table.rowCount()):
            row = self.readTableRow(index)
            if not row['omit']:
                v.append(np.linspace(row['amp0'], row['amp1'], row['npoints']))
        try:
            return np.concatenate(v)
        except ValueError:
            return np.asarray([])
        
        
    def insertRow(self, index, row=None):
        if row is None:
            row = self.default_row.copy()
            if index > 0:
                print(index)
                lastRow = self.readTableRow(index-1)
                row.update({'t0': lastRow['t1'],
                               't1': lastRow['t1'] + 100.0,
                               'x0': lastRow['x1'],
                               'x1': lastRow['x1'] - 10.0,})
        self.table.insertRow(index)
        self.table.blockSignals(True)
        self.writeTableRow(index, row)
        self.table.blockSignals(False)
        print('Added the {:d} row'.format(index))

    
    def removeRow(self, index, force=False):
        if self.table.rowCount() == 1 and not force:
            print("You shouldn't remove the last row!\n")
            return
        self.table.removeRow(index)
        print('Removed the {:d} row'.format(index))
        print('There are {:d} rows left\n'.format(self.table.rowCount()))
        self.plotRamps()
        
    def readTableRow(self, index):
        row = {}
        for head in self.headers_row:
            col_index = self.headers.index(head)
            item = self.table.item(index, col_index)
            if head in ['omit',]:
                value = bool(item.checkState())
            elif head in ['npoints', 'amp0', 'amp1',]:
                try:
                    value = int(item.text())
                except ValueError as e:
                    print(e)
                    value = np.nan
            elif head in ['t0', 't1', 'x0', 'x1',]:
                try:
                    value = float(item.text())
                except ValueError as e:
                    print(e)
                    value = np.nan
            row[head] = value
        return row
        
    def writeTableRow(self, index, row):
        for col_index, head in enumerate(self.headers):
            witem = QtGui.QTableWidgetItem()
            if head in row:
    #            print('writing ',head)
                value = row[head]
                if head in ['omit',]:
                    witem.setCheckState(QtCore.Qt.CheckState(bool(value)))
                elif head in ['npoints', 'amp0', 'amp1',]:
                    witem.setText('{:d}'.format(int(value)))
                elif head in ['t0', 't1', 'x0', 'x1',]:
                    witem.setText('{:.2f}'.format(float(value)))
            else:
                if head == 'dt':
                    dt = row['t1'] - row['t0']
                    witem.setText('{:.4f}'.format(dt))
                elif head == 'slope':
                    try:
                        slope = (row['x1'] - row['x0'])/(row['t1'] - row['t0'])
                    except ZeroDivisionError as e:
                        print(e)
                        slope = np.nan
                    witem.setText('{:.4f}'.format(slope*1e3))
                elif head == 'Add':
                    widg = QPushButtonIndexed(index, text='Add',)
                    self.table.setCellWidget(index, col_index, widg)
                    widg.nextIndexSignal.connect(self.insertRow)
                elif head == 'Remove' and index > 0:
                    widg = QPushButtonIndexed(index, text='Remove')
                    self.table.setCellWidget(index, col_index, widg)
                    widg.indexSignal.connect(self.removeRow)
                else:
                    pass
                witem.setFlags(QtCore.Qt.ItemIsEnabled)
                witem.setBackground(QtGui.QColor('lightGray'))
            self.table.setItem(index, col_index, witem)
        self.plotRamps()

            
        
        
    @QtCore.Slot(QtGui.QTableWidgetItem)
    def updateRow(self, witem):
        index, col_index = witem.row(), witem.column()
        head = self.headers[col_index]
        # read updated values and format
        row = self.readTableRow(index)
        value = row[head]
        self.table.blockSignals(True)
        if head in ['npoints', 'amp0', 'amp1',]:
            witem.setText('{:d}'.format(value))
        elif head in ['t0', 't1', 'x0', 'x1',]:
            witem.setText('{:.2f}'.format(value))
        # update uneditable values (dt, slope)
        for head in ['dt', 'slope']:
            item = self.table.item(index, self.headers.index(head))
            if head == 'dt':
                dt = row['t1'] - row['t0']
                item.setText('{:.4f}'.format(dt))
            elif head == 'slope':
                try:
                    slope = (row['x1'] - row['x0'])/(row['t1'] - row['t0'])
                except ZeroDivisionError as e:
                    print(e)
                    slope = np.nan
                item.setText('{:.4f}'.format(slope*1e3))
        # ramps are auto-updated via properties. Now plot
        self.table.blockSignals(False)
        self.plotRamps()
        

    def connectButtons(self):
        self.loadPushButton.clicked.connect(self.load)
        self.newPushButton.clicked.connect(self.new)
        
    def setupTable(self, table):
        self.horizHeader = table.horizontalHeader()
        self.vertHeader = table.verticalHeader()
        self.vertHeader.setVisible(True)
        table.setColumnCount(len(self.headers))
        table.setHorizontalHeaderLabels(self.headers)                
        table.itemChanged.connect(self.updateRow)
#        table.blockSignals(True)
        self.insertRow(0)
        self.setFixedWidth(self.horizHeader.length() + 60)
    
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
        self.axes.plot(self.times, self.freqs, **self.plot_kwargs)
        self.axes.grid(True)
        self.canvas.draw()
        
    def clearTable(self,):
        for j in range(self.table.rowCount()):
            self.removeRow(j, force=True)
            
            
    def new(self):
        self.clearTable()
        self.insertRow(0)
        
    def load(self,):
        self.clearTable()
        fileName = QtGui.QFileDialog.getOpenFileName(self,'Open file', 
                                                     filter='Ramp txt/csv (*.txt *.csv)',
                                                     directory='data/evaporation')[0]
        print(fileName)
        headers_old = ['npoints', 't0', 't1', 'x0', 'x1', 'amp0', 'amp1',]
        A = np.genfromtxt(fileName, usecols=(1,2,3,4,5,6,7))
        for index, values in enumerate(A):
            row = {'omit': False,}
            row.update(dict(zip(headers_old, values)))
            print(row)
            self.insertRow(index, row)

