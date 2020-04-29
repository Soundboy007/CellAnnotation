# -*- coding: utf-8 -*-

# This file runs the GUI for image segmentation and uploading images onto Microsoft Azure and AWS MTurk

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
import PreprocessLargeImage
import pushazureblob
import SubmitTask
import importannotations
import PostprocessLargeImage
import os

# Making the GUI and adding widgets
class Ui_images(QtWidgets.QWidget):
    def setupUi(self, images):
        images.setObjectName("images")
        images.resize(1260, 240)
        self.centralwidget = QtWidgets.QWidget(images)
        self.centralwidget.setObjectName("centralwidget")
        self.button_preprocess = QtWidgets.QPushButton(self.centralwidget)
        self.button_preprocess.setGeometry(QtCore.QRect(50, 70, 250, 70))
        self.button_preprocess.setObjectName("button_preprocess")
        self.button_crowdsource = QtWidgets.QPushButton(self.centralwidget)
        self.button_crowdsource.setGeometry(QtCore.QRect(330, 70, 250, 70))
        self.button_crowdsource.setObjectName("button_crowdsource")
        self.button_retrieve = QtWidgets.QPushButton(self.centralwidget)
        self.button_retrieve.setGeometry(QtCore.QRect(610, 70, 250, 70))
        self.button_retrieve.setObjectName("button_retrieve")
        self.button_postprocess = QtWidgets.QPushButton(self.centralwidget)
        self.button_postprocess.setGeometry(QtCore.QRect(890, 70, 250, 70))
        self.button_postprocess.setObjectName("button_postprocess")
        images.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(images)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 603, 20))
        self.menubar.setObjectName("menubar")
        images.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(images)
        self.statusbar.setObjectName("statusbar")
        images.setStatusBar(self.statusbar)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 160, 171, 61))

        self.retranslateUi(images)
        QtCore.QMetaObject.connectSlotsByName(images)

        self.button_preprocess.clicked.connect(self.imgCut)
        self.button_crowdsource.clicked.connect(self.crowdsource)
        self.button_retrieve.clicked.connect(self.retrieve)
        self.button_postprocess.clicked.connect(self.postprocess)

    # Adding functionality to widgets
    def retranslateUi(self, images):
        _translate = QtCore.QCoreApplication.translate
        images.setWindowTitle(_translate("images", "Crowdsourcing Annotations"))
        self.button_preprocess.setText(_translate("images", "Preprocess Imgs"))
        self.button_crowdsource.setText(_translate("images", "Crowdsource"))
        self.button_retrieve.setText(_translate("images", "Retrieve Results"))
        self.button_postprocess.setText(_translate("images", "Postprocess Imgs"))

    # Cutting an image into 9 segments for easier annotation
    def imgCut(self):
        images_to_cut = QFileDialog.getOpenFileNames(self, 'Open file', 'c:\\', "Image files (*.jpg *.tif *.png)")
        files = images_to_cut[0]
        if len(files) > 0:
            PreprocessLargeImage.preprocess(files[0], files[1])
        #print(fname)
        #print(files)

    imagepaths = ''
    imagenames = ''

    # Crowdsource the segments to AWS MTurk
    def crowdsource(self):
        global imagepaths
        global imagenames
        folder_to_crowdsource = QFileDialog.getExistingDirectory(self, 'Select Directory')
        folderpath = folder_to_crowdsource
        def fileiter(filename, segment = 1):
            filepaths, filenames, i = [], [], 0
            for subdir, dirs, files in os.walk(filename):
                for file in files:
                    i += 1
                    if i == segment and file.endswith('jpg'):
                        # print(subdir + os.sep + file)
                        filepaths.append(subdir + os.sep + file)
                        filenames.append(file)
                        i = 0
                        break
            return filepaths, filenames

        imagepaths, imagenames = fileiter(folderpath, 1)
        #print(imagepaths)
        #print(imagenames)

        # replacing the images in the javascript file before pushing all web files into Azure Blob Storage 
        with open('C:/Users/Anand/Desktop/Sai Anand Maringanti/refScript.js') as fin, open('C:/Users/Anand/Desktop/Sai Anand Maringanti/Script.js', 'w') as fout:
            for line in fin:
                if "img.src = 'merged" in line:
                    #print([x for x in imagenames if 'merged' in x][0])
                    line = "\timg.src = '" + [x for x in imagenames if 'merged' in x][0] + "';\n"
                if "img2.src = 'embryo-d_lifeact" in line:
                    #print([x for x in imagenames if 'embryo-d_lifeact' in x][0])
                    line = "\timg2.src = '" + [x for x in imagenames if 'embryo-d_lifeact' in x][0] + "';\n"
                fout.write(line)
             
        # Pushing the files into an Azure blob
        pushazureblob.run_sample(imagenames, imagepaths)
        link = SubmitTask.runSubmitTask()
        print(link)
        urlLink = " <a href=" + link + "> <font face=verdana size=3 color=blue> Link to Amazon Amt </font> </a>"
        self.label.setText(urlLink)
        self.label.setOpenExternalLinks(True)
        self.label.adjustSize()

    # Retrieve annotated results after crowdworkers finish their task and importing the annotations onto the respective images
    def retrieve(self):
        answer = SubmitTask.runRetrieveResults()
        print(answer)

        # responses = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "files (*.txt *.tsv)")
        # responses = (responses[0])
        # originalpath = [x for x in imagepaths if 'embryo-d_lifeact' in x][0]
        # mergedname = [x for x in imagenames if 'merged' in x][0]

        importannotations.annotate()

    # Postprocess the nine different segments of images into one big image
    def postprocess(self):
        folder_to_concatnate = QFileDialog.getExistingDirectory(self, 'Select Directory')
        basepath = folder_to_concatnate + '/'
        PostprocessLargeImage.postprocess(basepath)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    images = QtWidgets.QMainWindow()
    ui = Ui_images()
    ui.setupUi(images)
    images.show()
    sys.exit(app.exec_())
