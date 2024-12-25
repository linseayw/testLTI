import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import cv2
import os

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(20, 60, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 60, 75, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 100, 361, 141))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(20, 20, 89, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 20, 89, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(250, 20, 89, 20))
        self.radioButton_3.setObjectName("radioButton_3")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(20, 70, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 49, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(110, 50, 49, 16))
        self.label_3.setObjectName("label_3")
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setGeometry(QtCore.QRect(110, 70, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_3.setGeometry(QtCore.QRect(250, 80, 42, 22))
        self.spinBox_3.setObjectName("spinBox_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(250, 40, 49, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(250, 60, 71, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(300, 270, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 20, 161, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(90, 250, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 250, 49, 16))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.add_video)
        self.pushButton_2.clicked.connect(self.remove_video)
        self.pushButton_4.clicked.connect(self.convert_video)

        self.video_path = ""

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Add video"))
        self.pushButton_2.setText(_translate("Form", "Remove"))
        self.groupBox.setTitle(_translate("Form", "Extract"))
        self.radioButton.setText(_translate("Form", "Every"))
        self.radioButton_2.setText(_translate("Form", "Every"))
        self.radioButton_3.setText(_translate("Form", "Total"))
        self.label_2.setText(_translate("Form", "Frames"))
        self.label_3.setText(_translate("Form", "Seconds"))
        self.label_4.setText(_translate("Form", "Frames"))
        self.label_5.setText(_translate("Form", "from video"))
        self.pushButton_4.setText(_translate("Form", "Convert"))
        self.label.setText(_translate("Form", "Convert video to image"))
        self.label_7.setText(_translate("Form", "Save To:"))

    def add_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi *.mkv)", options=options)
        if file_path:
            self.video_path = file_path
            QMessageBox.information(None, "Video Selected", f"Selected: {file_path}")

    def remove_video(self):
        self.video_path = ""
        QMessageBox.information(None, "Video Removed", "Video selection cleared.")

    def convert_video(self):
        if not self.video_path:
            QMessageBox.warning(None, "No Video", "Please add a video file first.")
            return

        save_path = self.lineEdit.text()
        if not save_path:
            QMessageBox.warning(None, "No Save Path", "Please specify a save path.")
            return

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            QMessageBox.critical(None, "Error", "Could not open video.")
            return

        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        os.makedirs(save_path, exist_ok=True)

        count = 0
        frame_number = 0

        if self.radioButton.isChecked():
            interval = self.spinBox.value()
            if interval <= 0:
                QMessageBox.warning(None, "Invalid Interval", "Frame interval must be greater than 0.")
                return
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if count % interval == 0:
                    cv2.imwrite(os.path.join(save_path, f"frame_{frame_number}.png"), frame)
                    frame_number += 1
                count += 1

        elif self.radioButton_2.isChecked():
            seconds = self.spinBox_2.value()
            if seconds <= 0:
                QMessageBox.warning(None, "Invalid Interval", "Seconds interval must be greater than 0.")
                return
            interval = int(frame_rate * seconds)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if count % interval == 0:
                    cv2.imwrite(os.path.join(save_path, f"frame_{frame_number}.png"), frame)
                    frame_number += 1
                count += 1

        elif self.radioButton_3.isChecked():
            total = self.spinBox_3.value()
            if total <= 0 or total > total_frames:
                QMessageBox.warning(None, "Invalid Total Frames", "Total frames must be between 1 and the total number of video frames.")
                return
            interval = total_frames // total
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if count % interval == 0 and frame_number < total:
                    cv2.imwrite(os.path.join(save_path, f"frame_{frame_number}.png"), frame)
                    frame_number += 1
                count += 1

        cap.release()
        QMessageBox.information(None, "Success", "Frames extracted successfully!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
