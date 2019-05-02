# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/springbok/Documents/UGent/[2019] Computergrafiek/Project/UI/Neuroviz.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_qmwMain(object):
    def setupUi(self, qmwMain):
        qmwMain.setObjectName("qmwMain")
        qmwMain.resize(800, 643)
        qmwMain.setAnimated(True)
        self.qwCentral = QtWidgets.QWidget(qmwMain)
        self.qwCentral.setObjectName("qwCentral")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.qwCentral)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.qwCentral)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.qwBasic = QtWidgets.QWidget()
        self.qwBasic.setObjectName("qwBasic")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.qwBasic)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.qvtkBasic = QVTKRenderWindowInteractor(self.qwBasic)
        self.qvtkBasic.setObjectName("qvtkBasic")
        self.verticalLayout_2.addWidget(self.qvtkBasic)
        self.tabWidget.addTab(self.qwBasic, "")
        self.qwEEG = QtWidgets.QWidget()
        self.qwEEG.setObjectName("qwEEG")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.qwEEG)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.qvtkEEG = QVTKRenderWindowInteractor(self.qwEEG)
        self.qvtkEEG.setObjectName("qvtkEEG")
        self.verticalLayout_3.addWidget(self.qvtkEEG)
        self.qvtkXY = QVTKRenderWindowInteractor(self.qwEEG)
        self.qvtkXY.setMaximumSize(QtCore.QSize(16777215, 300))
        self.qvtkXY.setObjectName("qvtkXY")
        self.verticalLayout_3.addWidget(self.qvtkXY)
        self.tabWidget.addTab(self.qwEEG, "")
        self.qwDSA = QtWidgets.QWidget()
        self.qwDSA.setObjectName("qwDSA")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.qwDSA)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.qvtkDSA = QVTKRenderWindowInteractor(self.qwDSA)
        self.qvtkDSA.setMinimumSize(QtCore.QSize(0, 512))
        self.qvtkDSA.setObjectName("qvtkDSA")
        self.verticalLayout_4.addWidget(self.qvtkDSA)
        self.tabWidget.addTab(self.qwDSA, "")
        self.verticalLayout.addWidget(self.tabWidget)
        qmwMain.setCentralWidget(self.qwCentral)
        self.qmbMenu = QtWidgets.QMenuBar(qmwMain)
        self.qmbMenu.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.qmbMenu.setObjectName("qmbMenu")
        qmwMain.setMenuBar(self.qmbMenu)
        self.qsbStatus = QtWidgets.QStatusBar(qmwMain)
        self.qsbStatus.setObjectName("qsbStatus")
        qmwMain.setStatusBar(self.qsbStatus)
        self.qdwDock = QtWidgets.QDockWidget(qmwMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qdwDock.sizePolicy().hasHeightForWidth())
        self.qdwDock.setSizePolicy(sizePolicy)
        self.qdwDock.setObjectName("qdwDock")
        self.qdwBasic = QtWidgets.QWidget()
        self.qdwBasic.setObjectName("qdwBasic")
        self.qdwDock.setWidget(self.qdwBasic)
        qmwMain.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.qdwDock)

        self.retranslateUi(qmwMain)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(qmwMain)

    def retranslateUi(self, qmwMain):
        _translate = QtCore.QCoreApplication.translate
        qmwMain.setWindowTitle(_translate("qmwMain", "Neuroviz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.qwBasic), _translate("qmwMain", "Basic Visualization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.qwEEG), _translate("qmwMain", "EEG Visualization"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.qwDSA), _translate("qmwMain", "DSA Visualization"))

from Neuroviz.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
