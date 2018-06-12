# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogSetParam.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ParamDialog(object):
    def setupUi(self, ParamDialog):
        ParamDialog.setObjectName("ParamDialog")
        ParamDialog.setWindowModality(QtCore.Qt.WindowModal)
        ParamDialog.resize(436, 371)
        self.gridLayout = QtWidgets.QGridLayout(ParamDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.param_list = QtWidgets.QListView(ParamDialog)
        self.param_list.setEnabled(True)
        self.param_list.setMinimumSize(QtCore.QSize(400, 300))
        self.param_list.setObjectName("param_list")
        self.verticalLayout.addWidget(self.param_list)
        self.buttonBox = QtWidgets.QDialogButtonBox(ParamDialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(400, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ParamDialog)
        self.buttonBox.accepted.connect(ParamDialog.accept)
        self.buttonBox.rejected.connect(ParamDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParamDialog)

    def retranslateUi(self, ParamDialog):
        _translate = QtCore.QCoreApplication.translate
        ParamDialog.setWindowTitle(_translate("ParamDialog", "Dialog"))

