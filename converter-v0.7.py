#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 13:35:47 2015

@author: Simone Donadello
"""

import shutil

#move all user data in the "data" folder
shutil.move("programs", "data/programs")
shutil.move("definitions/actions", "data")
shutil.move("definitions/boards", "data")
shutil.rmtree("definitions")
shutil.move(".program.conf", "data")
