from inputs import get_gamepad
import threading
import time
import sys
import json
import math
from PyQt5.QtCore import Qt, QObject, QThread, QRunnable, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox, QDialog, QSizePolicy, QStyleFactory,
                             QLabel, QLineEdit, QProgressBar, QPushButton, QWidget, QPlainTextEdit)
import pyautogui

class XboxBinder(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LRDPad = 0
        self.UDDPad = 0

    def bindKey(self):
        while (round(max(abs(inputs))) != 1):
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'ABS_HAT0X':
                    self.LRDPad = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.UDDPad = event.state
            inputs = [self.LeftJoystickY, self.LeftJoystickX, self.RightJoystickY, self.RightJoystickX, self.LeftTrigger, self.RightTrigger, self.LeftBumper, self.RightBumper, self.A, self.X, self.Y, self.B, self.LeftThumb, self.RightThumb, self.Back, self.Start, self.LRDPad, self.UDDPad]

        if (round(abs(inputs[0])) == 1):
            return ['ABS_Y', self.LeftJoystickY * XboxController.MAX_JOY_VAL]
        elif (round(abs(inputs[1])) == 1):
            return ['ABS_X', self.LeftJoystickX * XboxController.MAX_JOY_VAL]
        elif (round(abs(inputs[2])) == 1):
            return ['ABS_RY', self.RightJoystickY * XboxController.MAX_JOY_VAL]
        elif (round(abs(inputs[3])) == 1):
            return ['ABS_RX', self.RightJoystickX * XboxController.MAX_JOY_VAL]
        elif (round(abs(inputs[4])) == 1):
            return ['ABS_Z', self.LeftTrigger * XboxController.MAX_TRIG_VAL]
        elif (round(abs(inputs[5])) == 1):
            return ['ABS_RZ', self.RightTrigger * XboxController.MAX_TRIG_VAL]
        elif (round(abs(inputs[6])) == 1):
            return ['BTN_TL', self.LeftBumper]
        elif (round(abs(inputs[7])) == 1):
            return ['BTN_TR', self.RightBumper]
        elif (round(abs(inputs[8])) == 1):
            return ['BTN_SOUTH', self.A]
        elif (round(abs(inputs[9])) == 1):
            return ['BTN_NORTH', self.X]
        elif (round(abs(inputs[10])) == 1):
            return ['BTN_WEST', self.Y]
        elif (round(abs(inputs[11])) == 1):
            return ['BTN_EAST', self.B]
        elif (round(abs(inputs[12])) == 1):
            'BTN_THUMBL'
            self.LeftThumb = event.state
        elif (round(abs(inputs[13])) == 1):
            return ['BTN_THUMBR', self.RightThumb]
        elif (round(abs(inputs[14])) == 1):
            return ['BTN_SELECT', self.Back]
        elif (round(abs(inputs[15])) == 1):
            return ['BTN_START', self.Start]
        elif (round(abs(inputs[16])) == 1):
            return ['ABS_HAT0X', self.LRDPad]
        elif (round(abs(inputs[17])) == 1):
            return ['ABS_HAT0Y', self.UDDPad]

class XboxController(object):

    def __init__(self, inputStrs):

        self.inputStrings = inputStrs

        self.firstInput = 0
        self.secondInput = 0
        self.thirdInput = 0
        self.fourthInput = 0
        self.fifthInput = 0
        self.sixthInput = 0
        self.seventhInput = 0
        self.eigthInput = 0

    def startThread(self):
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def endThread(self):
        self._monitor_thread.join()

    def read(self): # return the buttons/triggers that you care about in this methode
        return [self.firstInput, self.secondInput, self.thirdInput, self.fourthInput, self.fifthInput, self.sixthInput, self.seventhInput, self.eigthInput]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == self.inputStrings[0]:
                    self.firstInput = event.state
                elif event.code == self.inputStrings[1]:
                    self.secondInput = event.state 
                elif event.code == self.inputStrings[2]:
                    self.thirdInput = event.state
                elif event.code == self.inputStrings[3]:
                    self.fourthInput = event.state
                elif event.code == self.inputStrings[4]:
                    self.fifthInput = event.state
                elif event.code == self.inputStrings[5]:
                    self.sixthInput = event.state
                elif event.code == self.inputStrings[6]:
                    self.seventhInput = event.state
                elif event.code == self.inputStrings[7]:
                    self.eigthInput = event.state

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.setMinimumSize(500, 500)
        self.setWindowTitle("HoloCure Gamepad Bindings")

        self.overallWidget()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.fullWidget, 1, 0, 1, 1)

        self.setLayout(mainLayout)

        self.changeStyle('windowsvista')

        # order of inputs: up, down, left, right, strafe, pet, special, enter
        self.gameBindings = ["w","s","a","d","shift","p","space","enter"]
        self.padBindings = ["ABS_Y","ABS_Y","ABS_X","ABS_X","ABS_Z","BTN_THUMBL","BTN_TL","ABS_HAT0Y"]
        self.padValues = [1,-1,-1,1,1,1,-1,1]

        self.loadSettings()
        
        self.joyBinder = XboxBinder()

    def overallWidget(self):

        self.fullWidget = QWidget()
        self.fullWidgetLayout = QGridLayout()

        self.gameBindBox = QGroupBox("Game Keybinds")
        self.padBindBox = QGroupBox("Controller Keybinds")
        self.controlGroupBox = QGroupBox("Pad Control")

        self.upGameText = QLabel("Up")
        self.upGameBox = QLineEdit("w")
        self.downGameText = QLabel("Down")
        self.downGameBox = QLineEdit("s")
        self.leftGameText = QLabel("Left")
        self.leftGameBox = QLineEdit("a")
        self.rightGameText = QLabel("Right")
        self.rightGameBox = QLineEdit("d")
        self.strafeGameText = QLabel("Strafe/Confirm")
        self.strafeGameBox = QLineEdit("shift")
        self.specialGameText = QLabel("Special/Back")
        self.specialGameBox = QLineEdit("space")

        self.gameLayout = QGridLayout()
        self.gameLayout.addWidget(self.upGameText, 0, 0, 1, 1)
        self.gameLayout.addWidget(self.upGameBox, 0, 1, 1, 1)
        self.gameLayout.addWidget(self.downGameText, 1, 0, 1, 1)
        self.gameLayout.addWidget(self.downGameBox, 1, 1, 1, 1)
        self.gameLayout.addWidget(self.leftGameText, 2, 0, 1, 1)
        self.gameLayout.addWidget(self.leftGameBox, 2, 1, 1, 1)
        self.gameLayout.addWidget(self.rightGameText, 3, 0, 1, 1)
        self.gameLayout.addWidget(self.rightGameBox, 3, 1, 1, 1)
        self.gameLayout.addWidget(self.strafeGameText, 4, 0, 1, 1)
        self.gameLayout.addWidget(self.strafeGameBox, 4, 1, 1, 1)
        self.gameLayout.addWidget(self.specialGameText, 5, 0, 1, 1)
        self.gameLayout.addWidget(self.specialGameBox, 5, 1, 1, 1)
        self.gameBindBox.setLayout(self.gameLayout)

        self.upPadText = QLabel("Up: ")
        self.upPadBox = QLabel("ABS_Y")
        self.upPadIntensityBox = QLabel("1")
        self.upPadButton = QPushButton("Bind")
        self.upPadButton.clicked.connect(self.upPadBind)
        self.downPadText = QLabel("Down Key: ")
        self.downPadBox = QLabel("ABS_Y")
        self.downPadIntensityBox = QLabel("-1")
        self.downPadButton = QPushButton("Bind")
        self.downPadButton.clicked.connect(self.downPadBind)
        self.leftPadText = QLabel("Left: ")
        self.leftPadBox = QLabel("ABS_X")
        self.leftPadIntensityBox = QLabel("-1")
        self.leftPadButton = QPushButton("Bind")
        self.leftPadButton.clicked.connect(self.leftPadBind)
        self.rightPadText = QLabel("Right: ")
        self.rightPadBox = QLabel("ABS_X")
        self.rightPadIntensityBox = QLabel("1")
        self.rightPadButton = QPushButton("Bind")
        self.rightPadButton.clicked.connect(self.rightPadBind)
        self.strafePadText = QLabel("Strafe/Confirm: ")
        self.strafePadBox = QLabel("ABS_Z")
        self.strafePadIntensityBox = QLabel("1")
        self.strafePadButton = QPushButton("Bind")
        self.strafePadButton.clicked.connect(self.strafePadBind)
        self.specialPadText = QLabel("Special/Back: ")
        self.specialPadBox = QLabel("BTN_TL")
        self.specialPadIntensityBox = QLabel("1")
        self.specialPadButton = QPushButton("Bind")
        self.specialPadButton.clicked.connect(self.specialPadBind)
        self.enterPadText = QLabel("Enter: ")
        self.enterPadBox = QLabel("ABS_HAT0Y")
        self.enterPadIntensityBox = QLabel("-1")
        self.enterPadButton = QPushButton("Bind")
        self.enterPadButton.clicked.connect(self.enterPadBind)
        self.petPadText = QLabel("Pet Bubba: ")
        self.petPadBox = QLabel("BTN_THUMBL")
        self.petPadIntensityBox = QLabel("1")
        self.petPadButton = QPushButton("Bind")
        self.petPadButton.clicked.connect(self.petPadBind)

        self.padBindLayout = QGridLayout()
        self.padBindLayout.addWidget(self.upPadText, 0, 0, 1, 1)
        self.padBindLayout.addWidget(self.upPadBox, 0, 1, 1, 1)
        self.padBindLayout.addWidget(self.upPadIntensityBox, 0, 2, 1, 1)
        self.padBindLayout.addWidget(self.upPadButton, 0, 3, 1, 1)
        self.padBindLayout.addWidget(self.downPadText, 1, 0, 1, 1)
        self.padBindLayout.addWidget(self.downPadBox, 1, 1, 1, 1)
        self.padBindLayout.addWidget(self.downPadIntensityBox, 1, 2, 1, 1)
        self.padBindLayout.addWidget(self.downPadButton, 1, 3, 1, 1)
        self.padBindLayout.addWidget(self.leftPadText, 2, 0, 1, 1)
        self.padBindLayout.addWidget(self.leftPadBox, 2, 1, 1, 1)
        self.padBindLayout.addWidget(self.leftPadIntensityBox, 2, 2, 1, 1)
        self.padBindLayout.addWidget(self.leftPadButton, 2, 3, 1, 1)
        self.padBindLayout.addWidget(self.rightPadText, 3, 0, 1, 1)
        self.padBindLayout.addWidget(self.rightPadBox, 3, 1, 1, 1)
        self.padBindLayout.addWidget(self.rightPadIntensityBox, 3, 2, 1, 1)
        self.padBindLayout.addWidget(self.rightPadButton, 3, 3, 1, 1)
        self.padBindLayout.addWidget(self.strafePadText, 4, 0, 1, 1)
        self.padBindLayout.addWidget(self.strafePadBox, 4, 1, 1, 1)
        self.padBindLayout.addWidget(self.strafePadIntensityBox, 4, 2, 1, 1)
        self.padBindLayout.addWidget(self.strafePadButton, 4, 3, 1, 1)
        self.padBindLayout.addWidget(self.specialPadText, 5, 0, 1, 1)
        self.padBindLayout.addWidget(self.specialPadBox, 5, 1, 1, 1)
        self.padBindLayout.addWidget(self.specialPadIntensityBox, 5, 2, 1, 1)
        self.padBindLayout.addWidget(self.specialPadButton, 5, 3, 1, 1)
        self.padBindLayout.addWidget(self.enterPadText, 6, 0, 1, 1)
        self.padBindLayout.addWidget(self.enterPadBox, 6, 1, 1, 1)
        self.padBindLayout.addWidget(self.enterPadIntensityBox, 6, 2, 1, 1)
        self.padBindLayout.addWidget(self.enterPadButton, 6, 3, 1, 1)
        self.padBindLayout.addWidget(self.petPadText, 7, 0, 1, 1)
        self.padBindLayout.addWidget(self.petPadBox, 7, 1, 1, 1)
        self.padBindLayout.addWidget(self.petPadIntensityBox, 7, 2, 1, 1)
        self.padBindLayout.addWidget(self.petPadButton, 7, 3, 1, 1)
        self.padBindBox.setLayout(self.padBindLayout)

        self.saveButton = QPushButton("Save Settings")
        self.saveButton.clicked.connect(self.saveSettings)

        self.freeControlButton = QPushButton("Pad Control")
        self.freeControlButton.setStyleSheet("background-color : lightgrey")
        self.freeControlButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.freeControlButton.setCheckable(True)
        self.freeControlButton.clicked.connect(self.togglePadControl)

        self.controlLayout = QGridLayout()
        self.controlLayout.addWidget(self.saveButton, 0, 0, 1, 1)
        self.controlLayout.addWidget(self.freeControlButton, 0, 1, 1, 1)
        self.controlLayout.setVerticalSpacing(0)
        self.controlGroupBox.setLayout(self.controlLayout)

        self.fullWidgetLayout.addWidget(self.gameBindBox, 0, 0, 1, 1)
        self.fullWidgetLayout.addWidget(self.padBindBox, 0, 1, 1, 1)
        self.fullWidgetLayout.addWidget(self.controlGroupBox, 1, 0, 1, 2)
        self.fullWidgetLayout.setRowStretch(3,1)
        self.fullWidget.setLayout(self.fullWidgetLayout)

    def upPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[0] = bindVals[0]
        self.padValues[0] = bindVals[1]

        self.upPadBox.setText(bindVals[0])
        self.upPadIntensityBox.setText(bindVals[1])
    
    def downPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[1] = bindVals[0]
        self.padValues[1] = bindVals[1]

        self.downPadBox.setText(bindVals[0])
        self.downPadIntensityBox.setText(bindVals[1])
    
    def leftPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[2] = bindVals[0]
        self.padValues[2] = bindVals[1]

        self.leftPadBox.setText(bindVals[0])
        self.leftPadIntensityBox.setText(bindVals[1])

    def rightPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[3] = bindVals[0]
        self.padValues[3] = bindVals[1]

        self.rightPadBox.setText(bindVals[0])
        self.rightPadIntensityBox.setText(bindVals[1])

    def strafePadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[4] = bindVals[0]
        self.padValues[4] = bindVals[1]

        self.strafePadBox.setText(bindVals[0])
        self.strafePadIntensityBox.setText(bindVals[1])

    def petPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[5] = bindVals[0]
        self.padValues[5] = bindVals[1]

        self.petPadBox.setText(bindVals[0])
        self.petPadIntensityBox.setText(bindVals[1])

    def specialPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[6] = bindVals[0]
        self.padValues[6] = bindVals[1]

        self.specialPadBox.setText(bindVals[0])
        self.specialPadIntensityBox.setText(bindVals[1])

    def enterPadBind(self):
        bindVals = self.joyBinder.bindKey()
        self.padBindings[7] = bindVals[0]
        self.padValues[7] = bindVals[1]

        self.enterPadBox.setText(bindVals[0])
        self.enterPadIntensityBox.setText(bindVals[1])
        
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def loadSettings(self):
        # order of inputs: up, down, left, right, strafe, pet, special, enter
        filename = "gameBindings.json"
        try:
            data = open(filename)
            data_dump = json.load(data)
            self.gameBindings = [data_dump['up'],data_dump['down'],data_dump['left'],data_dump['right'],data_dump['strafe'],"p",data_dump['special'],"enter"]

            self.upGameBox.setText(self.gameBindings[0])
            self.downGameBox.setText(self.gameBindings[1])
            self.leftGameBox.setText(self.gameBindings[2])
            self.rightGameBox.setText(self.gameBindings[3])
            self.strafeGameBox.setText(self.gameBindings[4])
            self.specialGameBox.setText(self.gameBindings[6])
        except:
            print("Failed to load game data")
        
        filename = "padBindings.json"
        try:
            data = open(filename)
            data_dump = json.load(data)
            self.padBindings = [data_dump['up'],data_dump['down'],data_dump['left'],data_dump['right'],data_dump['strafe'],data_dump['pet'],data_dump['special'],data_dump['enter']]
            self.padValues = [data_dump['upIntensity'],data_dump['downIntensity'],data_dump['leftIntensity'],data_dump['rightIntensity'],data_dump['strafeIntensity'],data_dump['petIntensity'],data_dump['specialIntensity'],data_dump['enterIntensity']]

            self.upPadBox.setText(self.padBindings[0])
            self.downPadBox.setText(self.padBindings[1])
            self.leftPadBox.setText(self.padBindings[2])
            self.rightPadBox.setText(self.padBindings[3])
            self.strafePadBox.setText(self.padBindings[4])
            self.petPadBox.setText(self.padBindings[5])
            self.specialPadBox.setText(self.padBindings[6])
            self.enterPadBox.setText(self.padBindings[7])

            self.upPadIntensityBox.setText(str(self.padValues[0]))
            self.downPadIntensityBox.setText(str(self.padValues[1]))
            self.leftPadIntensityBox.setText(str(self.padValues[2]))
            self.rightPadIntensityBox.setText(str(self.padValues[3]))
            self.strafePadIntensityBox.setText(str(self.padValues[4]))
            self.petPadIntensityBox.setText(str(self.padValues[5]))
            self.specialPadIntensityBox.setText(str(self.padValues[6]))
            self.enterPadIntensityBox.setText(str(self.padValues[7]))
        except:
            print("Failed to load pad data")

    def saveSettings(self):
        filename = "gameBindings.json"
        gameData = {}
        gameData['up'] = self.upGameBox.text()
        gameData['down'] = self.downGameBox.text()
        gameData['left'] = self.leftGameBox.text()
        gameData['right'] = self.rightGameBox.text()
        gameData['strafe'] = self.strafeGameBox.text()
        gameData['special'] = self.specialGameBox.text()
        with open(filename, "w") as outfile:
            json_game_data = json.dump(gameData,outfile)
        
        filename = "padBindings.json"
        padData = {}
        padData['up'] = self.upPadBox.text()
        padData['down'] = self.downPadBox.text()
        padData['left'] = self.leftPadBox.text()
        padData['right'] = self.rightPadBox.text()
        padData['strafe'] = self.strafePadBox.text()
        padData['pet'] = self.petPadBox.text()
        padData['special'] = self.specialPadBox.text()
        padData['enter'] = self.specialPadBox.text()
        padData['upIntensity'] = self.upPadIntensityBox.text()
        padData['downIntensity'] = self.downPadIntensityBox.text()
        padData['leftIntensity'] = self.leftPadIntensityBox.text()
        padData['rightIntensity'] = self.rightPadIntensityBox.text()
        padData['strafeIntensity'] = self.strafePadIntensityBox.text()
        padData['petIntensity'] = self.petPadIntensityBox.text()
        padData['specialIntensity'] = self.specialPadIntensityBox.text()
        padData['enterIntensity'] = self.enterPadIntensityBox.text()
        with open(filename, "w") as outfile:
            json_pad_data = json.dump(padData,outfile)

    def togglePadControl(self):
        try:
            get_gamepad()
        except:
            self.updateStatus.appendPlainText("No pad attached.")
            self.freeControlButton.setChecked(False)
            return -1

        if (self.freeControlButton.isChecked()):
            self.joy = XboxController(self.padBindings)
            self.padThread = QThread()
            self.padTracker = padWorker(self.freeControlButton, self.joy, self.gameBindings, self.padValues)
            self.padTracker.moveToThread(self.padThread)
            self.padThread.started.connect(self.padTracker.run)
            self.padTracker.disconnect.connect(self.padDisconnect)
            self.padTracker.disconnect.connect(self.padThread.quit)
            self.padTracker.disconnect.connect(self.padTracker.deleteLater)
            self.padThread.finished.connect(self.padThread.deleteLater)
            try:
                self.joy.startThread()
                self.padThread.start()
                # update sliders on voltage change as well
                self.freeControlButton.setStyleSheet("background-color : lightblue")
                self.padControlToggle = 1
            except:
                self.updateStatus.appendPlainText("No controller attached.")
                self.freeControlButton.setStyleSheet("background-color : lightgrey")
                self.padControlToggle = 0
                self.freeControlButton.setChecked(False)
        else:
            self.padDisconnect()
        
        return -1
    
    def padDisconnect(self):
        self.joy.endThread()
        self.freeControlButton.setStyleSheet("background-color : lightgrey")
        self.padControlToggle = 0
        self.padControlToggle = 0
        self.freeControlButton.setChecked(False)

class padWorker(QThread):
    disconnect = pyqtSignal()
    gamepadCheck = 0
    joyInputs = []

    def __init__(self, toggleButton, joy, keyInputs, keyValExpects):
        super().__init__()
        self.toggleButton = toggleButton
        self.joy = joy
        self.keyInputs = keyInputs
        self.keyValExpects = keyValExpects

        self.leftDown = 0
        self.rightDown = 0
        self.upDown = 0
        self.downDown = 0
        self.strafeDown = 0
        self.petDown = 0
    
    def run(self):
        try:
            get_gamepad()
            self.gamepadCheck = 1
        except:
            self.gamepadCheck = 0

        while (self.toggleButton.isChecked() and self.gamepadCheck == 1):

            try:
                get_gamepad()
                self.gamepadCheck = 1
            except:
                self.gamepadCheck = 0
            
            if (self.gamepadCheck == 1):
                self.joyInputs = self.joy.read()
            else:
                self.joyInputs = [0,0,0,0,0]

            if (self.upDown == 1 and self.inputs[0] < 0.25*abs(self.keyValExpects[0])):
                pyautogui.keyUp(self.keyInputs[0])
                self.upDown = 0
            else:    
                if (self.keyValExpects[0] > 0):   
                    if (self.inputs[0] > 0.25*self.keyValExpects[0] and self.upDown == 0):
                        if (self.downDown == 1):    
                            pyautogui.keyUp(self.keyInputs[1])
                            self.downDown = 0
                        pyautogui.keyDown(self.keyInputs[0])
                        self.upDown = 1
                elif (self.keyValExpects[0] < 0):
                    if (self.inputs[0] < 0.25*self.keyValExpects[0] and self.upDown == 0):
                        if (self.downDown == 1):    
                            pyautogui.keyUp(self.keyInputs[1])
                            self.downDown = 0
                        pyautogui.keyDown(self.keyInputs[0])
                        self.upDown = 1

            if (self.downDown == 1 and self.inputs[1] < 0.25*abs(self.keyValExpects[1])):
                pyautogui.keyUp(self.keyInputs[1])
                self.downDown = 0
            else:
                if (self.keyValExpects[1] > 0):   
                    if (self.inputs[1] > 0.25*self.keyValExpects[1] and self.downDown == 0):
                        if (self.upDown == 1):    
                            pyautogui.keyUp(self.keyInputs[0])
                            self.upDown = 0
                        pyautogui.keyDown(self.keyInputs[1])
                        self.downDown = 1
                elif (self.keyValExpects[1] < 0):
                    if (self.inputs[1] < 0.25*self.keyValExpects[1] and self.downDown == 0):
                        if (self.upDown == 1):    
                            pyautogui.keyUp(self.keyInputs[0])
                            self.upDown = 0
                        pyautogui.keyDown(self.keyInputs[1])
                        self.downDown = 1

            if (self.leftDown == 1 and self.inputs[2] < 0.25*abs(self.keyValExpects[2])):
                pyautogui.keyUp(self.keyInputs[2])
                self.leftDown = 0
            else:
                if (self.keyValExpects[2] > 0):
                    if (self.inputs[2] > 0.25*self.keyValExpects[2] and self.leftDown == 0):
                        if (self.rightDown == 1):    
                            pyautogui.keyUp(self.keyInputs[3])
                            self.rightDown = 0
                        pyautogui.keyDown(self.keyInputs[2])
                        self.leftDown = 1
                elif (self.keyValExpects[2] > 0):
                    if (self.inputs[0] < 0.25*self.keyValExpects[2] and self.leftDown == 0):
                        if (self.rightDown == 1):    
                            pyautogui.keyUp(self.keyInputs[3])
                            self.rightDown = 0
                        pyautogui.keyDown(self.keyInputs[2])
                        self.leftDown = 1

            if (self.rightDown == 1 and self.inputs[3] < 0.25*abs(self.keyValExpects[3])):
                pyautogui.keyUp(self.keyInputs[3])
                self.rightDown = 0
            else:
                if (self.keyValExpects[3] > 0):
                    if (self.inputs[3] > 0.25*self.keyValExpects[3] and self.rightDown == 0):
                        if (self.leftDown == 1):    
                            pyautogui.keyUp(self.keyInputs[2])
                            self.leftDown = 0
                        pyautogui.keyDown(self.keyInputs[3])
                        self.rightDown = 1
                elif (self.keyValExpects[3] < 0):
                    if (self.inputs[3] < 0.25*self.keyValExpects[3] and self.rightDown == 0):
                        if (self.leftDown == 1):    
                            pyautogui.keyUp(self.keyInputs[2])
                            self.leftDown = 0
                        pyautogui.keyDown(self.keyInputs[3])
                        self.rightDown = 1
            
            if (self.strafeDown == 1 and self.inputs[2] < 0.25*abs(self.keyValExpects[4])):
                pyautogui.keyUp(self.keyInputs[4])
                self.strafeDown = 0
            else:
                if (self.keyValExpects[4] > 0):
                    if (self.inputs[4] > 0.25*self.keyValExpects[4] and self.strafeDown == 0):
                        pyautogui.keyDown(self.keyInputs[4])
                        self.strafeDown = 1
                elif (self.keyValExpects[4] < 0):
                    if (self.inputs[4] < 0.25*self.keyValExpects[4] and self.strafeDown == 0):
                        pyautogui.keyDown(self.keyInputs[4])
                        self.strafeDown = 1

            if (self.petDown == 1 and self.inputs[4] < 0.25*abs(self.keyValExpects[5])):
                pyautogui.keyUp(self.keyValExpects[5])
                self.petDown = 0
            else:
                if (self.keyValExpects[5] > 0):
                    if (self.inputs[5] > 0.25 and self.petDown == 0):
                        pyautogui.keyDown(self.keyInputs[5])
                        self.petDown = 1
                elif (self.keyValExpects[5] < 0):
                    if (self.inputs[5] < 0.25 and self.petDown == 0):
                        pyautogui.keyDown(self.keyInputs[5])
                        self.petDown = 1
        
            if (inputs[6] == self.keyValExpects[6]):
                pyautogui.press(self.keyInputs[6])
            
            if (inputs[7] == self.keyValExpects[7]):
                pyautogui.press(self.keyInputs[7])
            
            time.sleep(0.008)
            # order of inputs: up, down, left, right, strafe, pet, special, enter
            # how to kill controller thread at end?
        self.disconnect.emit()

def main(argv):
    app = QApplication([])
    gallery = WidgetGallery()
    gallery.show()
    app.exec()
            
if __name__ == '__main__':
    main(sys.argv)