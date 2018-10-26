# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:06:07 2016

@author: deudon
"""

import os
import logging
import datetime
import codecs
from PyQt4 import QtCore
from PyQt4.QtGui import *
from startupview import StartupView
from formview import FormView
from trainingview import TrainingView
from testview import TestView
from versionselectionview import VersionSelectionView
from config import *


class MainWindow(QMainWindow):
    """ Main Window class 
    The main window is basically a Qt stacked widget containing the different widgets. 
    Only one widget can be viewed at a time. Given the user action, one or another 
    widget is selected and showed in the main window. For example when the user click
    the "Start Test Fam" button, the testView widget is selected. 
    
        attributes:
            - startup_view    : Startup view class - view at startup.
            - form_view       : Form view class - to enter subject's informations.
            - training_view   : Training view class - view for training.
            - test_view       : Test view class - view for testing.
            - stacked_widget   : Qt stacked widget which contains the 4 previous widgets (views).
            - subject        : Subject class - containt the current subject informations.
            - app_date         : Contain the current date when the software is launched.
            - app_time         : Contain the current time when the software is launched.
            - time_log_file     : File ID where all the time events are saved.
            - resultsFIle     : File ID where all the results are saved.
            
    """
    def __init__(self, app, fullscreen, fill_subject):
        self.app = app
        self.fullscreen = fullscreen
        self.version = []
        self.response_ver = []
        self.soft_rules = []

        QMainWindow.__init__(self)
        self.startup_view = StartupView()
        self.form_view = FormView(fill_subject)
        self.training_view = TrainingView(fullscreen)
        self.test_view = TestView(fullscreen)
        self.version_sel_view = VersionSelectionView()

        self.stacked_widget = QStackedWidget()

        self.stacked_widget.addWidget(self.version_sel_view)
        self.stacked_widget.addWidget(self.startup_view)
        self.stacked_widget.addWidget(self.form_view)
        self.stacked_widget.addWidget(self.training_view)
        self.stacked_widget.addWidget(self.test_view)
        self.setCentralWidget(self.stacked_widget)
        
        self.app_date = QtCore.QDate.currentDate()
        self.app_time = QtCore.QTime()
        self.time_log_file, self.result_file = [], []
        self.subject = []

        # Version selection view
        self.version_sel_view.quit_app_sig.connect(self.quit_app_sig_received)
        self.version_sel_view.version_selected_sig.connect(self.version_selected_received)
        # Startup View
        self.startup_view.start_form_sig.connect(lambda: self.stacked_widget.setCurrentIndex(GUI_FORM))
        self.startup_view.start_training_fam_sig.connect(lambda: self.starttraining("fam"))
        self.startup_view.start_training_new_sig.connect(lambda: self.starttraining("new"))
        self.startup_view.start_test_fam_sig.connect(lambda: self.starttesting("fam"))
        self.startup_view.start_test_new_sig.connect(lambda: self.starttesting("new"))
        self.startup_view.quit_app_sig.connect(self.quit_app_sig_received)
        # Form view
        self.form_view.form_over_sig.connect(self.form_over_sig_received)
        self.form_view.exit_form_sig.connect(self.exit_form_sig_received)        
        # Training view
        self.training_view.exit_training_sig.connect(self.exit_train_sig_received)
        self.training_view.training_over_sig.connect(self.training_over_sig_received)
        self.training_view.video_start_sig.connect(self.video_start_sig_received)
        # Test view
        self.test_view.exit_test_sig.connect(self.exit_test_sig_received)
        self.test_view.test_start_sig.connect(self.test_start_sig_received)
        self.test_view.test_response_sig.connect(self.test_response_sig_received)
        self.test_view.testing_over_sig.connect(self.testing_over_sig_received) 

    def version_selected_received(self, version, response_version):
        self.version = version
        self.response_ver = response_version
        self.soft_rules = load_soft_rules(version)
        self.form_view.set_soft_rules(self.soft_rules)
        self.test_view.set_soft_rules(self.soft_rules)
        self.training_view.set_soft_rules(self.soft_rules)
        self.test_view.set_version(version, response_version)
        self.form_view.set_version(version)
        logging.info('Version {} {}'.format(version, response_version))
        self.startup_view.set_title('DANA SOFT {} {}'.format(version, response_version))
        self.stacked_widget.setCurrentIndex(GUI_HOME)

    def createtextfiles(self):
        if self.subject:
            subject_dirpath = self.subject.result_dir
            # Time log file
            self.time_log_file = codecs.open(os.path.join(subject_dirpath, TIME_LOG_FILE_NAME), 'w', encoding='utf-8')
            # Add the time of the Application start
            self.time_log_file.write(SOFT_NAME+"\n"+str(self.app_date.toString("dd_MM_yy"))+"\n")
            logging.info(SOFT_NAME+"\n"+str(self.app_date.toString("dd_MM_yy"))+"\n")
            # Results file
            self.result_file = codecs.open(os.path.join(subject_dirpath, RESULTS_FILE_NAME), 'w', encoding='utf-8')
            self.result_file.write(SOFT_NAME+"\n"+str(self.app_date.toString("dd_MM_yy"))+"\n\n")
            self.result_file.write('AssoPos1,AssoPos2,AssoPos3,Cible,Reponse,Cible Pos,Reponse Pos,Temps Reaction (ms)\n')

    def form_over_sig_received(self, sub):
        self.stacked_widget.setCurrentIndex(GUI_HOME)
        # Assign subject here and to the training view
        self.subject = sub
        self.training_view.setsubject(sub)
        self.test_view.setsubject(sub)
        # Create results files
        self.createtextfiles()
        # Enable buttons
        self.startup_view.enablebuttons(1)

    def starttraining(self, novelty):
        # Create pseudo-random order for training videos
        self.subject.create_train_sequence(novelty)
        if novelty.lower() in ['fam', 'new']:
            self.subject.write_train_sequence(novelty)
            # Add start of training to timeLog
            self.addtimeevent('\nTraining {} start'.format(novelty.upper()), None)
            self.result_file.write('\nTrain{} START\n'.format(novelty.capitalize()))
            if 'explicit' in self.version:
                condition = novelty
                self.training_view.set_condition(condition)
                # Load first training video
                self.training_view.setnextvideo()
                self.stacked_widget.setCurrentIndex(GUI_TRAINING)
            elif self.version in ['fast-mapping', 'scrambled-2y', 'scrambled-4y', 'simon', 'simon-easy']:
                if self.version in ['scrambled-2y', 'scrambled-4y']:
                    self.test_view.set_version(self.version, 'visual')
                    self.response_ver = 'visual'
                condition = '{}_train_{}'.format(self.version, novelty)
                self.test_view.set_condition(condition)
                self.test_view.setaudio()
                self.test_view.setimages()
                self.test_view.setanimation()
                self.stacked_widget.setCurrentIndex(GUI_TEST)
                if self.response_ver == 'visual' and self.version not in ['scrambled-2y', 'scrambled-4y']:
                    self.test_view.starttrial()
        else:
            raise ValueError('Wrong novelty : {} - Possibles values are [\'fam\' or \'new\']')

    def starttesting(self, novelty):
        # Create pseudo-random order for test videos
        self.subject.create_test_sequence(novelty)
        # Set condition
        self.test_view.set_condition('test_{}'.format(novelty))
        # In scrambled versions, training is visual and testing is tactile
        if self.version in ['scrambled-2y', 'scrambled-4y']:
            self.test_view.set_version(self.version, 'tactile')
            self.response_ver = 'tactile'
        if novelty.lower() in ['fam', 'new']:
            self.subject.write_test_sequence(novelty)
            # Add start of training to timeLog
            self.addtimeevent('\nTesting {} start'.format(novelty.upper()), None)
        else:
            raise ValueError('Wrong condition : {} - Possibles values are [\'fam\' or \'new\']')
        self.result_file.write('\nTest{} START\n'.format(novelty.capitalize()))
        self.test_view.setaudio()
        self.test_view.setimages()
        self.test_view.setanimation()
        self.stacked_widget.setCurrentIndex(GUI_TEST)
        if self.response_ver == 'visual':
            self.test_view.starttrial()
        
    def exit_form_sig_received(self):
        self.stacked_widget.setCurrentIndex(GUI_HOME)
        
    def exit_train_sig_received(self):
        conf_widget = QWidget()
        self.training_view.pausevideo()
        quit_training = QMessageBox.question(conf_widget, SOFT_NAME, 'Stop the training ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if quit_training == QMessageBox.Yes:
            self.training_view.stopvideo()
            self.addtimeevent('---------- TRAINING ABORTED ----------', None)
            self.stacked_widget.setCurrentIndex(GUI_HOME)
        else:
            self.training_view.playvideo()
        
    def exit_test_sig_received(self):
        conf_widget = QWidget()
        self.test_view.pause()
        quit_training = QMessageBox.question(conf_widget, SOFT_NAME, 'Stop the testing ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if quit_training == QMessageBox.Yes:
            self.test_view.reset()
            self.addtimeevent('---------- TESTING ABORTED ----------', None)
            self.stacked_widget.setCurrentIndex(GUI_HOME)
        else:
            self.test_view.resume()

    def test_start_sig_received(self, trial_num):
        self.addtimeevent("Trial #"+str(trial_num), None)

    def test_response_sig_received(self, reaction_time, asso_pos1, asso_pos2, asso_pos3, asso_target, asso_response, target_pos, response_pos):
        self.addtimeevent("Response", str(reaction_time)+'ms')
        # Add the result to the result file
        result_text = asso_pos1+','+asso_pos2+','+asso_pos3+','+asso_target+','+asso_response+','+str(target_pos)+','+str(response_pos)+','+str(reaction_time)+'\n'
        self.result_file.write(result_text)
            
    def video_start_sig_received(self, vid_num, vid_name):
        self.addtimeevent("video #"+str(vid_num), vid_name)
        
    def training_over_sig_received(self, condition):
        self.addtimeevent("Training"+condition+"Over", None)
        self.stacked_widget.setCurrentIndex(GUI_HOME)

    def testing_over_sig_received(self):
        self.addtimeevent("Testing Over", None)
        self.stacked_widget.setCurrentIndex(GUI_HOME)

    def starttimer(self):
        self.app_time.start()

    def addtimeevent(self, event_description, event_opt):
        time_log = datetime.datetime.now().strftime('%Hh%Mm%Ss-%f')[:-3]
        logging.debug('{} - {}'.format(event_description, time_log))
        ms_elapsed = self.app_time.elapsed()
        time_elapsed = QtCore.QTime()
        time_elapsed = time_elapsed.addMSecs(ms_elapsed)
        if time_elapsed.hour() > 0:
            time_elapsed_str = time_elapsed.toString("HH:mm:ss:zzz")
        else:
            time_elapsed_str = time_elapsed.toString("mm:ss:zzz")
        current_time = QtCore.QTime.currentTime()
        current_time_str = current_time.toString(QtCore.QString("HH:mm:ss:zzz"))     
        if not event_opt:
            event_opt = ''
        event_str = event_description+","+current_time_str+","+time_elapsed_str+','+event_opt+"\n"
        self.time_log_file.write(event_str)

    def quit_app_sig_received(self):
        conf_widget = QWidget()
        quit_app = QMessageBox.question(conf_widget, SOFT_NAME, 'Exit Application ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if quit_app == QMessageBox.Yes:
            self.app.quit()


