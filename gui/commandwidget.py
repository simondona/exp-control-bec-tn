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


from PySide import QtGui, QtCore

from .constants import RED, BLUE


class VariableForm(QtGui.QWidget):
    deleteMeSignal = QtCore.Signal(QtGui.QWidget)
    
    def __init__(self):
        super(VariableForm, self).__init__()
        self.setupUi()
        self.del_button.clicked.connect(self.deleteMe)
        
    @property
    def name(self):
        return self.name_edit.text()
    @property
    def start(self):
        try:
            return float(self.start_lineEdit.text())
        except ValueError:
            print "Invalid input: 'start' must be a number"
            return 0
    @property
    def stop(self):
        try:
            return float(self.stop_lineEdit.text())
        except ValueError:
            print "Invalid input: 'stop' must be a number"
            return 1
    @property
    def step(self):
        try:
            return float(self.step_lineEdit.text())
        except ValueError:
            print "Invalid input: 'step' must be a number"
            return 1
    @property
    def npoints(self):
        return max(0, (self.stop - self.start)//abs(self.step))
    
    def write_npoints(self):
        self.npoints_value_label.setText("(%d)"%self.npoints)
        if self.npoints == 0:
            self.npoints_value_label.setStyleSheet("color: %s"%RED)
        else:
            self.npoints_value_label.setStyleSheet("")
            
    def deleteMe(self):
        self.deleteMeSignal.emit(self)
    
    def setupUi(self):
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setContentsMargins(-1, 6, -1, 6)
        self.gridLayout.setVerticalSpacing(0)
        
        self.name_edit = QtGui.QLineEdit(self)
        self.name_edit.setText("")
        self.gridLayout.addWidget(self.name_edit, 0, 0, 1, 2)
        
        self.add_button = QtGui.QPushButton("Add")
        self.gridLayout.addWidget(self.add_button, 0, 2, 1, 1)
        
        self.del_button = QtGui.QPushButton("Del")
        self.gridLayout.addWidget(self.del_button, 0, 3, 1, 1)
        
        self.start_label = QtGui.QLabel("Start")
        self.gridLayout.addWidget(self.start_label, 1, 0, 1, 1)
        self.stop_label = QtGui.QLabel("Stop")
        self.gridLayout.addWidget(self.stop_label, 1, 1, 1, 1)
        self.step_label = QtGui.QLabel("Step")
        self.gridLayout.addWidget(self.step_label, 1, 2, 1, 1)
        self.npoints_label = QtGui.QLabel("N points")
        self.gridLayout.addWidget(self.npoints_label, 1, 3, 1, 1)
        
        self.start_lineEdit = QtGui.QLineEdit(self)
        self.start_lineEdit.setText('0')
        self.start_lineEdit.textChanged.connect(self.write_npoints)
        self.gridLayout.addWidget(self.start_lineEdit, 2, 0, 1, 1)
        self.stop_lineEdit = QtGui.QLineEdit(self)
        self.stop_lineEdit.setText('1')
        self.stop_lineEdit.textChanged.connect(self.write_npoints)
        self.gridLayout.addWidget(self.stop_lineEdit, 2, 1, 1, 1)
        self.step_lineEdit = QtGui.QLineEdit(self)
        self.step_lineEdit.setText('1')
        self.step_lineEdit.textChanged.connect(self.write_npoints)
        self.gridLayout.addWidget(self.step_lineEdit, 2, 2, 1, 1)
        self.npoints_value_label = QtGui.QLabel()
        self.write_npoints()
        self.gridLayout.addWidget(self.npoints_value_label, 2, 3, 1, 1)



class VariablesWidget(QtGui.QWidget):
    def __init__(self, iconSize=QtCore.QSize(36, 36), *args, **kwargs):
        self.vars_list = []
        self._iconSize = iconSize
        super(VariablesWidget, self).__init__(*args, **kwargs)
        self.initUi()
        
        self.add_variable()
    
    @property    
    def n_vars(self):
        return len(self.vars_list)
    @property
    def operation(self):
        if self.n_vars >= 1:
            return self.oper_combo.currentText()
        else:
            return None
                
    def initUi(self):
        layout = QtGui.QVBoxLayout(self)
        
        self.auto_button = QtGui.QPushButton()
        self.auto_button.setCheckable(True)
        self.auto_button.toggled.connect(self.style_auto_button)
        self.style_auto_button()        
        layout.addWidget(self.auto_button)
        
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        layout.addWidget(line)
        
        hlayout = QtGui.QHBoxLayout()
        layout.addLayout(hlayout)
        
        vlabel = QtGui.QLabel("Variables")
        vlabel.setFixedHeight(self._iconSize.height())
        hlayout.addWidget(vlabel)
        
        self.oper_combo = QtGui.QComboBox()
        self.oper_combo.setFixedHeight(self._iconSize.height())
        self.oper_combo.addItem("plus") #TODO add icons
        self.oper_combo.addItem("cross")
#        like:
#        icon = QtGui.QIcon(QtGui.QPixmap(_fromUtf8(':/icons/edit-table-insert-column-right.png')))
#        self.oper_combo.addItem(icon, "+")
        hlayout.addWidget(self.oper_combo)        
        self.oper_combo.setVisible(False)
        
        hlayout.setStretch(0,3)
        hlayout.setStretch(1,1)
        
        
        self.vars_layout = QtGui.QVBoxLayout()
        self.vars_layout.setAlignment(QtCore.Qt.AlignTop)
        layout.addLayout(self.vars_layout)
        
        line = QtGui.QFrame()
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        layout.addWidget(line)
        
        wait_widg = QtGui.QWidget()
        wait_layout = QtGui.QFormLayout(wait_widg)
        self.wait_spinBox = QtGui.QSpinBox()
        wait_layout.addRow("Wait time (ms)", self.wait_spinBox)
        self.wait_spinBox.setMaximum(99999)
        self.wait_spinBox.setValue(100)
        layout.addWidget(wait_widg)
        
        layout.addStretch()
        
        
    def add_variable(self):
        v = VariableForm()
        self.vars_list.append(v)
        self.vars_layout.addWidget(v)
        v.add_button.clicked.connect(self.add_variable)
        if self.n_vars > 1:
            self.oper_combo.setVisible(True)
            v.deleteMeSignal.connect(self.del_variable)
        else:
            v.del_button.setEnabled(False)
        
    @QtCore.Slot(QtGui.QWidget)
    def del_variable(self, var):
        self.vars_layout.removeWidget(var)
        var.deleteLater()
        self.vars_list.remove(var)
        if self.n_vars <= 1:
            self.oper_combo.setVisible(False)
            
    def style_auto_button(self):
        if self.auto_button.isChecked():
            self.auto_button.setText('Auto')
            self.auto_button.setStyleSheet("color: %s"%RED)
        else:
            self.auto_button.setText('Manual')
            self.auto_button.setStyleSheet("")
        
        
        
        
        
class CommandWidget(QtGui.QWidget):
    def __init__(self, mainwindow, parent=None, *args, **kwargs):
        self.mainwindow = mainwindow
        
        self.cmd_init_edit = mainwindow.cmd_init_edit
        self.cmd_loop_edit = mainwindow.cmd_loop_edit
        self.cmd_init_edit.setToolTip("run once at the beginning, variables prg and cmd are avaiable")
        self.cmd_loop_edit.setToolTip("infinite loop, interrupt with cmd.stop()")
        super(CommandWidget, self).__init__(parent=None, *args, **kwargs)
        self.initUi()
        
        self.variables = self.vars_tab.vars_list
        self.operation = self.vars_tab.operation
        
        
    def initUi(self):
        cmd_layout = QtGui.QGridLayout(self)
        
        #commands tab
        self.vars_tab = VariablesWidget()
        self.vars_tab.setToolTip("An user-friendly interface for cmd variables setting")
        


        code_tab = QtGui.QWidget()
        code_tab.setToolTip("The commands code")
        code_layout = QtGui.QVBoxLayout(code_tab)
        init_label = QtGui.QLabel("Init")
        loop_label = QtGui.QLabel("Loop")
        code_layout.addWidget(init_label)
        code_layout.addWidget(self.cmd_init_edit)
        code_layout.addWidget(loop_label)
        code_layout.addWidget(self.cmd_loop_edit)
        code_layout.setStretch(0,0)
        code_layout.setStretch(1,1)
        code_layout.setStretch(2,0)
        code_layout.setStretch(3,2)

        cmd_sub_tabwidget = QtGui.QTabWidget(self)
        cmd_sub_tabwidget.addTab(self.vars_tab, "Vars")
        cmd_sub_tabwidget.addTab(code_tab, "Code")

        #commands text areas settings
        font = QtGui.QFont("Monospace")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        font.setPointSize(int(0.8*float(font.pointSize())))
        self.cmd_loop_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.cmd_init_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.cmd_loop_edit.setFont(font)
        self.cmd_init_edit.setFont(font)
        

        #start stop commands buttons settings
        self.start_cmd_button = QtGui.QPushButton("Start")
        self.start_cmd_button.setToolTip("send system commands (init + the infinite loop)")
        self.start_cmd_button.setStyleSheet("color: %s"%BLUE)
        self.stop_cmd_button = QtGui.QPushButton("Stop")
        self.stop_cmd_button.setToolTip("stop the running system commands")
        self.stop_cmd_button.setStyleSheet("color: %s"%RED)

        #commands layout
        cmd_layout.addWidget(cmd_sub_tabwidget, 0, 0, 1, 2)
        cmd_layout.addWidget(self.start_cmd_button, 1, 0, 1, 1)
        cmd_layout.addWidget(self.stop_cmd_button, 1, 1, 1, 1)