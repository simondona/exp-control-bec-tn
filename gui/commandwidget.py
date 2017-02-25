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


from PySide import QtGui

from .constants import RED, BLUE

class CommandWidget(QtGui.QWidget):
    def __init__(self, mainwindow, parent=None, *args, **kwargs):
        self.mainwindow = mainwindow
        
        self.cmd_init_edit = mainwindow.cmd_init_edit
        self.cmd_loop_edit = mainwindow.cmd_loop_edit
        
        super(CommandWidget, self).__init__(parent=None, *args, **kwargs)
        self.initUi()
        
    def initUi(self):
        cmd_layout = QtGui.QGridLayout(self)
        
        #commands tab
        init_tab = QtGui.QWidget()
        init_tab.setToolTip("run once at the beginning, variables prg and cmd are avaiable")
        init_layout = QtGui.QVBoxLayout(init_tab)
        init_layout.addWidget(self.cmd_init_edit)

        loop_tab = QtGui.QWidget()
        loop_tab.setToolTip("infinite loop, interrupt with cmd.stop()")
        loop_layout = QtGui.QVBoxLayout(loop_tab)
        loop_layout.addWidget(self.cmd_loop_edit)

        cmd_sub_tabwidget = QtGui.QTabWidget(self)
        cmd_sub_tabwidget.addTab(init_tab, "Init")
        cmd_sub_tabwidget.addTab(loop_tab, "Loop")

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