# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:24:17 2016

@author: deudon
"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *


class StartupView(QtGui.QWidget):
    # Signals
    start_form_sig = QtCore.pyqtSignal()
    start_training_fam_sig = QtCore.pyqtSignal()
    start_training_new_sig = QtCore.pyqtSignal()
    start_test_fam_sig = QtCore.pyqtSignal()
    start_test_new_sig = QtCore.pyqtSignal()
    quit_app_sig = QtCore.pyqtSignal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)

        # Top Horizontal Layout (with Quit Button)
        hori_layout = QHBoxLayout()
        hori_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        quit_btn = QPushButton("Quit")
        size_policy = QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        quit_btn.setSizePolicy(size_policy)
        hori_layout.addWidget(quit_btn)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hori_layout.addItem(spacer_item)
        quit_btn.pressed.connect(lambda: self.quit_app_sig.emit())
        layout.addLayout(hori_layout)

        # Page title
        self.page_title = QtGui.QLabel("DANA SOFT")
        self.page_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.page_title)
        
        # Spacer
        spacer_item = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer_item)
        
        # Buttons
        button_layout = QtGui.QGridLayout()
        button_layout.setHorizontalSpacing(20)
        button_layout.setVerticalSpacing(20)
        create_subject_btn = QtGui.QPushButton("Create Subject")
        self.start_train_fam_btn = QtGui.QPushButton("Start Training Fam")
        self.start_train_new_btn = QtGui.QPushButton("Start Training New")
        self.start_test_fam_btn = QtGui.QPushButton("Start Test Fam")
        self.start_test_new_btn = QtGui.QPushButton("Start Test New")
        button_layout.addWidget(create_subject_btn, 0, 1, 1, 1)
        button_layout.addWidget(self.start_train_fam_btn, 1, 0, 1, 1)
        button_layout.addWidget(self.start_train_new_btn, 2, 0, 1, 1)
        button_layout.addWidget(self.start_test_fam_btn, 1, 2, 1, 1)
        button_layout.addWidget(self.start_test_new_btn, 2, 2, 1, 1)
        layout.addLayout(button_layout)

        # Signals
        create_subject_btn.clicked.connect(lambda: self.start_form_sig.emit())
        self.start_train_fam_btn.clicked.connect(lambda: self.start_training_fam_sig.emit())
        self.start_train_new_btn.clicked.connect(lambda: self.start_training_new_sig.emit())
        self.start_test_fam_btn.clicked.connect(lambda: self.start_test_fam_sig.emit())
        self.start_test_new_btn.clicked.connect(lambda: self.start_test_new_sig.emit())

        # Disable buttons
        self.enablebuttons(0)
        
    def enablebuttons(self, val):
        self.start_train_fam_btn.setEnabled(val)
        self.start_train_new_btn.setEnabled(val)
        self.start_test_fam_btn.setEnabled(val)
        self.start_test_new_btn.setEnabled(val)

    def set_title(self, title):
        self.page_title.setText(title)