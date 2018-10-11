# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:31:49 2016

@author: deudon
"""

import os
import logging
import time
import random
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from PyQt4.QtGui import *
from config import *


class WaitLabel(QLabel):
    # Attributes
    timer = QtCore.QTimer()
    init_size = None
    ready = None
    # signal
    clicked_sig = QtCore.pyqtSignal()    
    
    def __init__(self):
        QtGui.QLabel.__init__(self)
        wait_image = QtGui.QImage()
        wait_image.load(TRAIN_WAIT_IMAGE_BKG)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("QLabel {background-color:black}")
        self.timer.timeout.connect(self.putattractorimage)
        self.init_size = 0
        self.ready = False
        
    def starttimer(self):
        self.timer.start(TRAIN_TIMER_DURATION)        
        
    def putattractorimage(self):
        wait_image = QtGui.QImage()
        wait_image.load(TRAIN_WAIT_IMAGE)
        pixmap = QtGui.QPixmap(wait_image)
        scaled_pixmap = pixmap.scaled(self.width(), self.height(),QtCore.Qt.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)
        self.timer.stop()
        self.ready = True

    # Trick to get the image to maximum size
    def resizeEvent(self, evt):
        if self.init_size == 0:
            self.setbackgroundimage()
            self.init_size = 1

    def setbackgroundimage(self):
        self.ready = False
        wait_image = QtGui.QImage()
        wait_image.load(TRAIN_WAIT_IMAGE_BKG)
        pixmap = QtGui.QPixmap(wait_image)
        scaled_pixmap = pixmap.scaled(self.width(), self.height(),QtCore.Qt.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        if self.ready:
            self.clicked_sig.emit()


class TrainingView(QWidget):
    """ TrainingView class
    The widget is shown for training. It first show a wait image that needs to be 
    clicked on before playing the video. After the training video ended, the wait
    image is shown again. 
    The widget is composed of a stacked widget containing two widget, one WaitLabel
    widget used for the wait image, one Phonon VideoPlayer widget used for 
    playing the video.
    
        attributes:
            - stacked_widget     : Stacked widget containing the WaitLabel and VidPlayer widgets.
            - vid_player        : Phonon VideoPlayer class for playing the video.
            - wait_label        : WaitLabel class for showing the wait image.
            - subject          : Subject class containing the subject informations.
            - cur_vid_num         : Variable for counting the number of videos played.
            - condition         : Can be 'Fam' or 'New'.
            
        signals: 
            - exit_training_sig : Emitted when home button is pressed
            - training_over_sig : Emitted when the training is over
            - video_start_sig   : Emitted when a video starts
        
    """
    # Signals
    exit_training_sig = QtCore.pyqtSignal()
    training_over_sig = QtCore.pyqtSignal(str)
    video_start_sig = QtCore.pyqtSignal(int, str)  # Emitted when video starts (vid_num, vid_name)

    def __init__(self, fullscreen):
        self.subject = []
        self.condition = []
        self.soft_rules = []

        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)
        
        if fullscreen:
            screen_H = QDesktopWidget().screenGeometry().height()
        else:
            screen_H = MAIN_WINDOW_HEIGHT

        # Top Horizontal Layout (with Home Button)
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        hori_layout.addStretch(1)
        exit_btn = QtGui.QPushButton("Home")
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        exit_btn.setSizePolicy(size_policy)
        hori_layout.addWidget(exit_btn)

        # Main Layout - StackedWidget : Wait Label / Video Player
        layout.addLayout(hori_layout)
        self.stacked_widget = QtGui.QStackedWidget()
        page_title = QtGui.QLabel("Training")
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        page_title.setSizePolicy(size_policy)
        page_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(page_title)
        spacer_vert = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_vert)
        # Video player
        self.vid_player = Phonon.VideoPlayer()
        self.vid_player.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.vid_player.setFixedHeight(screen_H/RATIO_SCREEN_H_TRAINING_H)
        # Image for starting video
        self.wait_label = WaitLabel()
        self.wait_label.clicked_sig.connect(self.clicked_sig_received)
        self.wait_label.setFixedHeight(screen_H/RATIO_SCREEN_H_TRAINING_H)
        self.stacked_widget.addWidget(self.wait_label)
        self.stacked_widget.addWidget(self.vid_player)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.stacked_widget.setSizePolicy(size_policy)
        layout.addWidget(self.stacked_widget)
        self.setMaximumHeight(screen_H)   
        layout.addItem(spacer_vert)
        
        # Position in training videos
        self.cur_vid_num = 0
        # Video Player  
        self.vid_player.finished.connect(self.setnextvideo)

        exit_btn.clicked.connect(self.exittraining)

    def set_soft_rules(self, soft_rules):
        self.soft_rules = soft_rules

    def set_condition(self, condition):
        condition = condition.lower()
        if condition.lower() == "fam" or condition.lower() == "new":
            self.condition = condition
        else:
            raise ValueError('Wrong condition argument : {} -- Possibles values are [\'fam\' or \'new\']'.format(condition))
        
    def exittraining(self):
        self.cur_vid_num = 0  # Reset cur_vid_num
        self.exit_training_sig.emit()

    def setsubject(self, sub):
        self.subject = sub
        
    def loadmedia(self, media_path):
        media = Phonon.MediaSource(media_path)
        if media.type() == 1:
            logging.error('Invalid Media Source: {}'.format(media_path))
            print('Invalid Media Source: {}'.format(media_path))
        else:
            self.vid_player.load(media)
            
    def stopvideo(self):
        if self.vid_player.mediaObject():
            self.vid_player.stop()

    def pausevideo(self):
        if self.vid_player.isPlaying():
            self.vid_player.pause()

    def playvideo(self):
        if not self.vid_player.isPlaying():
            self.vid_player.play()
        
    def setnextvideo(self):
        # Wait (pause between 2 videos)
        if self.cur_vid_num > 0:
            time.sleep(1)
        
        # Training over
        n_trials_fam = self.soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] + self.soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] + self.soft_rules['N_REPET_OBJ_TRAIN_FAM_3']
        n_trials_new = self.soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] + self.soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] + self.soft_rules['N_REPET_OBJ_TRAIN_NEW_3']
        if self.condition == "fam" and self.cur_vid_num == n_trials_fam:
            logging.info('Training FAM over')
            print('Training FAM over')
            self.cur_vid_num = 0
            self.training_over_sig.emit("fam")
        elif self.condition == "new" and self.cur_vid_num == n_trials_new:
            logging.info('Training NEW over')
            print('Training NEW over')
            self.cur_vid_num = 0
            self.training_over_sig.emit("new")
        # Training continue    
        else:
            random_inst = TRAIN_INSTRUCTIONS[random.randint(0, 2)]
            # FAM
            if self.condition == "fam":
                vid_num = self.subject.train_vidorder_fam[self.cur_vid_num]  # get the training video number Fam
                obj_name = self.subject.getobjectname(vid_num)[0]
                vid_name = random_inst+'_'+obj_name+VIDEO_FORMAT
                vid_path = os.path.join(VIDEO_FAM_DIR, obj_name, vid_name)
            # NEW
            elif self.condition == "new":
                vid_num = self.subject.train_vidorder_new[self.cur_vid_num]  # get the training video number New
                asso_name, obj_name, pseudo_word = self.subject.getobjectname(vid_num)
                vid_name = random_inst+'_'+obj_name+'_'+pseudo_word+VIDEO_FORMAT
                vid_path = os.path.join(VIDEO_NEW_DIR, obj_name, pseudo_word, vid_name)

            self.loadmedia(vid_path)
            # Emit sig
            self.video_start_sig.emit(self.cur_vid_num, vid_name)
            self.cur_vid_num += 1
            self.wait_label.setbackgroundimage()
            self.wait_label.starttimer()
            self.stacked_widget.setCurrentIndex(0)

    def clicked_sig_received(self):
        self.playvideo()
        self.stacked_widget.setCurrentIndex(1)
