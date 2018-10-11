# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:07:24 2016

@author: deudon
"""
import os

SOFT_NAME = "Dana Soft"

DATA_PATH = r'C:\Users\deudon\Desktop\M4\ProjetDanae\DanaSoft\data\\'

# Get root dir path - data directory should be placed on the DanaSoft root directory
ROOT_DIR_PATH, tail = os.path.split(DATA_PATH)
if not tail:
    ROOT_DIR_PATH, _ = os.path.split(ROOT_DIR_PATH)
LOG_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'log')
if not os.path.exists(LOG_DIR_PATH):
    os.mkdir(LOG_DIR_PATH)

################ Soft Rules ##################
# Waiting time for visual mode
TEST_CONTINUE_DELAY = 4000
TEST_CONTINUE_DELAY_SCRAMBLED_2Y = 5600
TEST_CONTINUE_DELAY_SCRAMBLED_4Y = 4500
# If not fullscreen, dimensions of the main window
MAIN_WINDOW_WIDTH = 800         # Must be inferior to the screen resolution width
MAIN_WINDOW_HEIGHT = 600        # Must be inferior to the screen resolution heigh

# TRAINING PARAMETERS
RATIO_SCREEN_H_TRAINING_H = 1.2   # Ratio between screen height and training view height (video)

# Warning : If too low, test images will be cut !
AUDIO_REPEAT_TIME_MS        = 7000  # Time between 2 repetition of the audio instruction (ms)
MIN_REACTION_TIME_MS        = 3000  # Minimal reaction time, responses before this will not be consider (ms)

#############################################
GUI_VER_SELECTION   = 0
GUI_HOME            = 1
GUI_FORM            = 2
GUI_TRAINING        = 3
GUI_TEST            = 4
GUI_RESULTS         = 5

# GUI - TEST View
RATIO_SCREEN_W_IMAGE_W = 3.5          # The test images will have the width of the main window divided by this value
RATIO_SCREEN_H_WAITIMAGE_H = 5        # Ratio between the height of the screen and the height of the wait image
RATIO_SCREEN_H_ANIMATION_H = 2        # Ratio between the height of the screen and the height of the animation
TEST_IMAGE_SPACING_HORI_FACTOR = 3    # Increase this value to increase the spacing between the 2 bottom test images
RATIO_SCREEN_H_VERT_SPACING_TEST = 20 # Decrease this value to increase the spacing between the top test image and the 2 bottom test images

# Training videos
VIDEO_FAM_DIR = os.path.join(DATA_PATH, 'videos', 'FAM')
VIDEO_NEW_DIR = os.path.join(DATA_PATH, 'videos', 'NEW')
VIDEO_FORMAT = '.avi'
TRAIN_WAIT_IMAGE_BKG = os.path.join(DATA_PATH, 'images', 'waitImage', 'trainWaitImageBackground.png')
TRAIN_WAIT_IMAGE = os.path.join(DATA_PATH, 'images', 'waitImage', 'trainWaitImage.png')

# Test images and audio
IMAGE_FAM_DIR = os.path.join(DATA_PATH, 'images', 'FAM')
IMAGE_NEW_DIR = os.path.join(DATA_PATH, 'images', 'NEW')
IMAGE_FAM_SCRAMBLED_DIR = os.path.join(DATA_PATH, 'images', 'FAM_scrambled')
IMAGE_NEW_SCRAMBLED_DIR = os.path.join(DATA_PATH, 'images', 'NEW_scrambled')
IMAGE_FORMAT = ".png"
TEST_WAIT_IM_PATH = os.path.join(DATA_PATH, 'images', 'waitImage', 'stim_attractif_3_grand.png')
AUDIO_FAM_DIR = os.path.join(DATA_PATH, 'audio', 'FAM')
AUDIO_FAM_SCRAMBLED_2Y_DIR = os.path.join(DATA_PATH, 'audio_short_ver_2y', 'FAM')
AUDIO_FAM_SCRAMBLED_4Y_DIR = os.path.join(DATA_PATH, 'audio_short_ver_4y', 'FAM')
AUDIO_NEW_DIR = os.path.join(DATA_PATH, 'audio', 'NEW')
AUDIO_NEW_SCRAMBLED_2Y_DIR = os.path.join(DATA_PATH, 'audio_short_ver_2y', 'NEW')
AUDIO_NEW_SCRAMBLED_4Y_DIR = os.path.join(DATA_PATH, 'audio_short_ver_4y', 'NEW')
AUDIO_FORMAT = ".wav"
ANIMATION_DIR = os.path.join(DATA_PATH, 'animation')
N_ANIMATION = 13  # Number of animations

# Simon's version - FEEDBACK
AUDIO_FEEDBACK_DIR = os.path.join(DATA_PATH, 'feedback_audio')
N_POSITIF_AUDIO_FEEDBACKS = len(os.listdir(os.path.join(AUDIO_FEEDBACK_DIR, 'positif')))
N_NEGATIF_AUDIO_FEEDBACKS = len(os.listdir(os.path.join(AUDIO_FEEDBACK_DIR, 'negatif')))
IM_POSITIF_FEEDBACK = os.path.join(DATA_PATH, 'feedback_image', 'positif.jpg')
IM_NEGATIF_FEEDBACK = os.path.join(DATA_PATH, 'feedback_image', 'negatif.jpg')
IMAGE_FEEDBACK_PROP_H = 0.4  # Increase for a bigger feedback image
FEEDBACK_TIME_MS = 3000
CORRECT_IM_SHOW_MS = 2000
CORRECT_IM_SHOW_AUDIOPATH = os.path.join(DATA_PATH, 'feedback_audio', 'cetaitlui.wav')
CORRECT_IM_HEIGHT = 300

# Files 
RESULTS_DIR = os.path.join(ROOT_DIR_PATH, 'results_v3')
TIME_LOG_FILE_NAME = 'time_events.txt'
RESULTS_FILE_NAME = 'test_results.txt'

# Training 
FAM_OBJECT_LIST = ["cuillere", "marteau", "tasse", "voiture", "toupie", "livre"]
NEW_OBJECT_LIST = ["chenille", "dinosaure_bleu", "dinosaure_orange", "dinosaure_vert", "hochet", "monstre_vert", "ours", "toupie"]
NEW_WORD_LIST = ["guessa", "kilu", "lupa", "nive", "nubi", "peno", "pite", "ralo", "rivou", "tuda", "vassi"]
TRAIN_INSTRUCTIONS = ["regarde", "tiens", "vu"]
TRAIN_TIMER_DURATION = 700  # Duration after which the attractor appears on the waiting image (in ms)

# Testing
TEST_INSTRUCTIONS_TACTILE = ["est_ou", "montre", "touche"]
TEST_INSTRUCTIONS_POINTAGE = ["ou_est", "regarde", "tu_vois"]
TRAIN_INSTRUCTIONS_SCRAMBLED = ["regarde", "tiens", "vu"]

# GRAPHICS 
BACKGROUND_COLOR = 240, 240, 240


def load_soft_rules(version):
    soft_rules = {}
    if version == 'explicit':
        soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM'] = 1  # If 1, during the FAM testing, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_NEW'] = 0  # If 1, during the FAM testing, continue only if the response is correct
        # TEST PARAMETERS
        soft_rules['N_TEST_FAM'] = 3              # Must be multiple of 3
        soft_rules['N_TEST_NEW'] = 9              # Must be multiple of 3
        soft_rules['SAME_POS_ROW_TEST_MAX'] = 1                   # Object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
        soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'] = 2               # Target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX_ROW times in a row
        soft_rules['SAME_TARGET_TEST_MAX_ROW'] = 2                   # Target cannot be the same more than SAME_TARGET_MAX times in a row
        # TRAINING PARAMETERS
        # Number of repetition for each video
        soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_3'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] = 3
        soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] = 5
        # Maximal number of repetitions in a row
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_1'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_2'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_3'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_1'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_2'] = 2
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_3'] = 2

    elif version == 'explicit-1rep':
        # TEST PARAMETERS
        soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM'] = 1  # If 1, during the FAM testing, continue only if the response is correct
        soft_rules['N_TEST_FAM'] = 3              # Must be multiple of 3
        soft_rules['N_TEST_NEW'] = 9              # Must be multiple of 3
        soft_rules['SAME_POS_ROW_TEST_MAX'] = 1                      # Object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
        soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'] = 2               # Target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX_ROW times in a row
        soft_rules['SAME_TARGET_TEST_MAX_ROW'] = 2                   # Target cannot be the same more than SAME_TARGET_MAX times in a row
        # TRAINING PARAMETERS
        # Number of repetition for each video
        soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_3'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] = 1
        # Maximal number of repetitions in a row
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_1'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_2'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_FAM_3'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_1'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_2'] = 1
        soft_rules['SERIE_MAX_VID_TRAIN_NEW_3'] = 1

    elif version == 'fast-mapping':
        # TEST PARAMETERS
        soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM'] = 0   # If 1, during the FAM testing, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_FAM'] = 1  # If 1, during the FAM training, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_NEW'] = 1  # If 1, during the NEW training, continue only if the response is correct
        soft_rules['N_TEST_FAM'] = 3              # Must be multiple of 3
        soft_rules['N_TEST_NEW'] = 9              # Must be multiple of 3
        soft_rules['SAME_POS_ROW_TEST_MAX'] = 1                      # Object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
        soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'] = 2               # Target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX_ROW times in a row
        soft_rules['SAME_TARGET_TEST_MAX_ROW'] = 2                   # Target cannot be the same more than SAME_TARGET_MAX times in a row
        # TRAINING PARAMETERS
        # Number of repetition for each video
        soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_3'] = 1
        # New objects
        soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] = 3
        soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] = 5
        soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_1'] = 2
        soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_3'] = 1
        soft_rules['N_TRAIN_NEW'] = soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] + soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] + \
                                    soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] + soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_1'] + \
                                    soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_2'] + soft_rules['N_REPET_OBJ_TRAIN_NEW_FAM_3']

    elif version in ['scrambled-2y', 'scrambled-4y']:
        # TEST PARAMETERS
        soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM'] = 1   # If 1, during the FAM testing, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_FAM'] = 1  # If 1, during the FAM training, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_NEW'] = 1  # If 1, during the NEW training, continue only if the response is correct
        soft_rules['N_TEST_FAM'] = 3              # Must be multiple of 3
        soft_rules['N_TEST_NEW'] = 9              # Must be multiple of 3
        soft_rules['SAME_POS_ROW_TEST_MAX'] = 1                      # Object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
        soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'] = 2               # Target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX_ROW times in a row
        soft_rules['SAME_TARGET_TEST_MAX_ROW'] = 2                   # Target cannot be the same more than SAME_TARGET_MAX times in a row
        # TRAINING PARAMETERS
        # Number of repetition for each video
        soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_3'] = 1
        # New objects
        soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] = 3
        soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] = 5

    elif version in ['simon', 'simon-easy']:
        # TEST PARAMETERS
        soft_rules['WAIT_GOOD_RESPONSE_TEST_FAM'] = 0   # If 1, during the FAM testing, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_FAM'] = 0  # If 1, during the FAM training, continue only if the response is correct
        soft_rules['WAIT_GOOD_RESPONSE_TRAIN_NEW'] = 0  # If 1, during the NEW training, continue only if the response is correct
        soft_rules['N_TEST_FAM'] = 6              # Must be multiple of 3
        soft_rules['N_TEST_NEW'] = 9              # Must be multiple of 3
        soft_rules['SAME_POS_ROW_TEST_MAX'] = 1                      # Object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
        soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'] = 2               # Target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX_ROW times in a row
        soft_rules['SAME_TARGET_TEST_MAX_ROW'] = 2                   # Target cannot be the same more than SAME_TARGET_MAX times in a row
        # TRAINING PARAMETERS
        # Number of repetition for each video
        soft_rules['N_REPET_OBJ_TRAIN_FAM_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_2'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_FAM_3'] = 1
        # New objects
        soft_rules['N_REPET_OBJ_TRAIN_NEW_1'] = 1
        soft_rules['N_REPET_OBJ_TRAIN_NEW_2'] = 3
        soft_rules['N_REPET_OBJ_TRAIN_NEW_3'] = 5
    else:
        raise ValueError('Wrong version argument {}'.format(version))

    return soft_rules
