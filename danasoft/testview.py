# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 10:27:42 2016

@author: deudon
"""
import os
from random import randint
import time
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
from PyQt4.QtGui import *
from config import *


class ClickableImage(QtGui.QLabel):
    """ ClickableImage class - inheriting from QLabel
    Qt QLabel widget showing a test image that can responds to click events.

        attributes:
            - image         : Image shown on this widget.
            - pos           : Position of this widget on the test view.

        signals:
            - clicked_sig   : Emitted when user clicks on the widget

    """
    image       = None
    pos         = None
    is_reactive = False
    # signal
    clicked_sig = QtCore.pyqtSignal(int)

    def __init__(self, image_path, pos, black_background, wait_image):
        """ Load the image, put it in the label """
        QtGui.QLabel.__init__(self)
        self.image = QtGui.QImage()
        self.image.load(image_path)
        self.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(self.image)
        self.pos = pos
        if black_background:
            self.setStyleSheet("QLabel {background-color:black}")
        size_policy_im = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        # Resize the wait_image so that it keeps the same size whatever the screen resolution is
        if wait_image:
            if self.isFullScreen():
                screen_h = QDesktopWidget().screenGeometry().height()
            else:
                screen_h = MAIN_WINDOW_HEIGHT
            pixmap = pixmap.scaledToHeight(screen_h/RATIO_SCREEN_H_WAITIMAGE_H)
        self.setPixmap(pixmap)
        self.setSizePolicy(size_policy_im)
        self.is_reactive = False

    def mousePressEvent(self, event):
        """ Emit a clicked_sig signal when the widget is clicked """
        self.clicked_sig.emit(self.pos)

    def set_reactivity(self, reactivity):
        self.is_reactive = reactivity

    def setimage(self, image_path):
        """ Load an image, rescale it and put it in the Qt label """
        self.image.load(image_path)                          # Load image
        pixmap = QtGui.QPixmap(self.image)            # Get pixmap
        if self.isFullScreen():
            screenW = QDesktopWidget().screenGeometry().width()
        else:
            screenW = MAIN_WINDOW_WIDTH
        # Rescale pixmap given the main window size and keep aspect ratio
        scaled_pixmap = pixmap.scaledToWidth(screenW/RATIO_SCREEN_W_IMAGE_W)
        self.setPixmap(scaled_pixmap)

          
class QTimerWithPause(QtCore.QTimer):
    """ QTimerWithPause class - Inherits from QTimer
    Same thing as a QTimer but the timer can be paused and resumed.
 
        attributes:
            - start_time     : Stock the time when the timer is started.
            - remaining_time    : Stock the remaining time.
    
        methods:
            - __init__      : Initialize the QTimer.
            - start_timer    : Start the timer. Keep track of the starting time.
            - pause         : Pause the timer. Compute the remaining time.
            - resume        : Resume the timer given the remaining time.
    """
    
    def __init__(self, parent=None):
        QtCore.QTimer.__init__(self, parent)
        self.start_time = 0
        self.remaining_time = 0
        
    def start_timer(self, remaining_time):
        self.remaining_time = remaining_time
        self.start_time = time.time()
        QtCore.QTimer.start(self, remaining_time)   
        
    def pause(self):
        if self.isActive():
            self.stop()
            elapsed_time = time.time() - self.start_time
            # time() returns float secs, interval is int msec
            self.remaining_time = self.remaining_time - int(elapsed_time*1000)

    def resume(self):
        if not self.isActive():
            self.start_time = time.time()
            self.start(self.remaining_time)
            

class TestView(QtGui.QWidget):
    """ TestView class
    The test view is showed when testing the subject either with familiar or new objects.
    It is composed of a stacked_widget containing three widgets, one for the waiting 
    image, one for showing the test images, and the third one for playing the 
    animation between two tests. 
    When user click on the home button, a confirmation box pops up, the audio or animation
    is paused, if the user decides to go back to the test, the audio or animation 
    is resumed and the "pause" duration is measured. This pause duration is substracted
    from the reaction time. 
    
        attributes:
            - stacked_widget     : Stacked widget containing 3 widgets, the first one
            for the waiting image, the second one for showing the test images,
            the third one for playing the animation
            - im1               : First test image.
            - im2               : Second test image.
            - im3               : Third test image
            - i_trial            : Variable for incrementing trial number.
            - condition         : Can be either 'Fam' or 'New'.
            - subject          : Subject class 
            - audio_output       : Phonon audio output for playing instructions.
            - audio_media        : Phonon media object for audio.
            - animation_player   : Phonon video player.
            - test_time          : Time for measuring response time.
            - repeat_timer       : QTimerWithPause. Timer for repeating audio 
            instruction after a while.
            - next_trial_timer    : QTimerWithPause. If response is visual only, 
            timer for going to the next trial.
            - pause_start_time    : QTime (clock) for measuring pause duration (when click on home button)
            - pause_duration_ms   : Total pause duration in ms
  
      signals:
          - exit_test_sig       : Emitted when user clicks the home button
          - test_start_sig      : Emitted when a trial starts
          - test_response_sig   : Emitted for sending the response to main window
          after subject responded, for visual response after next_trial_timer is finished
          - testing_over_sig    : Emitted when the last trial ends
          
    """
    # Signals
    exit_test_sig = QtCore.pyqtSignal()
    test_start_sig = QtCore.pyqtSignal(int)
    test_response_sig = QtCore.pyqtSignal(int, str, str, str, str, str, int, int)
    # test response sig arguments : RT,AssoPos1,AssoPos2,asso_target,asso_response,TargetPos,response_pos
    testing_over_sig = QtCore.pyqtSignal()

    def __init__(self, n_objects=3):
        # These attributes are set when the method setsubject is called
        self.subject = []
        self.n_objects = n_objects
        self.n_trials = []
        self.version = []
        self.response_ver = []
        self.condition = []
        self.soft_rules = []

        # Gui
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)

        # Get the height of the widget
        screen_h = QDesktopWidget().screenGeometry().height() if self.isFullScreen() else MAIN_WINDOW_HEIGHT
                
        # Top Horizontal Layout (with Home Button)
        top_hori_layout = QtGui.QHBoxLayout()
        top_hori_layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        top_hori_layout.addStretch(1)
        exit_btn = QtGui.QPushButton("Home")
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        exit_btn.setSizePolicy(size_policy)
        top_hori_layout.addWidget(exit_btn)
        layout.addLayout(top_hori_layout)

        # Page title
        page_title = QtGui.QLabel("TESTING")
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        page_title.setSizePolicy(size_policy)
        page_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(page_title)
     
        # Central stacked widget : Wait Image / Test Images / Animation (Phonon VideoPlayer)
        self.stacked_widget = QtGui.QStackedWidget()
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.stacked_widget.setSizePolicy(size_policy)
        self.stacked_widget.setMaximumHeight(0.9*screen_h)
        # Fill the central stacked widget
        # Wait image 
        wait_image = ClickableImage(TEST_WAIT_IM_PATH, -1, False, True)
        wait_image.clicked_sig.connect(self.wait_image_clicked)
        self.stacked_widget.addWidget(wait_image)
        # Images widget
        images_widget, self.im_list = create_images_widget(screen_h)
        self.stacked_widget.addWidget(images_widget)
        # Phonon audio player
        self.audioOuput = Phonon.AudioOutput(Phonon.MusicCategory)
        self.audio_media = Phonon.MediaObject()
        Phonon.createPath(self.audio_media, self.audioOuput)
        # Animation Phonon video player
        self.animation_player, animation_widget = create_animation_widget(screen_h)
        self.animation_player.finished.connect(self.animation_finished)
        # Add it to the stacked widget
        self.stacked_widget.addWidget(animation_widget)
        # Feedback image widget
        # im_feedback_widget = create_image_feedback_widget()
        im_feedback_widget = QtGui.QWidget()
        im_feedback_layout = QtGui.QHBoxLayout()
        spacer_item_hori = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        im_feedback_layout.addItem(spacer_item_hori)
        self.im_feedback = QtGui.QLabel(im_feedback_widget)
        self.im_feedback.setAlignment(QtCore.Qt.AlignCenter)
        im_feedback_layout.addWidget(self.im_feedback)
        im_feedback_layout.addItem(spacer_item_hori)
        im_feedback_widget.setLayout(im_feedback_layout)
        self.stacked_widget.addWidget(im_feedback_widget)
        self.feedback_timer = QTimerWithPause()

        # Main layout
        spacer_item_vert = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer_item_vert)
        layout.addWidget(self.stacked_widget)
        layout.addItem(spacer_item_vert)

        # Trial increment
        self.i_trial = 0
        # Time  (for reaction time) and Timer for repeating audio
        self.test_time = QtCore.QTime()
        self.repeat_timer = QTimerWithPause()
        self.next_trial_timer = []

        # Time clock for measure the pause duration
        self.pause_start_time = QtCore.QTime()
        self.pause_duration_ms = 0

        # Signals
        exit_btn.clicked.connect(lambda: self.exit_test_sig.emit())

    def set_soft_rules(self, soft_rules):
        self.soft_rules = soft_rules

    def set_version(self, version, response_version):
        self.version = version
        self.response_ver = response_version
        if response_version == 'visual':
            self.next_trial_timer = QTimerWithPause()
            self.stacked_widget.setCurrentIndex(1)
            for i in range(self.n_objects):
                if self.im_list[i].is_reactive:
                    self.im_list[i].clicked_sig.disconnect()
                    self.im_list[i].set_reactivity(0)
        else:
            self.stacked_widget.setCurrentIndex(0)
            for i in range(self.n_objects):
                self.im_list[i].clicked_sig.connect(self.test_image_clicked)
                self.im_list[i].set_reactivity(1)

    def set_condition(self, condition):
        condition = condition.lower()
        self.condition = condition
        if self.condition == 'test_fam':
            self.n_trials = self.subject.test_objinpos_fam.shape[0]
        elif self.condition == 'test_new':
            self.n_trials = self.subject.test_objinpos_new.shape[0]
        elif self.condition in ['fast-mapping_train_fam', 'scrambled-2y_train_fam', 'scrambled-4y_train_fam', 'simon_train_fam', 'simon-easy_train_fam']:
            self.n_trials = self.subject.train_objinpos_fam.shape[0]
        elif self.condition in ['fast-mapping_train_new', 'scrambled-2y_train_new', 'scrambled-4y_train_new', 'simon_train_new', 'simon-easy_train_new']:
            self.n_trials = self.subject.train_objinpos_new.shape[0]
        else:
            raise ValueError('Wrong condition argument : {} -- Possibles values are [\'fam\' or \'new\']'.format(condition))

    def reset(self):
        """
        Reset all the parameters to start again the testing : 
            - Set the trial counter variable to 0.
            - If current widget is test images, stop and disconnect the repeat_timer.
            - If visual response, stop and disconnect the next_trial_timer.
            - Set the pause duration to 0
            - Stop the animation player.
            - Clear the audio media.
            - Set the current widget to the wait_image widget.
        """
        self.i_trial = 0
        if self.stacked_widget.currentIndex() == 1:
            if self.condition not in ['scrambled-2y_train_fam', 'scrambled-2y_train_new', 'scrambled-4y_train_fam', 'scrambled-4y_train_new']:
                self.repeat_timer.stop()
                self.repeat_timer.timeout.disconnect()
        if self.response_ver == 'visual' and self.stacked_widget.currentIndex() == 1:
            self.next_trial_timer.stop()
            self.next_trial_timer.timeout.disconnect()
        self.pause_duration_ms = 0
        self.animation_player.stop()
        self.audio_media.clear()
        self.stacked_widget.setCurrentIndex(0)

    def setimages(self):
        """ Given the condition and the trial number, put the corresponding images on the ClickableImage widgets """
        # Get the the object name at each position
        for i in range(self.n_objects):
            obj_num, asso_name_i, objname_i, _ = self.subject.getobjectinpos(i, self.i_trial, self.condition)
            _, target_name_i = self.subject.gettargetname(self.i_trial, self.condition)
            if self.condition in ['scrambled-2y_train_fam', 'scrambled-2y_train_new', 'scrambled-4y_train_fam', 'scrambled-4y_train_new']:
                if obj_num < 0:  # Fam objects
                    im_dir_path = IMAGE_FAM_DIR if objname_i == target_name_i else IMAGE_FAM_SCRAMBLED_DIR
                    objpath_i = os.path.join(im_dir_path, objname_i + IMAGE_FORMAT)
                else:  # New objects
                    im_dir_path = IMAGE_NEW_DIR if asso_name_i == target_name_i else IMAGE_NEW_SCRAMBLED_DIR
                    objpath_i = os.path.join(im_dir_path, objname_i + IMAGE_FORMAT)
            else:
                if obj_num < 0:  # Fam objects
                    objpath_i = os.path.join(IMAGE_FAM_DIR, objname_i+IMAGE_FORMAT)
                else:  # New objects
                    objpath_i = os.path.join(IMAGE_NEW_DIR, objname_i+IMAGE_FORMAT)
            self.im_list[i].setimage(objpath_i)

    def setanimation(self):
        """ Randomly choose an animation and load it in the animation_player """
        animation_str = 'animation_'+str(randint(1, N_ANIMATION)) + VIDEO_FORMAT
        animation_media = Phonon.MediaSource(os.path.join(ANIMATION_DIR, animation_str))
        self.animation_player.load(animation_media)
        
    def animation_finished(self):
        """ Called when animation is over :
            - stop the animation player.
            - if response is visual, start the next trial.
            - else, set the current widget to the wait image.
            - prepare another animation.
        """
        self.animation_player.stop()
        if self.response_ver == 'visual':
            self.starttrial()  # Start next trial
        else:
            self.stacked_widget.setCurrentIndex(0)
        self.setanimation()

    def pause(self):
        """ Called when user click on the home button
        If the current view is the test images:
            - Pause the audio.
            - Pause the repeat_timer.
            - If visual response, also pause the next_trial_timer
            - Measure the pause duration, start the pause_start_time QTime
        If the current view is the animation
            - Pause the animation
        """
        if self.stacked_widget.currentIndex() == 1:   # Test images
            self.audio_media.pause()                   # stop the audio
            self.repeat_timer.pause()                 # pause the repeat audio timer
            self.pause_start_time.start()
            if self.response_ver == 'visual':
                self.next_trial_timer.pause()
        elif self.stacked_widget.currentIndex() == 2:  # Animation
            self.animation_player.pause()
        elif self.stacked_widget.currentIndex() == 3:  # Feedback widget
            self.audio_media.pause()
            self.feedback_timer.pause()
            self.pause_start_time.start()

    def resume(self):
        """ Called when user click on the home button and change his mind
        If the current view is the test images:
            - Resume the audio.
            - Resume the repeat_timer.
            - If visual response, also resume the next_trial_timer
        If the current view is the animation
            - Resume the animation
        """
        if self.stacked_widget.currentIndex() == 1:    # Test images
            self.audio_media.play()                    # restart the audio
            self.repeat_timer.resume()                 # restart the repeat timer
            self.pause_duration_ms += self.pause_start_time.elapsed()
            if self.response_ver == 'visual':
                self.next_trial_timer.resume()
        elif self.stacked_widget.currentIndex() == 2:   # Animation
            self.animation_player.play()
        elif self.stacked_widget.currentIndex() == 3:  # Feedback widget
            self.audio_media.play()
            self.feedback_timer.resume()
            self.pause_duration_ms += self.pause_start_time.elapsed()

    def repeataudio(self):
        """ Called when the repeat_timer is over.
        Load an new instruction and re-init the repeat_timer.
        """
        self.setaudio()
        self.audio_media.play()
        # Re-init the repeat timer
        self.repeat_timer.start(AUDIO_REPEAT_TIME_MS)

    def setsubject(self, sub):
        """ Set the current subject to the class """
        self.subject = sub
        self.n_objects = sub.n_objects

    def exit_button_clicked(self):
        """ Emitted when the "home" button is clicked """
        self.exit_test_sig.emit()

    def setnexttrial(self):
        """ Prepare next trial :
            - Disconnect the repeat timer, and the nextTrial timer (if visual response and not scrambled ver)
            - Increment trial number
            - If end of testing, quit test view
            - else set up next trial
            - Switch and play animation
        """
        if self.condition in ['simon_train_fam', 'simon-easy_train_fam', 'simon_train_new', 'simon-easy_train_new']:
            self.feedback_timer.timeout.disconnect()
        elif self.condition not in ['scrambled-2y_train_fam', 'scrambled-2y_train_new', 'scrambled-4y_train_fam', 'scrambled-4y_train_new']:
            # Disconnect the repeat timer
            try:
                self.repeat_timer.timeout.disconnect()
            except:
                print('repeat_timer already disconnected')
        # If visual response disconnect next trial timer
        if self.response_ver == 'visual':
            self.sendresponse(-1, -1)
            self.next_trial_timer.timeout.disconnect()
        # Increment trial number
        self.i_trial += 1
        # End of testing
        if self.i_trial == self.n_trials:
            self.i_trial = 0
            self.stacked_widget.setCurrentIndex(0)
            self.audio_media.clear()
            self.testing_over_sig.emit()
        # Set up next trial
        else:
            self.setimages()
            self.setaudio()
            # Switch to the animation
            self.stacked_widget.setCurrentIndex(2)
            # Play animation
            self.animation_player.play()

    def starttrial(self):
        """ Start a trial
            - Send a signal to the main window for time log
            - Set the pause time to 0
            - Start the test_time clock
            - Start repeat timer and next_trial_timer (if visual response)
            - Switch the stacked widget index to the test images
            - Start the audio
        """
        # Send signal for time log
        self.test_start_sig.emit(self.i_trial+1)
        # Set the pause time to 0
        self.pause_duration_ms = 0
        # Start clock
        self.test_time.start()
        if self.condition not in ['scrambled-2y_train_fam', 'scrambled-2y_train_new', 'scrambled-4y_train_fam', 'scrambled-4y_train_new']:
            self.repeat_timer.timeout.connect(self.repeataudio)
            self.repeat_timer.start_timer(AUDIO_REPEAT_TIME_MS)
        # If only visual response, start the timer for next trial
        if self.response_ver == 'visual':
            self.next_trial_timer.timeout.connect(self.setnexttrial)
            if self.version == 'scrambled-2y':
                self.next_trial_timer.start_timer(TEST_CONTINUE_DELAY_SCRAMBLED_2Y)
            elif self.version == 'scrambled-4y':
                self.next_trial_timer.start_timer(TEST_CONTINUE_DELAY_SCRAMBLED_4Y)
            else:
                self.next_trial_timer.start_timer(TEST_CONTINUE_DELAY)
        else:
            try:
                self.next_trial_timer.timeout.disconnect()
            except:
                print('next_trial_timer already disconnected')
        # Switch to the test images
        self.stacked_widget.setCurrentIndex(1)
        # Start the audio
        self.audio_media.play()

    def test_image_clicked(self, response_pos):
        """ Called when a test image is clicked.
        Accept only the responses happening MIN_REACTION_TIME_MS ms after the start of the trial.
        Calcul the reaction time as the elpased time since the beginning of the trial,
        if the response is not too early, send the response. Prepare next trial.
        The "pause" duration (if any) is substracted from the reaction time
        """
        reaction_time = self.test_time.elapsed()-self.pause_duration_ms
        if reaction_time > MIN_REACTION_TIME_MS:
            _, asso_target = self.subject.gettargetname(self.i_trial, self.condition)
            _, asso_response, _, _ = self.subject.getobjectinpos(response_pos - 1, self.i_trial, self.condition)
            good_response = asso_response == asso_target
            if (self.condition in ['test_fam'] and self.soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM']) or \
                    (self.condition in ['fast-mapping_train_fam'] and self.soft_rules['WAIT_GOOD_RESPONSE_TRAIN_FAM']) or \
                    (self.condition in ['fast-mapping_train_new'] and self.soft_rules['WAIT_GOOD_RESPONSE_TRAIN_NEW']):
                if not good_response:
                    return
            self.sendresponse(response_pos, reaction_time)
            # Set next trial
            if self.version in ['explicit', 'scrambled-2y', 'scrambled-4y', 'fast-mapping', 'explicit-1rep']:
                self.setnexttrial()
            elif self.version in ['simon', 'simon-easy']:
                if self.condition in ['simon_train_fam', 'simon-easy_train_fam', 'simon_train_new', 'simon-easy_train_new']:
                    # target_pos = self.subject.gettargetpos(self.i_trial, self.condition)
                    obj_target = asso_target if 'fam' in self.condition else '_'.join(asso_target.split('_')[:-1])
                    self.send_feedback(good_response, obj_target)
                else:
                    self.setnexttrial()
        else:
            print "Response too early"

    def send_feedback(self, correct_response, obj_target):
        # Disconnect the repeat timer
        self.repeat_timer.timeout.disconnect()
        self.set_image_feedback(correct_response)
        self.stacked_widget.setCurrentIndex(3)  # Feedback image
        # Start timer
        self.feedback_timer.start_timer(FEEDBACK_TIME_MS)
        if self.version == 'simon-easy' and not correct_response:
            self.feedback_timer.timeout.connect(lambda: self.show_correct_image(obj_target))
        else:
            self.feedback_timer.timeout.connect(self.setnexttrial)
        # Play audio feedback
        self.setaudiofeedback(correct_response)
        self.audio_media.play()

    def set_image_feedback(self, correct_response):
        screen_h = QDesktopWidget().screenGeometry().height() if self.isFullScreen() else MAIN_WINDOW_HEIGHT
        if correct_response:
            self.im_feedback.setPixmap(QtGui.QPixmap(IM_POSITIF_FEEDBACK).scaledToHeight(int(screen_h*IMAGE_FEEDBACK_PROP_H)))
            # self.im_feedback.setPixmap(QtGui.QPixmap(IM_POSITIF_FEEDBACK))
        else:
            self.im_feedback.setPixmap(QtGui.QPixmap(IM_NEGATIF_FEEDBACK).scaledToHeight(int(screen_h*IMAGE_FEEDBACK_PROP_H)))
            # self.im_feedback.setPixmap(QtGui.QPixmap(IM_NEGATIF_FEEDBACK))

    def show_correct_image(self, obj_target):
        self.feedback_timer.timeout.disconnect()
        self.feedback_timer.timeout.connect(self.setnexttrial)
        self.feedback_timer.start_timer(CORRECT_IM_SHOW_MS)
        if 'fam' in self.condition:
            im_target = os.path.join(IMAGE_FAM_DIR, '{}{}'.format(obj_target, IMAGE_FORMAT))
        elif 'new' in self.condition:
            im_target = os.path.join(IMAGE_NEW_DIR, '{}{}'.format(obj_target, IMAGE_FORMAT))
        screen_h = QDesktopWidget().screenGeometry().height() if self.isFullScreen() else MAIN_WINDOW_HEIGHT
        self.im_feedback.setPixmap(QtGui.QPixmap(im_target).scaledToHeight(int(screen_h*0.4)))
        self.audio_media.setCurrentSource(Phonon.MediaSource(CORRECT_IM_SHOW_AUDIOPATH))
        self.audio_media.play()

    def setaudiofeedback(self, correct_response):
        if correct_response:
            audio_dirpath = os.path.join(AUDIO_FEEDBACK_DIR, 'positif')
            rand_filename = '{}.wav'.format(randint(1, N_POSITIF_AUDIO_FEEDBACKS))
        else:
            audio_dirpath = os.path.join(AUDIO_FEEDBACK_DIR, 'negatif')
            rand_filename = '{}.wav'.format(randint(1, N_NEGATIF_AUDIO_FEEDBACKS))
        audio_filepath = os.path.join(audio_dirpath, rand_filename)
        self.audio_media.setCurrentSource(Phonon.MediaSource(audio_filepath))

    def setaudio(self):
        """ Choose randomly an audio instruction. Set it to the audio player """
        self.audio_media.clear()
        # Get the number ot the target object
        obj_target_num, _ = self.subject.gettargetname(self.i_trial, self.condition)
        # Choose randomly an instruction
        if self.condition in ['scrambled-2y_train_fam', 'scrambled-2y_train_new', 'scrambled-4y_train_fam', 'scrambled-4y_train_new']:
            test_inst_str = TRAIN_INSTRUCTIONS_SCRAMBLED[randint(0, 2)]
        elif self.response_ver == 'visual':
            test_inst_str = TEST_INSTRUCTIONS_POINTAGE[randint(0, 2)]
        else:
            test_inst_str = TEST_INSTRUCTIONS_TACTILE[randint(0, 2)]
        # Get audio path
        if obj_target_num < 0:  # Familiar objects
            if self.condition == 'scrambled-2y_train_fam':
                audio_dir_path = AUDIO_FAM_SCRAMBLED_2Y_DIR
            elif self.condition == 'scrambled-4y_train_fam':
                audio_dir_path = AUDIO_FAM_SCRAMBLED_4Y_DIR
            else:
                audio_dir_path = AUDIO_FAM_DIR
            obj_name = self.subject.getobjectname(obj_target_num)[0]
            audio_path = os.path.join(audio_dir_path, obj_name, test_inst_str+'_'+obj_name+AUDIO_FORMAT)
        else:  # New objects
            if self.condition == 'scrambled-2y_train_new':
                audio_dir_path = AUDIO_NEW_SCRAMBLED_2Y_DIR
            elif self.condition == 'scrambled-4y_train_new':
                audio_dir_path = AUDIO_NEW_SCRAMBLED_4Y_DIR
            else:
                audio_dir_path = AUDIO_NEW_DIR
            _, _, pseudo_word = self.subject.getobjectname(obj_target_num)
            audio_path = os.path.join(audio_dir_path, pseudo_word, test_inst_str+'_'+pseudo_word+AUDIO_FORMAT)
        self.audio_media.setCurrentSource(Phonon.MediaSource(audio_path))

    def wait_image_clicked(self):
        """ called when the wait_image is clicked.
        There is no wait image for visual condition.
        If tactile condition, start next trial.
        """
        print "wait Image clicked - Start test trial"
        # if self.response_ver == 'visual':
        #     self.next_trial_timer.timeout.connect(self.setnexttrial)
        self.starttrial()

    def sendresponse(self, response_pos, reaction_time):
        _, asso_pos_1, _, _ = self.subject.getobjectinpos(0, self.i_trial, self.condition)
        _, asso_pos_2, _, _ = self.subject.getobjectinpos(1, self.i_trial, self.condition)
        _, asso_pos_3, _, _ = self.subject.getobjectinpos(2, self.i_trial, self.condition)
        if self.response_ver == 'visual':
            asso_response = '-1'
            reaction_time = -1
        else:
            _, asso_response, _, _ = self.subject.getobjectinpos(response_pos-1, self.i_trial, self.condition)
        target_pos = self.subject.gettargetpos(self.i_trial, self.condition)
        _, asso_target, _, _ = self.subject.getobjectinpos(target_pos-1, self.i_trial, self.condition)

        self.test_response_sig.emit(reaction_time, asso_pos_1, asso_pos_2, asso_pos_3, asso_target, asso_response,
                                    target_pos, response_pos)


def create_images_widget(screen_h):
    # Images widget
    images_widget = QtGui.QWidget()
    im1 = ClickableImage(TRAIN_WAIT_IMAGE, 1, True, False)
    im2 = ClickableImage(TRAIN_WAIT_IMAGE, 2, True, False)
    im3 = ClickableImage(TRAIN_WAIT_IMAGE, 3, True, False)
    # Layout for test images
    image_layout = QVBoxLayout()
    im_top_layout = QHBoxLayout()
    im_top_layout.addStretch(1)
    im_top_layout.addWidget(im2)
    im_top_layout.addStretch(1)
    im_bottom_layout = QHBoxLayout()
    im_bottom_layout.addStretch(1)
    im_bottom_layout.addWidget(im1)
    im_bottom_layout.addStretch(TEST_IMAGE_SPACING_HORI_FACTOR)
    im_bottom_layout.addWidget(im3)
    im_bottom_layout.addStretch(1)
    image_layout.addLayout(im_top_layout)
    image_layout.addStretch(100)
    image_layout.addLayout(im_bottom_layout)
    image_layout.setSpacing(screen_h/RATIO_SCREEN_H_VERT_SPACING_TEST)
    image_layout.setMargin(screen_h/20)
    images_widget.setLayout(image_layout)
    return images_widget, [im1, im2, im3]


def create_animation_widget(screen_h):
    # Create the Phonon video player
    animation_player = Phonon.VideoPlayer()
    animation_player.setStyleSheet("QLabel {background-color:blue}")
    size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    animation_player.setSizePolicy(size_policy)
    # The animation size is a square
    animation_player.setFixedSize(screen_h / RATIO_SCREEN_H_ANIMATION_H, screen_h / RATIO_SCREEN_H_ANIMATION_H)
    animation_widget = QtGui.QWidget()
    animation_layout = QtGui.QHBoxLayout()
    spacer_item_1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    spacer_item_2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
    animation_layout.addItem(spacer_item_1)
    animation_layout.addWidget(animation_player)
    animation_layout.addItem(spacer_item_2)
    animation_widget.setLayout(animation_layout)
    return animation_player, animation_widget

