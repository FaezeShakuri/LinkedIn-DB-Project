# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_network.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_myNetwork(object):
    def setupUi(self, myNetwork):
        myNetwork.setObjectName("myNetwork")
        myNetwork.resize(617, 657)
        self.label = QtWidgets.QLabel(myNetwork)
        self.label.setGeometry(QtCore.QRect(40, 30, 67, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(myNetwork)
        self.label_2.setGeometry(QtCore.QRect(40, 330, 156, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listWidget_invitaion = QtWidgets.QListWidget(myNetwork)
        self.listWidget_invitaion.setGeometry(QtCore.QRect(40, 70, 271, 211))
        self.listWidget_invitaion.setObjectName("listWidget_invitaion")
        self.pushButton_accept = QtWidgets.QPushButton(myNetwork)
        self.pushButton_accept.setGeometry(QtCore.QRect(330, 72, 101, 31))
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.pushButton_decline = QtWidgets.QPushButton(myNetwork)
        self.pushButton_decline.setGeometry(QtCore.QRect(330, 110, 101, 31))
        self.pushButton_decline.setObjectName("pushButton_decline")
        self.listWidget_peopleYouyMayKnow = QtWidgets.QListWidget(myNetwork)
        self.listWidget_peopleYouyMayKnow.setGeometry(QtCore.QRect(40, 360, 271, 221))
        self.listWidget_peopleYouyMayKnow.setObjectName("listWidget_peopleYouyMayKnow")
        self.pushButton_showProfile = QtWidgets.QPushButton(myNetwork)
        self.pushButton_showProfile.setGeometry(QtCore.QRect(330, 400, 101, 31))
        self.pushButton_showProfile.setObjectName("pushButton_showProfile")
        self.pushButton_backToHome = QtWidgets.QPushButton(myNetwork)
        self.pushButton_backToHome.setGeometry(QtCore.QRect(480, 590, 111, 41))
        self.pushButton_backToHome.setObjectName("pushButton_backToHome")
        self.message = QtWidgets.QLabel(myNetwork)
        self.message.setGeometry(QtCore.QRect(130, 590, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setText("")
        self.message.setObjectName("message")
        self.pushButton_invite = QtWidgets.QPushButton(myNetwork)
        self.pushButton_invite.setGeometry(QtCore.QRect(330, 360, 101, 31))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.pushButton_refresh = QtWidgets.QPushButton(myNetwork)
        self.pushButton_refresh.setGeometry(QtCore.QRect(560, 10, 60, 41))
        self.pushButton_refresh.setText("Refresh")
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("refreshIcon.png"))
        # self.pushButton_refresh.setIcon(QtGui.QIcon('refreshIcon.png'))
        # self.pushButton_refresh.setStyleSheet("background-image : url(refreshIcon.png);")
        # self.pushButton_refresh.resize(35, 35)
        # self.pushButton_refresh.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_refresh.setObjectName("pushButton_refresh")

        self.retranslateUi(myNetwork)
        QtCore.QMetaObject.connectSlotsByName(myNetwork)

    def retranslateUi(self, myNetwork):
        _translate = QtCore.QCoreApplication.translate
        myNetwork.setWindowTitle(_translate("myNetwork", "My network"))
        self.label.setText(_translate("myNetwork", "Invitation"))
        self.label_2.setText(_translate("myNetwork", "People you may know"))
        self.pushButton_accept.setText(_translate("myNetwork", "accept"))
        self.pushButton_decline.setText(_translate("myNetwork", "decline"))
        self.pushButton_showProfile.setText(_translate("myNetwork", "Show profile"))
        self.pushButton_backToHome.setText(_translate("myNetwork", "back to home"))
        self.pushButton_invite.setText(_translate("myNetwork", "Invite"))
        self.pushButton_refresh.setShortcut(_translate("myNetwork", "Return"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myNetwork = QtWidgets.QWidget()
    ui = Ui_myNetwork()
    ui.setupUi(myNetwork)
    myNetwork.show()
    sys.exit(app.exec_())