import sys
import os
import re

import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.2
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Turn Simulator')

        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene(self.graphicsView)
        self.scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(self.scene)

        self.plot_button = QPushButton("plot", self)
        self.plot_button.setCheckable(True)
        self.plot_button.toggled.connect(self.slot_plot_button_toggled)

        self.save_button = QPushButton("save", self)
        self.save_button.clicked.connect(self.slot_save_button_pushed)

        validator = QDoubleValidator(-400, 400, 2)
        self.paramEdit1 = QLineEdit()
        self.paramEdit1.setValidator(validator)
        param1layout = QHBoxLayout()
        param1layout.addWidget(QLabel("inner offset:"))
        param1layout.addWidget(self.paramEdit1)
        param1layout.addWidget(QLabel("[mm]"))

        self.paramEdit2 = QLineEdit()
        self.paramEdit2.setValidator(validator)
        param2layout = QHBoxLayout()
        param2layout.addWidget(QLabel("radius:"))
        param2layout.addWidget(self.paramEdit2)
        param2layout.addWidget(QLabel("[mm]"))

        self.paramEdit3 = QLineEdit()
        self.paramEdit3.setValidator(validator)
        param3layout = QHBoxLayout()
        param3layout.addWidget(QLabel("machine width:"))
        param3layout.addWidget(self.paramEdit3)
        param3layout.addWidget(QLabel("[mm]"))

        self.paramOutput1 = QLineEdit()
        self.paramOutput1.setValidator(validator)
        self.paramOutput1.setReadOnly(True)
        param4layout = QHBoxLayout()
        param4layout.addWidget(QLabel("outer:"))
        param4layout.addWidget(self.paramOutput1)
        param4layout.addWidget(QLabel("[mm]"))

        self.combo = QComboBox(self)
        self.combo.addItem("-- select --")
        self.combo.addItem("90(search)")
        self.combo.addItem("45")
        self.combo.addItem("90(short)")
        self.combo.addItem("135")
        self.combo.addItem("180")
        self.combo.addItem("90(slanting)")
        self.pattern = ""
        self.combo.activated[str].connect(self.slot_pattern_combo)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.plot_button)
        layout2.addWidget(self.save_button)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.combo)
        layout3.addLayout(param1layout)
        layout3.addLayout(param2layout)
        layout3.addLayout(param3layout)
        layout3.addLayout(param4layout)

        layout1 = QVBoxLayout()
        layout1.addWidget(self.graphicsView)

        mainlayout = QHBoxLayout()

        layout1.addLayout(layout2)
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout3)
        self.setLayout(mainlayout)

    def slot_plot_button_toggled(self, checked):
        if checked:
            if self.pattern == "90(search)":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 200
                    self.paramEdit1.setText(str(90))
                else:
                    start_y = 275 - float(self.paramEdit1.text())/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(start_x-machineWidth/2, 350, start_x-machineWidth/2, start_y)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(start_x+machineWidth/2, 350, start_x+machineWidth/2, start_y)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 90
                if self.paramEdit2.text() == "":
                    radius = 75
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 355, end_y)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str((end_x-200)*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2, start_y)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2, start_y)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x, end_y-machineWidth/2, 355, end_y-machineWidth/2)
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x, end_y+machineWidth/2, 355, end_y+machineWidth/2)
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)
            elif self.pattern == "45":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 275
                    self.paramEdit1.setText(str(90))
                else:
                    start_y = 275 - float(self.paramEdit1.text())/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(start_x-machineWidth/2, 350, start_x-machineWidth/2, start_y)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(start_x+machineWidth/2, 350, start_x+machineWidth/2, start_y)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 45
                if self.paramEdit2.text() == "":
                    radius = 200
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, end_x+end_y-50, 50)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(np.sqrt(2*(end_y-50)*(end_y-50))*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2, start_y)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2, start_y)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x-machineWidth/2*np.sqrt(2)/2, end_y-machineWidth/2*np.sqrt(2)/2, end_x+end_y-50-machineWidth/2*np.sqrt(2)/2, 50-machineWidth/2*np.sqrt(2)/2)
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x+machineWidth/2*np.sqrt(2)/2, end_y+machineWidth/2*np.sqrt(2)/2, end_x+end_y-50+machineWidth/2*np.sqrt(2)/2, 50+machineWidth/2*np.sqrt(2)/2)
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)
            elif self.pattern == "90(short)":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 275
                    self.paramEdit1.setText(str(90))
                else:
                    start_y = 275 - float(self.paramEdit1.text())/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(start_x-machineWidth/2, 350, start_x-machineWidth/2, start_y)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(start_x+machineWidth/2, 350, start_x+machineWidth/2, start_y)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 90
                if self.paramEdit2.text() == "":
                    radius = 150
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 355, end_y)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str((end_x-200)*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2, start_y)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2, start_y)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x, end_y-machineWidth/2, 355, end_y-machineWidth/2)
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x, end_y+machineWidth/2, 355, end_y+machineWidth/2)
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)
            elif self.pattern == "135":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 275
                    self.paramEdit1.setText(str(90))
                else:
                    start_y = 275 - float(self.paramEdit1.text())/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(start_x-machineWidth/2, 350, start_x-machineWidth/2, start_y)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(start_x+machineWidth/2, 350, start_x+machineWidth/2, start_y)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 135
                if self.paramEdit2.text() == "":
                    radius = 100
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 350, end_y+350-end_x)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(np.sqrt(2*(end_x-350)*(end_x-350))*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2, start_y)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2, start_y)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x+machineWidth/2*np.sqrt(2)/2, end_y-machineWidth/2*np.sqrt(2)/2, 350, end_y+350-end_x-machineWidth/2*np.sqrt(2))
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x-machineWidth/2*np.sqrt(2)/2, end_y+machineWidth/2*np.sqrt(2)/2, 350, end_y+350-end_x+machineWidth/2*np.sqrt(2))
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)
            elif self.pattern == "180":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                start_x = 125
                if self.paramEdit1.text() == "":
                    start_y = 200
                    self.paramEdit1.setText(str(90))
                else:
                    start_y = 200 - float(self.paramEdit1.text())/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(start_x, 350, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(start_x-machineWidth/2, 350, start_x-machineWidth/2, start_y)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(start_x+machineWidth/2, 350, start_x+machineWidth/2, start_y)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 180
                if self.paramEdit2.text() == "":
                    radius = 75
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius
                rad_y = start_y
                end_x = start_x + radius - radius * np.cos(np.deg2rad(angle))
                end_y = start_y - radius * np.sin(np.deg2rad(angle))
                startAngle = -180
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, end_x, 350)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str((end_y-350)*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2, start_y)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2, start_y)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x-machineWidth/2, end_y, end_x-machineWidth/2, 350)
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x+machineWidth/2, end_y, end_x+machineWidth/2, 350)
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)
            elif self.pattern == "90(slanting)":
                self.maze_draw(self.pattern)
                arc = QGraphicsPathItem()
                path = QPainterPath()
                outerArc = QGraphicsPathItem()
                outerPath = QPainterPath()
                innerArc = QGraphicsPathItem()
                innerPath = QPainterPath()
                if self.paramEdit1.text() == "":
                    start_x = 125
                    start_y = 200
                    self.paramEdit1.setText(str(90))
                else:
                    start_x = 125 + float(self.paramEdit1.text())/np.sqrt(2)/self.scale
                    start_y = 200 - float(self.paramEdit1.text())/np.sqrt(2)/self.scale

                if self.paramEdit3.text() == "":
                    machineWidth = 80/self.scale
                    self.paramEdit3.setText(str(80))
                else:
                    machineWidth = float(self.paramEdit3.text())/self.scale

                InnerLine = QGraphicsLineItem(50, 275, start_x, start_y)
                InnerLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.scene.addItem(InnerLine)

                InnerMachineLineInner = QGraphicsLineItem(50-machineWidth/2*np.sqrt(2)/2, 275-machineWidth/2*np.sqrt(2)/2, start_x-machineWidth/2*np.sqrt(2)/2, start_y-machineWidth/2*np.sqrt(2)/2)
                InnerMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineInner)

                OuterMachineLineInner = QGraphicsLineItem(50+machineWidth/2*np.sqrt(2)/2, 275+machineWidth/2*np.sqrt(2)/2, start_x+machineWidth/2*np.sqrt(2)/2, start_y+machineWidth/2*np.sqrt(2)/2)
                OuterMachineLineInner.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineInner)

                angle = 90
                if self.paramEdit2.text() == "":
                    radius = 75
                    self.paramEdit2.setText(str(radius*self.scale))
                else:
                    radius = float(self.paramEdit2.text())/self.scale
                rad_x = start_x + radius/np.sqrt(2)
                rad_y = start_y + radius/np.sqrt(2)
                end_x = start_x + 2 * radius/np.sqrt(2)
                end_y = start_y
                startAngle = -225
                path.moveTo(start_x, start_y)
                path.arcTo(rad_x-radius, rad_y-radius, radius*2, radius*2, startAngle, -angle)
                arc.setPen(QPen(Qt.red, 3, Qt.SolidLine))
                arc.setPath(path)
                OuterLine = QGraphicsLineItem(end_x, end_y, 350, end_y+350-end_x)
                OuterLine.setPen(QPen(Qt.blue, 3, Qt.SolidLine))
                self.paramOutput1.setText(str(np.sqrt(2*(end_x-350)*(end_x-350))*self.scale))
                self.scene.addItem(OuterLine)
                self.scene.addItem(arc)

                outerPath.moveTo(start_x-machineWidth/2*np.sqrt(2)/2, start_y-machineWidth/2*np.sqrt(2)/2)
                outerPath.arcTo(rad_x-radius-machineWidth/2, rad_y-radius-machineWidth/2, radius*2+machineWidth, radius*2+machineWidth, startAngle, -angle)
                outerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                outerArc.setPath(outerPath)
                self.scene.addItem(outerArc)

                innerPath.moveTo(start_x+machineWidth/2*np.sqrt(2)/2, start_y+machineWidth/2*np.sqrt(2)/2)
                innerPath.arcTo(rad_x-radius+machineWidth/2, rad_y-radius+machineWidth/2, radius*2-machineWidth, radius*2-machineWidth, startAngle, -angle)
                innerArc.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                innerArc.setPath(innerPath)
                self.scene.addItem(innerArc)

                InnerMachineLineOuter = QGraphicsLineItem(end_x+machineWidth/4*(np.sqrt(2)), end_y-machineWidth/4*(np.sqrt(2)), 350+machineWidth/4*(np.sqrt(2)), end_y+350-end_x-machineWidth/4*(np.sqrt(2)))
                InnerMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(InnerMachineLineOuter)
                OuterMachineLineOuter = QGraphicsLineItem(end_x-machineWidth/4*(np.sqrt(2)), end_y+machineWidth/4*(np.sqrt(2)), 350-machineWidth/4*(np.sqrt(2)), end_y+350-end_x+machineWidth/4*(np.sqrt(2)))
                OuterMachineLineOuter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
                self.scene.addItem(OuterMachineLineOuter)

            else:
                pass
        else:
            pass

    def slot_save_button_pushed(self):
        try:
            pass
        except:
            pass

    def slot_pattern_combo(self, pattern):
        self.pattern = pattern
        self.maze_draw(pattern)
    def maze_draw(self, pattern):
        if pattern == "90(search)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(345, 45, 10, 160)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "45":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 45, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(rect4)
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "90(short)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 200)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 200, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(345, 45, 10, 160)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 160, 10))
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
        elif pattern == "135":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(345, 195, 10, 160)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(rect5)
            self.scene.addItem(QGraphicsRectItem(195, 345, 160, 10))
        elif pattern == "180":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 345, 160, 10)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(195, 345, 160, 10)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(QGraphicsRectItem(45, 195, 10, 160))
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(rect1)
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(QGraphicsRectItem(345, 195, 10, 160))
            self.scene.addItem(rect5)
        elif pattern == "90(slanting)":
            self.scene.clear()
            centerLine1 = QGraphicsLineItem(125, 50, 125, 350)
            centerLine1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine1)
            centerLine2 = QGraphicsLineItem(50, 125, 350, 125)
            centerLine2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine2)
            centerLine3 = QGraphicsLineItem(275, 50, 275, 350)
            centerLine3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine3)
            centerLine4 = QGraphicsLineItem(50, 275, 350, 275)
            centerLine4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(centerLine4)
            rect1 = QGraphicsRectItem(45, 195, 10, 160)
            rect1.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect2 = QGraphicsRectItem(45, 195, 160, 10)
            rect2.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect3 = QGraphicsRectItem(195, 45, 10, 160)
            rect3.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect4 = QGraphicsRectItem(195, 195, 160, 10)
            rect4.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            rect5 = QGraphicsRectItem(345, 195, 10, 160)
            rect5.setPen(QPen(Qt.black, 0.5, Qt.DashLine))
            self.scene.addItem(QGraphicsRectItem(45, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 45, 10, 160))
            self.scene.addItem(rect1)
            self.scene.addItem(rect3)
            self.scene.addItem(rect2)
            self.scene.addItem(QGraphicsRectItem(195, 45, 160, 10))
            self.scene.addItem(QGraphicsRectItem(45, 345, 160, 10))
            self.scene.addItem(QGraphicsRectItem(345, 45, 10, 160))
            self.scene.addItem(rect4)
            self.scene.addItem(QGraphicsRectItem(195, 195, 10, 160))
            self.scene.addItem(rect5)
            self.scene.addItem(QGraphicsRectItem(195, 345, 160, 10))
        else:
            self.scene.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
