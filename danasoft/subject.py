# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:45:40 2016

@author: deudon
"""
import os
import random
import numpy as np
from PyQt4 import QtCore
from config import *


class Subject:
    """ Subject class - 3 objects version
    The subject class contains all the informations about the subject : 
    subject's informations, familiar and new object selected, order of the training
    and testing sequences. 
    
    The sequence for training is created randomly with the following rules :
        - familiar object 1 is presented N_REPET_OBJ_TRAIN_FAM_1
        - familiar object 2 is presented N_REPET_OBJ_TRAIN_FAM_2
        - familiar object 2 is presented N_REPET_OBJ_TRAIN_FAM_3
        - familiar object 1 must not appear more than SERIE_MAX_VID_TRAIN_FAM_1 times in a row
        - familiar object 2 must not appear more than SERIE_MAX_VID_TRAIN_FAM_2 times in a row
        - familiar object 3 must not appear more than SERIE_MAX_VID_TRAIN_FAM_3 times in a row
        (same for new videos)
        
    The sequence for testing is created randomly with the following rules : 
        - familiar objects are tested in total of the three objects N_TEST_FAM times
        - new objects are tested in total of the three objects N_TEST_NEW times
        - the same object cannot appear at the same position more than SAME_POS_TEST_MAX times in a row
        - target cannot be the same more than SAME_TARGET_TEST_MAX times in a row
        - target cannot appear at the position more than SAME_TARGET_POS_TEST_MAX times in a row
        - if number of test is even, check that the two halves of the sequence are different  
  

    """
    def __init__(self, name, age, sex, date, n_objects, obj_fam_list, asso_new_list, version, soft_rules):
        self.name = name
        self.age = age
        self.sex = sex
        self.date = date
        self.version = version
        self.soft_rules = soft_rules
        if n_objects not in [2, 3]:
            raise ValueError('Wrong argument n_objects : {} - Must be either 2 or 3'.format(n_objects))
        self.n_objects = n_objects
        self.result_dir = self.createresultdir()
        self.obj_fam = dict(zip(range(-1, -n_objects-1, -1), obj_fam_list))
        self.asso_new = dict(zip(range(1, n_objects+1, 1), asso_new_list))
        self.pseudo_obj_new = dict(zip(range(1, n_objects+1, 1),
                                       ['_'.join(asso_new_i.split('_')[:-1]) for asso_new_i in self.asso_new.values()]))
        self.pseudo_word_new = dict(zip(range(1, n_objects+1, 1),
                                        [asso_new_i.split('_')[-1] for asso_new_i in self.asso_new.values()]))
        self.test_objinpos_fam, self.test_posofobj_fam, self.test_objtarget_fam, self.test_posoftarget_fam = [], [], [], []
        self.test_objinpos_new, self.test_posofobj_new, self.test_objtarget_new, self.test_posoftarget_new = [], [], [], []
        # For the fast-mapping version and simon's versions :
        self.train_objinpos_fam, self.train_posofobj_fam, self.train_objtarget_fam, self.train_posoftarget_fam = [], [], [], []
        self.train_objinpos_new, self.train_posofobj_new, self.train_objtarget_new, self.train_posoftarget_new = [], [], [], []
        # For explicit version :
        self.train_vidorder_fam, self.train_vidorder_new = [], []

    def __str__(self):
        desc_str = '{} - Age : {} - Sex {} ans - {}\n'.format(self.name, self.age, self.sex, self.date)
        desc_str += 'Familiar objects : {}\n'.format(self.obj_fam)
        desc_str += 'New associations : {}'.format(self.asso_new)
        return desc_str

    def create_test_sequence(self, novelty):
        if novelty == 'fam':
            n_target_per_obj = int(self.soft_rules['N_TEST_FAM'] / 3)
            self.test_objinpos_fam, self.test_posofobj_fam, self.test_objtarget_fam, self.test_posoftarget_fam = \
                createrandomsequence_test(n_target_per_obj, n_target_per_obj, n_target_per_obj, 'fam',
                                          self.soft_rules['SAME_POS_ROW_TEST_MAX'], self.soft_rules['SAME_TARGET_TEST_MAX_ROW'],
                                          self.soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'])
        elif novelty == 'new':
            n_target_per_obj = int(self.soft_rules['N_TEST_NEW'] / 3)
            self.test_objinpos_new, self.test_posofobj_new, self.test_objtarget_new, self.test_posoftarget_new = \
                createrandomsequence_test(n_target_per_obj, n_target_per_obj, n_target_per_obj, 'new',
                                          self.soft_rules['SAME_POS_ROW_TEST_MAX'], self.soft_rules['SAME_TARGET_TEST_MAX_ROW'],
                                          self.soft_rules['SAME_TARGET_POS_TEST_MAX_ROW'])

    def create_train_sequence(self, novelty):
        # Assign this order
        if self.version in ['explicit', 'explicit-1rep']:
            if novelty == 'fam':
                self.train_vidorder_fam = createrandomsequence_train('fam', self.soft_rules)
            elif novelty == 'new':
                self.train_vidorder_new = createrandomsequence_train('new', self.soft_rules)
        elif self.version == 'fast-mapping':
            if novelty == 'fam':
                self.train_objinpos_fam, self.train_posofobj_fam, self.train_objtarget_fam, self.train_posoftarget_fam = \
                    createrandomsequence_test(self.soft_rules['N_REPET_OBJ_TRAIN_FAM_1'], self.soft_rules['N_REPET_OBJ_TRAIN_FAM_2'],
                                              self.soft_rules['N_REPET_OBJ_TRAIN_FAM_3'], novelty, self.soft_rules['SAME_POS_ROW_TEST_MAX'],
                                              self.soft_rules['SAME_TARGET_TEST_MAX_ROW'], self.soft_rules['SAME_TARGET_TEST_MAX_ROW'])
            elif novelty == 'new':
                self.train_objinpos_new, self.train_posofobj_new, self.train_objtarget_new, self.train_posoftarget_new = \
                    createrandomsequence_train_fastmapping_new(self.soft_rules)
        elif self.version in ['scrambled-2y', 'scrambled-4y', 'simon', 'simon-easy']:
            if novelty == 'fam':
                self.train_objinpos_fam, self.train_posofobj_fam, self.train_objtarget_fam, self.train_posoftarget_fam = \
                    createrandomsequence_test(self.soft_rules['N_REPET_OBJ_TRAIN_FAM_1'], self.soft_rules['N_REPET_OBJ_TRAIN_FAM_2'],
                                              self.soft_rules['N_REPET_OBJ_TRAIN_FAM_3'], novelty, self.soft_rules['SAME_POS_ROW_TEST_MAX'],
                                              self.soft_rules['SAME_TARGET_TEST_MAX_ROW'], self.soft_rules['SAME_TARGET_TEST_MAX_ROW'])
            elif novelty == 'new':
                self.train_objinpos_new, self.train_posofobj_new, self.train_objtarget_new, self.train_posoftarget_new = \
                    createrandomsequence_train_fastmapping_new(self.soft_rules)

    def getobjectinpos(self, pos, i_trial, condition):
        if condition.lower() == 'test_fam':
            obj_num = self.test_objinpos_fam[i_trial, pos]
        elif condition.lower() == 'test_new':
            obj_num = self.test_objinpos_new[i_trial, pos]
        elif condition.lower() in ['fast-mapping_train_fam', 'scrambled-2y_train_fam', 'scrambled-4y_train_fam', 'simon_train_fam', 'simon-easy_train_fam']:
            obj_num = self.train_objinpos_fam[i_trial, pos]
        elif condition.lower() in ['fast-mapping_train_new', 'scrambled-2y_train_new', 'scrambled-4y_train_new', 'simon_train_new', 'simon-easy_train_new']:
            obj_num = self.train_objinpos_new[i_trial, pos]
        else:
            raise ValueError('Wrong condition : {} - Possibles values are [\'fam\' or \'new\']')
        asso_name, obj_name, pseudo_word = self.getobjectname(obj_num)
        return obj_num, asso_name, obj_name, pseudo_word

    def getobjectname(self, obj_num):
        if obj_num < 0:     # Fam object
            return self.obj_fam[obj_num], self.obj_fam[obj_num], []
        else:               # New object
            return self.asso_new[obj_num], self.pseudo_obj_new[obj_num], self.pseudo_word_new[obj_num]

    def gettargetpos(self, i_trial, condition):
        condition = condition.lower()
        if condition == 'test_fam':
            target_pos = self.test_posoftarget_fam[i_trial]
        elif condition == 'test_new':
            target_pos = self.test_posoftarget_new[i_trial]
        elif condition in ['fast-mapping_train_fam', 'scrambled-2y_train_fam', 'scrambled-4y_train_fam', 'simon_train_fam', 'simon-easy_train_fam']:
            target_pos = self.train_posoftarget_fam[i_trial]
        elif condition in ['fast-mapping_train_new', 'scrambled-2y_train_new', 'scrambled-4y_train_new', 'simon_train_new', 'simon-easy_train_new']:
            target_pos = self.train_posoftarget_new[i_trial]
        else:
            raise ValueError('Wrong condition : {} - Possibles values are [\'fam\' or \'new\']')
        return target_pos

    def gettargetname(self, i_trial, condition):
        condition = condition.lower()
        if condition == 'test_fam':
            target_num = self.test_objtarget_fam[i_trial]
        elif condition == 'test_new':
            target_num = self.test_objtarget_new[i_trial]
        elif condition in ['fast-mapping_train_fam', 'scrambled-2y_train_fam', 'scrambled-4y_train_fam', 'simon_train_fam', 'simon-easy_train_fam']:
            target_num = self.train_objtarget_fam[i_trial]
        elif condition in ['fast-mapping_train_new', 'scrambled-2y_train_new', 'scrambled-4y_train_new', 'simon_train_new', 'simon-easy_train_new']:
            target_num = self.train_objtarget_new[i_trial]
        else:
            raise ValueError('Wrong condition : {} - Possibles values are [\'fam\' or \'new\']')
        target_name = self.getobjectname(target_num)[0]
        return target_num, target_name

    def write_train_sequence(self, novelty):
        filepath = os.path.join(self.result_dir, str(self.name)+'.txt')
        with open(filepath, 'a') as f:
            if novelty == 'fam':
                f.write('\n\n------- Training Parameters Fam-------')
                if self.version in ['explicit', 'explicit-1rep']:
                    f.write('\nTraining video order FAM,')
                    np.savetxt(f, self.train_vidorder_fam, '%d', ' ', ';')
                else:
                    f.write('\nObject at each position FAM,')
                    np.savetxt(f, self.train_objinpos_fam, '%d', ' ', ';')
                    f.write('\nPosition of the 3 objects FAM,')
                    np.savetxt(f, self.train_posofobj_fam, '%d', ' ', ';')
                    f.write('\nTarget object FAM,')
                    np.savetxt(f, self.train_objtarget_fam, '%d', ' ', ';')
                    f.write('\nPosition of target object FAM,')
                    np.savetxt(f, self.train_posoftarget_fam, '%d', ' ', ';')
            elif novelty == 'new':
                f.write('\n\n------- Training Parameters New-------')
                if self.version in ['explicit', 'explicit-1rep']:
                    f.write('\nTraining video order FAM,')
                    np.savetxt(f, self.train_vidorder_new, '%d', ' ', ';')
                else:
                    f.write('\nObject at each position NEW,')
                    np.savetxt(f, self.train_objinpos_new, '%d', ' ', ';')
                    f.write('\nPosition of the 3 objects NEW,')
                    np.savetxt(f, self.train_posofobj_new, '%d', ' ', ';')
                    f.write('\nTarget object NEW,')
                    np.savetxt(f, self.train_objtarget_new, '%d', ' ', ';')
                    f.write('\nPosition of target object NEW,')
                    np.savetxt(f, self.train_posoftarget_new, '%d', ' ', ';')
            else:
                raise ValueError('Wrong argument novelty : {}'.format(novelty))

    def write_test_sequence(self, novelty):
        filepath = os.path.join(self.result_dir, str(self.name)+'.txt')
        with open(filepath, 'a') as f:
            if novelty == 'fam':
                f.write('\n\n------- Test Parameters Fam-------')
                f.write('\nObject at each position FAM,')
                np.savetxt(f, self.test_objinpos_fam, '%d', ' ', ';')
                f.write('\nPosition of the 3 objects FAM,')
                np.savetxt(f, self.test_posofobj_fam, '%d', ' ', ';')
                f.write('\nTarget object FAM,')
                np.savetxt(f, self.test_objtarget_fam, '%d', ' ', ';')
                f.write('\nPosition of target object FAM,')
                np.savetxt(f, self.test_posoftarget_fam, '%d', ' ', ';')
            elif novelty == 'new':
                f.write('\n\n------- Test Parameters New-------')
                f.write('\nObject at each position NEW,')
                np.savetxt(f, self.test_objinpos_new, '%d', ' ', ';')
                f.write('\nPosition of the 3 objects NEW,')
                np.savetxt(f, self.test_posofobj_new, '%d', ' ', ';')
                f.write('\nTarget object NEW,')
                np.savetxt(f, self.test_objtarget_new, '%d', ' ', ';')
                f.write('\nPosition of target object NEW,')
                np.savetxt(f, self.test_posoftarget_new, '%d', ' ', ';')
            else:
                raise ValueError('Wrong argument novelty : {}'.format(novelty))

    def exporttotxt(self, filepath):
        with open(filepath, 'w') as f:
            f.write('Name,{}\nAge,{}\nSex,{}\nDate,{}\n'.format(self.name, self.age, self.sex, self.date))
            for i in range(self.n_objects):
                f.write('Familiar Object #{},{}\n'.format(i+1, self.obj_fam.values()[i]))
            for i in range(self.n_objects):
                f.write('New Object #{},{}\n'.format(i + 1, self.asso_new.values()[i]))

    def createresultdir(self):
        # Create a folder in the results directory based on the name of the subject and the current date
        date = QtCore.QDate.currentDate()
        date_str = date.toString('dd_MM_yy')
        if not os.path.isdir(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)
        dir_path = os.path.join(RESULTS_DIR, str(self.name)+'_'+str(date_str))
        inc = 2
        while os.path.isdir(dir_path):
            dir_path = dir_path + '_' + str(inc) if inc == 2 else dir_path[0:-len(str(inc-1))]+str(inc)
            inc += 1
        os.mkdir(dir_path)
        return dir_path


def createrandomsequence_train(novelty, sr):
    """ Create the sequence of the training videos. The number of repetitions of the same video in a row is
     controlled by the parameter N_REPET_OBJ_TRAIN_FAM_1[2,3] and N_REPET_OBJ_TRAIN_NEW_1[2,3]
    """
    novelty = novelty.lower()
    if novelty == 'fam':
        n_presentations = sr['N_REPET_OBJ_TRAIN_FAM_1'] + sr['N_REPET_OBJ_TRAIN_FAM_2'] + sr['N_REPET_OBJ_TRAIN_FAM_3']
        train_vid_order = np.hstack([1 * np.ones(sr['N_REPET_OBJ_TRAIN_FAM_1']), 2 * np.ones(sr['N_REPET_OBJ_TRAIN_FAM_2']),
                                     3 * np.ones(sr['N_REPET_OBJ_TRAIN_FAM_3'])]).astype(int)
    elif novelty == 'new':
        n_presentations = sr['N_REPET_OBJ_TRAIN_NEW_1'] + sr['N_REPET_OBJ_TRAIN_NEW_2'] + sr['N_REPET_OBJ_TRAIN_NEW_3']
        train_vid_order = np.hstack([1 * np.ones(sr['N_REPET_OBJ_TRAIN_NEW_1']), 2 * np.ones(sr['N_REPET_OBJ_TRAIN_NEW_2']),
                                     3 * np.ones(sr['N_REPET_OBJ_TRAIN_NEW_3'])]).astype(int)
    else:
        raise ValueError('Wrong condition : {}'.format(condition))

    criteria_met = False
    while not criteria_met:
        random.shuffle(train_vid_order)
        # First video can't be in first or last position
        if train_vid_order[0] == 1 or train_vid_order[-1] == 1:
            continue
        # Check number of repetition of the same video in a row
        vid_1_serie, vid_2_serie, vid_3_serie = 0, 0, 0
        for i in range(0, n_presentations):
            if train_vid_order[i] == 1:
                vid_1_serie += 1
                vid_2_serie, vid_3_serie = 0, 0
            elif train_vid_order[i] == 2:
                vid_2_serie += 1
                vid_1_serie, vid_3_serie = 0, 0
            elif train_vid_order[i] == 3:
                vid_3_serie += 1
                vid_1_serie, vid_2_serie = 0, 0

            if novelty == 'fam':
                if vid_1_serie > sr['SERIE_MAX_VID_TRAIN_FAM_1'] or vid_2_serie > sr['SERIE_MAX_VID_TRAIN_FAM_2'] or vid_3_serie > sr['SERIE_MAX_VID_TRAIN_FAM_3']:
                    criteria_met = False
                    break
                else:
                    criteria_met = True
            elif novelty == 'new':
                if vid_1_serie > sr['SERIE_MAX_VID_TRAIN_NEW_1'] or vid_2_serie > sr['SERIE_MAX_VID_TRAIN_NEW_2'] or vid_3_serie > sr['SERIE_MAX_VID_TRAIN_NEW_3']:
                    criteria_met = False
                    break
                else:
                    criteria_met = True

                    # If condition are met, exit the loop
        if criteria_met:
            break

    if novelty == 'fam':
        train_vid_order = -train_vid_order

    return train_vid_order.astype(int)


def createrandomsequence_train_fastmapping_new(sr):
    """ Use this function for creating the pseudo random sequence for the training on
    new objects using the fast-mapping approach
    """
    # Check number of trials is a multiple of 3

    n_trials = sr['N_REPET_OBJ_TRAIN_NEW_1'] + sr['N_REPET_OBJ_TRAIN_NEW_2'] + sr['N_REPET_OBJ_TRAIN_NEW_3']
    if not n_trials / 3 == n_trials / 3.0:
        raise ValueError("ERROR in subject:createrandomsequence_train_fastmapping_new n_trials should be a multiple of 3")

    # Target criteria : new object are identified by positive number, fam objects by negative ones
    obj_target = np.hstack((1*np.ones(sr['N_REPET_OBJ_TRAIN_NEW_1']), 2*np.ones(sr['N_REPET_OBJ_TRAIN_NEW_2']),
                            3*np.ones(sr['N_REPET_OBJ_TRAIN_NEW_3']))).astype(int)
    target_condition_met = False
    same_target = 1
    while not target_condition_met:
        np.random.shuffle(obj_target)
        # First criteria : The first object (beeing repeted less than the others) must appears after the 2 others (and not in last position)
        # if obj_target[0] != 1 and obj_target[-1] != 1:
        if obj_target[-1] != 1 and np.unique(obj_target[:int(np.where(obj_target == 1)[0]+1)]).size == 3:
            # Second criteria : Target cannot be the same in a row more than SAME_TARGET_TRAIN_MAX
            for i in range(1, n_trials):
                if obj_target[i] == obj_target[i - 1]:
                    same_target += 1
                else:
                    same_target = 1
                if same_target > sr['SAME_TARGET_TEST_MAX_ROW']:
                    target_condition_met = False
                    break
                else:
                    target_condition_met = True
    # Position of the target
    target_pos_condition_met = False
    # Criteria: the target position cannot be the same more than SAME_TARGET_POS_TRAIN_MAX times in a row
    while not target_pos_condition_met:
        target_pos = np.ones(n_trials)
        same_target_pos = 1
        for i in range(0, n_trials):
            target_pos[i] = np.random.randint(1, 4)
        for i in range(1, n_trials):
            if target_pos[i] == target_pos[i - 1]:
                same_target_pos += 1
            else:
                same_target_pos = 1
            if same_target_pos > sr['SAME_TARGET_POS_TEST_MAX_ROW']:
                target_pos_condition_met = False
                break
            else:
                target_pos_condition_met = True
        target_pos_count = np.array([np.sum(target_pos == i) for i in [1, 2, 3]])
        # Criteria : the target must appear the same number of times at each position
        if target_pos_count.max() > (n_trials / 3):
            target_pos_condition_met = False
    # Now that we have the target and its position for each trial, choose randomly familiar objects as distractor
    obj_in_pos = np.zeros((n_trials, 3))
    pos_of_obj = np.zeros((n_trials, 3))
    target_pos = target_pos.astype(int)
    rand_fam_vect = -np.array([1, 2, 3])
    for i in range(0, n_trials):
        np.random.shuffle(rand_fam_vect)
        for j in range(0, 3):
            if (target_pos[i] - 1) == j:
                # Set the target at the right position
                obj_in_pos[i, j] = obj_target[i]
            else:
                obj_in_pos[i, j] = rand_fam_vect[j]

    # Return
    return obj_in_pos.astype(int), pos_of_obj.astype(int), obj_target.astype(int), target_pos.astype(int)


# def createrandomsequence_test(condition, sr):
#     """ The conditions to be respected by the sequence are :
#             - object cannot appear in the same position more than SAME_POS_TEST_MAX
#             - target cannot be the same more than SAME_TARGET_TEST_MAX times in a row
#             - target cannot appear at the same position more than SAME_TARGET_POS_TEST_MAX times
#             - if the number of test is even, check that the two halves of the sequence are different
#
#     """
#     condition = condition.lower()
#     if condition == 'fam':
#         n_test_condition = sr['N_TEST_FAM']
#         same_target_pos_test_max = sr['SAME_TARGET_POS_TEST_MAX_FAM']
#     elif condition == 'new':
#         n_test_condition = sr['N_TEST_NEW']
#         same_target_pos_test_max = sr['SAME_TARGET_POS_TEST_MAX_NEW']
#     elif condition in ['fast-mapping_train_fam', 'simon_train_fam', 'simon-easy_train_fam']:
#         n_test_condition = sr['N_TRAIN_FAM']
#         same_target_pos_test_max = sr['SAME_TARGET_POS_TEST_MAX_FAM']
#     elif condition in ['simon_train_new', 'simon-easy_train_new']:
#         n_test_condition = sr['N_TEST_NEW']
#         same_target_pos_test_max = sr['SAME_TARGET_POS_TEST_MAX_NEW']
#
#     if not n_test_condition/3 == n_test_condition/3.0:
#         print ("ERROR in subject:createrandomsequence N_TEST_FAM and N_TEST_NEW must be multiples of 3")
#         return
#
#     # Use a timer to see if the algo is stuck
#     time_watch = QtCore.QTime()
#     algo_stuck = True
#     while algo_stuck:
#         algo_stuck = False
#         pos_possibilities = np.array([[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
#         same_pos_condition = False
#         obj_in_pos = np.zeros((n_test_condition, 3), dtype=int)
#         while not same_pos_condition:
#             # Shuffle
#             for i in range(0, n_test_condition):
#                 obj_in_pos[i] = pos_possibilities[np.random.randint(6)]
#
#             # Check condition for position: object cannot appear in the same position more than SAME_POS_TEST_MAX times in a row
#             same_pos = np.ones(3, dtype=int)
#             for i in range(0, n_test_condition):
#                 for j in range(0, 3):
#                     same_pos[j] = same_pos[j] + 1 if obj_in_pos[i, j] == obj_in_pos[i-1, j] else 1
#                 if np.max(same_pos) > sr['SAME_POS_ROW_TEST_MAX']:
#                     same_pos_condition = False
#                     break
#                 else:
#                     same_pos_condition = True
#
#         time_watch.start()
#         # Associate a target for each trial
#         obj_target = np.repeat(np.array([1, 2, 3]), n_test_condition/3)
#         pos_of_target = np.zeros(n_test_condition, dtype=int)
#         target_conditions = False
#         while not target_conditions:
#             np.random.shuffle(obj_target)
#             # Get position of the target given the position of each object
#             pos_of_target = np.array([int(np.where(obj_in_pos[i] == obj_target[i])[0]) for i in range(n_test_condition)]) + 1
#             # Check : Target's position cannot be the same more than SAME_TARGET_POS_TEST_MAX
#             pos_of_target_count = np.array([np.sum(pos_of_target == i) for i in [1, 2, 3]])
#             if pos_of_target_count.max() > same_target_pos_test_max:
#                 target_conditions = False
#             else:
#                 # Check : Target cannot be the same more than SAME_TARGET_TEST_MAX_ROW time in a row
#                 # Check : Target cannot appear at the position more than SAME_TARGET_POS_TEST_MAX_ROW
#                 same_target_row, same_target_row_pos = 1, 1
#                 for i in range(1, n_test_condition):
#                     same_target_row = same_target_row+1 if obj_target[i-1] == obj_target[i] else 1
#                     same_target_row_pos = same_target_row_pos+1 if pos_of_target[i-1] == pos_of_target[i] else 1
#                     if same_target_row > sr['SAME_TARGET_TEST_MAX_ROW'] or same_target_row_pos > sr['SAME_TARGET_POS_TEST_MAX_ROW']:
#                         target_conditions = False
#                         break
#                     target_conditions = True
#
#             # Condition 3: if number of test is even, check that the two halves of the sequence are different
#             if n_test_condition/2 == n_test_condition/2.0:
#                 if sum(obj_target[0:n_test_condition/2] == obj_target[n_test_condition/2:n_test_condition]) == n_test_condition/2:
#                     target_conditions = False
#
#             if time_watch.elapsed() > 5:
#                 algo_stuck = True
#                 print 'Im stuck !!!'
#                 break
#
#     if not target_conditions or not same_pos_condition:
#         raise ValueError('Error in generating Test sequence')
#     pos_of_obj = obj_in_pos
#
#     if 'fam' in condition:
#         obj_in_pos = -obj_in_pos
#         obj_target = -obj_target
#
#     return obj_in_pos.astype(int), pos_of_obj.astype(int), obj_target.astype(int), pos_of_target.astype(int)


def createrandomsequence_test(n_target_obj1, n_target_obj2, n_target_obj3, novelty, same_object_pos_max_row,
                                same_target_max_row, same_target_pos_max_row):
    """ Use this function for creating a test sequence (that can be used for training or testing), where 3 objects are
    presented.
    Conditions are :
        - The same object cannot appear at the same POSITION more than same_object_pos_max_row in a row
        - The target object must appear at each POSITION the same number of times (n_trials/3)
        - The target POSITION cannot be the same more than same_target_pos_max_row in a row
        - The target OBJECT cannot be the same more than same_target_max_row
        - The first object (beeing repeted less than the others) must appears after the 2 others and not in the last
        position. This is NOT verified for the test condition when each object is the target the same number of times
    """
    # Check number of trials is a multiple of 3
    n_trials = n_target_obj1 + n_target_obj2 + n_target_obj3
    if not n_trials / 3 == n_trials / 3.0:
        raise ValueError("ERROR in subject:createrandomsequence_test n_trials should be a multiple of 3")

    # Target criteria : new object are identified by positive number, fam objects by negative ones
    obj_target = np.hstack([1*np.ones(n_target_obj1), 2*np.ones(n_target_obj2), 3*np.ones(n_target_obj3)]).astype(int)

    time_watch = QtCore.QTime()
    algo_stuck = True

    while algo_stuck:
        algo_stuck = False
        target_condition_met = False
        same_target = 1

        while not target_condition_met:
            np.random.shuffle(obj_target)
            if np.unique([n_target_obj1, n_target_obj2, n_target_obj3]).size == 3:
                # Criteria : the first object (beeing repeted less than the others) must appears after the 2 others (and not in last position)
                if obj_target[-1] == 1 or np.unique(obj_target[:int(np.where(obj_target == 1)[0]+1)]).size < 3:
                    target_condition_met = False
                else:
                    target_condition_met = True
            else:
                target_condition_met = True
            # Second criteria : Target cannot be the same in a row more than same_target_max_row
            if target_condition_met:
                for i in range(1, n_trials):
                    if obj_target[i] == obj_target[i - 1]:
                        same_target += 1
                    else:
                        same_target = 1
                    if same_target > same_target_max_row:
                        target_condition_met = False
                        break
                    else:
                        target_condition_met = True

        # Position of the target
        target_pos_condition_met = False
        # Criteria: the target position cannot be the same more than same_target_pos_max_row times in a row and no more
        # than n_trials / 3 times
        while not target_pos_condition_met:
            target_pos = np.ones(n_trials)
            same_target_pos = 1
            for i in range(0, n_trials):
                target_pos[i] = np.random.randint(1, 4)
            for i in range(1, n_trials):
                if target_pos[i] == target_pos[i - 1]:
                    same_target_pos += 1
                else:
                    same_target_pos = 1
                if same_target_pos > same_target_pos_max_row:
                    target_pos_condition_met = False
                    break
                else:
                    target_pos_condition_met = True
            target_pos_count = np.array([np.sum(target_pos == i) for i in [1, 2, 3]])
            # Criteria : the target must appear the same number of times at each position
            if target_pos_count.max() > (n_trials / 3):
                target_pos_condition_met = False

        time_watch.start()
        same_pos_condition = False  # Object cannot appear at the same position more than same_object_pos_max_row
        while not same_pos_condition:
            # Now that we have the target and its position for each trial, choose randomly familiar objects as distractor
            obj_in_pos = np.zeros((n_trials, 3))
            target_pos = target_pos.astype(int)
            for i in range(0, n_trials):
                non_targets = np.delete(np.array([1, 2, 3]), obj_target[i]-1)
                np.random.shuffle(non_targets)
                k = 0
                for j in range(0, 3):
                    if (target_pos[i] - 1) == j:
                        # Set the target at the right position
                        obj_in_pos[i, j] = obj_target[i]
                    else:
                        obj_in_pos[i, j] = non_targets[k]
                        k += 1

            # Check condition for position: object cannot appear in the same position more same_object_pos_max_row in a row
            same_pos = np.ones(3, dtype=int)
            for i in range(0, n_trials):
                for j in range(0, 3):
                    same_pos[j] = same_pos[j] + 1 if obj_in_pos[i, j] == obj_in_pos[i - 1, j] else 1
                if np.max(same_pos) > same_object_pos_max_row:
                    same_pos_condition = False
                    break
                else:
                    same_pos_condition = True

            if time_watch.elapsed() > 5:
                algo_stuck = True
                print 'Im stuck !!!'
                break

    pos_of_obj = obj_in_pos

    # Return
    if novelty == 'fam':
        obj_in_pos = -obj_in_pos
        obj_target = -obj_target
    return obj_in_pos.astype(int), pos_of_obj.astype(int), obj_target.astype(int), target_pos.astype(int)


if __name__ == '__main__':
    s = Subject('oko', 2, 'f', 'today', 3, ['toupie', 'voiture', 'aaa'],
                ['dino_kilu', 'monstre_vert_pite', 'ours_guessa'], 'explicit', load_soft_rules('explicit'))
    s.create_train_sequence('fam')
    s.create_test_sequence('new')
    # print(s)

