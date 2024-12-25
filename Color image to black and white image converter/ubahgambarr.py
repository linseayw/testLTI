# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 200, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 250, 191, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 250, 171, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 70, 121, 121))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 70, 121, 121))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(60, 40, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(240, 40, 121, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(80, 20, 251, 16))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "ADD IMAGE"))
        self.pushButton_2.setText(_translate("Form", "convert"))
        self.pushButton_3.setText(_translate("Form", "Save As"))
        self.label_3.setText(_translate("Form", "Original Image"))
        self.label_4.setText(_translate("Form", "Black and White Image"))
        self.label_5.setText(_translate("Form", "Convert images from color to black and white"))

class ImageConverter(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.bw_image = None

        # Connect buttons
        self.pushButton.clicked.connect(self.load_image)
        self.pushButton_2.clicked.connect(self.convert_to_bw)
        self.pushButton_3.clicked.connect(self.save_image)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.image_path = file_name
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.label)
            print(f"Loaded image from: {file_name}")

    def convert_to_bw(self):
        if self.original_image is not None:
            try:
                gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                self.bw_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                self.display_image(self.bw_image, self.label_2)
                print("Image converted to black and white.")
            except Exception as e:
                print(f"Error during conversion: {e}")
        else:
            print("No image loaded to convert.")

    def save_image(self):
        if self.bw_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if file_name:
                # Ensure file has an appropriate extension
                if not (file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".bmp")):
                    file_name += ".png"  # Default format
                file_name = QtCore.QDir.toNativeSeparators(file_name)  # Ensure native file path format
                try:
                    cv2.imwrite(file_name, self.bw_image)
                    print(f"File saved successfully at {file_name}")
                except Exception as e:
                    print(f"Error saving file: {e}")
            else:
                print("Save canceled or invalid file name.")
        else:
            print("No image to save.")

    def display_image(self, image, label):
        try:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
        except Exception as e:
            print(f"Error displaying image: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec_())
