# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:24:17 2016

@author: deudon
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *


class VersionSelectionView(QtGui.QWidget):
    quit_app_sig = QtCore.pyqtSignal()
    version_selected_sig = QtCore.pyqtSignal(str, str)

    def __init__(self):
        self.response_version = ' '   # Can be 'tactile' or 'visual'
        self.version = ' '          # Can be 'explicit', 'fast-mapping', or 'simon'

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
        page_title = QtGui.QLabel("DANA SOFT - 3 objects\nSelect a version")
        page_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(page_title)

        # Spacer
        spacer_item = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        # Buttons
        button_layout = QtGui.QGridLayout()
        button_layout.setHorizontalSpacing(20)
        button_layout.setVerticalSpacing(20)

        explicit_learning_ver_btn = QtGui.QPushButton("Explicit Learning Version")
        explicit_one_rep_ver_btn = QtGui.QPushButton("Explicit Learning, One Rep. Version")
        fastmapping_ver_btn = QtGui.QPushButton("Fast-mapping Version")
        scrambled_2y_ver_btn = QtGui.QPushButton("Scrambled 2-Years Version")
        scrambled_4y_ver_btn = QtGui.QPushButton("Scrambled 4-Years Version")
        simon_ver_btn = QtGui.QPushButton("Simon's Version")
        simon_easy_ver_btn = QtGui.QPushButton("Simon's Version Easy")
        explicit_learning_ver_btn.pressed.connect(lambda: self.version_selected('explicit'))
        explicit_one_rep_ver_btn.pressed.connect(lambda: self.version_selected('explicit-1rep'))
        fastmapping_ver_btn.pressed.connect(lambda: self.version_selected('fast-mapping'))
        scrambled_2y_ver_btn.pressed.connect(lambda: self.version_selected('scrambled-2y'))
        scrambled_4y_ver_btn.pressed.connect(lambda: self.version_selected('scrambled-4y'))
        simon_ver_btn.pressed.connect(lambda: self.version_selected('simon'))
        simon_easy_ver_btn.pressed.connect(lambda: self.version_selected('simon-easy'))
        button_layout.addWidget(explicit_learning_ver_btn, 0, 0, 1, 1)
        button_layout.addWidget(explicit_one_rep_ver_btn, 0, 2, 1, 1)
        button_layout.addWidget(fastmapping_ver_btn, 1, 1, 1, 1)
        button_layout.addWidget(scrambled_2y_ver_btn, 2, 0, 1, 1)
        button_layout.addWidget(scrambled_4y_ver_btn, 2, 2, 1, 1)
        button_layout.addWidget(simon_ver_btn, 3, 0, 1, 1)
        button_layout.addWidget(simon_easy_ver_btn, 3, 2, 1, 1)
        radio_btn_layout = QtGui.QHBoxLayout()
        radio_btn_layout.setContentsMargins(20, 20, 20, 20)
        tactile_ver_btn = QtGui.QRadioButton('Tactile')
        tactile_ver_btn.setChecked(True)
        visual_ver_btn = QtGui.QRadioButton('Visuelle')
        tactile_ver_btn.clicked.connect(lambda: self.set_response_version('tactile'))
        visual_ver_btn.clicked.connect(lambda: self.set_response_version('visual'))
        spacer_hori = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        radio_btn_layout.addItem(spacer_hori)
        radio_btn_layout.addWidget(tactile_ver_btn)
        radio_btn_layout.addItem(spacer_hori)
        radio_btn_layout.addWidget(visual_ver_btn)
        radio_btn_layout.addItem(spacer_hori)

        layout.addLayout(button_layout)
        layout.addLayout(radio_btn_layout)
        layout.addItem(spacer_item)

    def version_selected(self, version):
        version = version.lower()
        if version in ['explicit', 'explicit-1rep', 'fast-mapping', 'scrambled-2y', 'scrambled-4y', 'simon', 'simon-easy']:
            self.version = version
        else:
            raise ValueError('Wrong value for argument version : {}. Possible values are {}'
                             .format(version, ['explicit', 'explicit-1rep', 'fast-mapping', 'scrambled-2y',
                                               'scrambled-4y', 'simon', 'simon-easy']))
        self.version_selected_sig.emit(self.version, self.response_version)

    def set_response_version(self, response_ver):
        response_ver = response_ver.lower()
        if response_ver in ['tactile', 'visual']:
            self.response_version = response_ver
        else:
            raise ValueError('Wrong value for argument response_ver : {}. Possible values are {}'
                             .format(response_ver, ['tactile', 'visual']))

