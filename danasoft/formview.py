# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:18:05 2016

@author: deudon
"""


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from subject import Subject
from config import *


class FormView(QtGui.QWidget):
    """  Form View class
    Widget used for filling the subject's informations (name, date, age, sex)
    and the objects used for the experiment (familiar and new objects)
    When the formular is validated with the "Create Subject" button, the entries 
    are checked: 
        - (Age entry must be numeric)
        - Gender entry must be either 'f' or 'm' (case insensitive)
        - The 3 familiar objects must be different
        - The 3 new objects must exist and be different
    After validation, the subject is created along with the sequences for 
    training and testing. The subject informations is also exported to a text file
    in the result directory. Finally the form_over_sig is emitted and the gui 
    returns to the startup view.
        
        Attributes:
            sub_name_ledit       : name entry (QLineEdit)
            date_ledit          : date entry (QLineEdit)
            age_ledit           : age entry (QLineEdit) - must be numeric
            sex_ledit           : gender entry (QLineEdit) - 'f' or 'm'
            fam_obj1_cb       : familiar object 1 (QComboBox)
            fam_obj2_cb       : familiar object 2 (QComboBox)
            fam_obj3_cb       : familiar object 3 (QComboBox)
            new_object1_ledit    : new object 1 (QLineEdit)
            new_object2_ledit    : new object 2 (QLineEdit)
            new_object3_ledit    : new object 2 (QLineEdit)
            create_subject_btn    : "Create Subject" button (QPushButton) used for 
                                 validating the formular
            
        Signals: 
            form_over_sig       : emitted when the user click the "Create Subject" 
                                 button and there is no error in the formular. 
                                 Send the subject object to the main window.
            exit_form_sig       : emitted when the used click the "Home" button.
                                 Go back to the startup view.
    """
    # Signals
    form_over_sig = QtCore.pyqtSignal(object)
    exit_form_sig = QtCore.pyqtSignal()
    
    def __init__(self, fill_subject):
        self.version = []
        self.soft_rules = []

        QtGui.QWidget.__init__(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(20, 20, 20, 20)

        # Top Horizontal Layout (with Home Button)
        hori_layout = QHBoxLayout()
        hori_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        hori_layout.addStretch(1)
        exit_btn = QPushButton("Home")
        size_policy = QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        exit_btn.setSizePolicy(size_policy)
        hori_layout.addWidget(exit_btn)
        
        # Page title
        page_title = QLabel("Setup Training")
        page_title.setAlignment(QtCore.Qt.AlignCenter)
        
        # All the new pseudo-object/pseudo-word pairs
        new_asso_pairs = QtCore.QStringList()
        for i in range(0, len(NEW_OBJECT_LIST)):
            for j in range(0, len(NEW_WORD_LIST)):
                new_asso_pairs.append(QtCore.QString(NEW_OBJECT_LIST[i]+'_'+NEW_WORD_LIST[j]))
                
        # Completer for auto-completion            
        completer_new = QCompleter()
        completer_new_model = QStringListModel()
        completer_new_model.setStringList(QtCore.QStringList(new_asso_pairs))
        completer_new.setModel(completer_new_model)
        
        # Formulaire Layout
        form_layout = QFormLayout()
        self.sub_name_ledit = QLineEdit()
        form_layout.addRow("Subject Name", self.sub_name_ledit)
        self.date_ledit = QLineEdit()
        form_layout.addRow("Date", self.date_ledit)
        self.age_ledit = QLineEdit()
        form_layout.addRow("Age", self.age_ledit)
        self.sex_ledit = QLineEdit()
        form_layout.addRow("Sex", self.sex_ledit)
        self.fam_obj1_cb = QComboBox()
        self.fam_obj1_cb.addItems(FAM_OBJECT_LIST)
        form_layout.addRow("Familiar Object #1", self.fam_obj1_cb)
        self.fam_obj2_cb = QComboBox()
        self.fam_obj2_cb.addItems(FAM_OBJECT_LIST)
        form_layout.addRow("Familiar Object #2", self.fam_obj2_cb)
        self.fam_obj3_cb = QComboBox()
        self.fam_obj3_cb.addItems(FAM_OBJECT_LIST)
        form_layout.addRow("Familiar Object #3", self.fam_obj3_cb)
        self.new_object1_ledit = QLineEdit()
        self.new_object1_ledit.setCompleter(completer_new)
        form_layout.addRow("New Object #1", self.new_object1_ledit)
        self.new_object2_ledit = QLineEdit()
        self.new_object2_ledit.setCompleter(completer_new)
        form_layout.addRow("New Object #2", self.new_object2_ledit)
        self.new_object3_ledit = QLineEdit()
        self.new_object3_ledit.setCompleter(completer_new)
        form_layout.addRow("New Object #3", self.new_object3_ledit)
        
        # If full_subject is True, fill subject info
        if fill_subject:
            self.sub_name_ledit.setText("Bob")
            self.date_ledit.setText("15 Avr 2015")
            self.age_ledit.setText("15 mois")
            self.sex_ledit.setText("M")
            self.fam_obj2_cb.setCurrentIndex(1)
            self.fam_obj3_cb.setCurrentIndex(2)
            self.new_object1_ledit.setText("dinosaure_orange_lupa")
            self.new_object2_ledit.setText("ours_kilu")
            self.new_object3_ledit.setText("monstre_vert_pite")

        # Create subject button
        start_layout = QHBoxLayout()
        spacer_item_left = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_item_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.create_subject_btn = QtGui.QPushButton("Create Subject")
        self.create_subject_btn.setSizePolicy(QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        start_layout.addItem(spacer_item_left)
        start_layout.addWidget(self.create_subject_btn)
        start_layout.addItem(spacer_item_right)
        
        # Main Layout
        layout.addLayout(hori_layout)
        layout.addWidget(page_title)
        layout.addLayout(form_layout)
        layout.addLayout(start_layout)

        self.create_subject_btn.clicked.connect(self.finish_form)
        exit_btn.clicked.connect(lambda: self.exit_form_sig.emit())

        # Check Formular when text changed
        self.sub_name_ledit.textChanged.connect(self.checkformcompleteness)
        self.date_ledit.textChanged.connect(self.checkformcompleteness)
        self.age_ledit.textChanged.connect(self.checkformcompleteness)
        self.sex_ledit.textChanged.connect(self.checkformcompleteness)
        self.new_object1_ledit.textChanged.connect(self.checkformcompleteness)
        self.new_object2_ledit.textChanged.connect(self.checkformcompleteness)
        self.new_object3_ledit.textChanged.connect(self.checkformcompleteness)

    def set_version(self, version):
        self.version = version

    def set_soft_rules(self, soft_rules):
        self.soft_rules = soft_rules

    def checkformcompleteness(self):
        form_ok = not(self.sub_name_ledit.text().isEmpty())
        form_ok = form_ok & (not(self.date_ledit.text().isEmpty()))
        form_ok = form_ok & (not(self.age_ledit.text().isEmpty()))
        form_ok = form_ok & (not(self.sex_ledit.text().isEmpty()))
        form_ok = form_ok & (not(self.new_object1_ledit.text().isEmpty()))
        form_ok = form_ok & (not(self.new_object2_ledit.text().isEmpty()))
        form_ok = form_ok & (not(self.new_object3_ledit.text().isEmpty()))
        if form_ok:
            self.create_subject_btn.setEnabled(1)
        else:
            self.create_subject_btn.setEnabled(0)
   
    def checksubjectinfo(self):
        err = False
        age_str, sex_str = unicode(self.age_ledit.text().toUtf8(), 'utf-8'), unicode(self.sex_ledit.text().toUtf8(), 'utf-8').upper()
        if sex_str in ["M", "F"]:
            self.sex_ledit.setStyleSheet("QLineEdit {color:black}")
        else:
            self.sex_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True           
        # Fam Objects 
        obj_fam1_str = unicode(self.fam_obj1_cb.currentText().toUtf8(), 'utf-8')
        obj_fam2_str = unicode(self.fam_obj2_cb.currentText().toUtf8(), 'utf-8')
        obj_fam3_str = unicode(self.fam_obj3_cb.currentText().toUtf8(), 'utf-8')
        # Chech the 3 fam objects are different
        if obj_fam1_str == obj_fam2_str:
            self.fam_obj2_cb.setStyleSheet("QComboBox {color:red}")
            err = True
        else:
            self.fam_obj2_cb.setStyleSheet("QComboBox {color:black}")
        if obj_fam1_str == obj_fam3_str or obj_fam2_str==obj_fam3_str:
            self.fam_obj3_cb.setStyleSheet("QComboBox {color:red}")
            err = True   
        else:
            self.fam_obj3_cb.setStyleSheet("QComboBox {color:black}")

        # New Objects
        obj_new1_str = unicode(self.new_object1_ledit.text().toUtf8(), 'utf-8')
        obj_new2_str = unicode(self.new_object2_ledit.text().toUtf8(), 'utf-8')
        obj_new3_str = unicode(self.new_object3_ledit.text().toUtf8(), 'utf-8')
        
        # All the new pseudo-object/pseudo-word pairs
        new_asso_pairs = [None]*(len(NEW_OBJECT_LIST)*len(NEW_WORD_LIST))
        i_asso = 0
        for i in range(0, len(NEW_OBJECT_LIST)):
            for j in range(0, len(NEW_WORD_LIST)):
                new_asso_pairs[i_asso] = NEW_OBJECT_LIST[i]+'_'+NEW_WORD_LIST[j]
                i_asso += 1
        # Check that the new objects are corrects associations
        if obj_new1_str not in new_asso_pairs:
            self.new_object1_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True
        else:
            self.new_object1_ledit.setStyleSheet("QLineEdit {color:black}")
        if obj_new2_str not in new_asso_pairs:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True
        else:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:black}")
        if obj_new3_str not in new_asso_pairs:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True
        else:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:black}")
            
        # Chech the 3 new objects are different
        if obj_new1_str == obj_new2_str:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True
        else:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:black}")
        if obj_new1_str == obj_new3_str or obj_new2_str == obj_new3_str:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True   
        else:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:black}")
            
        # Check that each new pseudo-object is different
        obj_new1_str_split = obj_new1_str.split(u'_')
        obj_new2_str_split = obj_new2_str.split(u'_')
        obj_new3_str_split = obj_new3_str.split(u'_')
        pseudo_obj_1 = u'_'.join(obj_new1_str_split[0:-1])
        pseudo_obj_2 = u'_'.join(obj_new2_str_split[0:-1])
        pseudo_obj_3 = u'_'.join(obj_new3_str_split[0:-1])
        pseudo_word_1 = obj_new1_str_split[-1]
        pseudo_word_2 = obj_new2_str_split[-1]
        pseudo_word_3 = obj_new3_str_split[-1]
        if pseudo_obj_1 == pseudo_obj_2 or pseudo_word_1 == pseudo_word_2:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True
        else:
            self.new_object2_ledit.setStyleSheet("QLineEdit {color:black}")
        if pseudo_obj_1 == pseudo_obj_3 or pseudo_obj_2 == pseudo_obj_3 or pseudo_word_1 == pseudo_word_3 or pseudo_word_2 == pseudo_word_3:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:red}")
            err = True   
        else:
            self.new_object3_ledit.setStyleSheet("QLineEdit {color:black}")

        name, date = self.sub_name_ledit.text().toUtf8(), self.date_ledit.text().toUtf8()
        name, date = unicode(name, 'utf-8'), unicode(date, 'utf-8')
        subject = Subject(name, age_str, sex_str, date, 3, [obj_fam1_str, obj_fam2_str, obj_fam3_str],
                          [obj_new1_str, obj_new2_str, obj_new3_str], self.version, self.soft_rules)
        return err, subject

    def finish_form(self):
        # Check validity of subject informations        
        err, subject = self.checksubjectinfo()
        print(subject.__unicode__())
        if not err:
            # Save subject informations            
            subject.exporttotxt(os.path.join(subject.result_dir, subject.name + u'.txt'))
            # Start training
            self.form_over_sig.emit(subject)
