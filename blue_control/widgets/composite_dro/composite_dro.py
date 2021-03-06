
import os
from qtpy import uic
from qtpy.QtCore import Slot, Property
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import QWidget, QVBoxLayout, QFrame

from qtpyvcp.plugins import getPlugin

BASE_PATH = os.path.join(os.path.dirname(__file__))
UI_FILE = os.path.join(os.path.dirname(__file__), "composite_dro.ui")

ICON_PATH = os.path.join(BASE_PATH, 'icons')

STATUS = getPlugin('status')


class CompositeDroWidget(QWidget):
    def __init__(self, parent=None, axis_number=None):
        super(CompositeDroWidget, self).__init__(parent)

        STATUS.homed.notify(self.updateHomedStatus)

        uic.loadUi(UI_FILE, self)

        self._anum = 0
        self._aletter = 'x'

        if axis_number is not None:
            self.axisNumber = axis_number

    @Property(int)
    def axisNumber(self):
        return self._anum

    @axisNumber.setter
    def axisNumber(self, axis):
        self._anum = max(0, min(axis, 8))
        self._aletter = 'xyzabcuvw'[self._anum]

        self.updateAxis()

    def updateAxis(self):
        self.dro_entry.axisNumber = self._anum
        self.abs_dro.axisNumber = self._anum
        self.dtg_dro.axisNumber = self._anum

        self.load_inidcator.pinBaseName = 'combidro.{}.load-indicator'.format(self._aletter)

        icon_name = 'axis-%s.png' % self._aletter
        icon = QIcon(os.path.join(ICON_PATH, icon_name))
        self.axis_actions_button.setIcon(icon)

    def updateHomedStatus(self, homed):
        if homed[self._anum] == 1:
            self.homed_indicator.setPixmap(self.getPixmap('homed.png'))
        else:
            self.homed_indicator.setPixmap(self.getPixmap('unhomed.png'))

    def getIcon(self, name):
        # icon_name = 'axis-%(axis_letter).png' % {'axis_letter': self._anum}

        return QIcon(os.path.join(ICON_PATH, name))

    def getPixmap(self, name):
        return QPixmap(os.path.join(ICON_PATH, name))


class CompositeDroGroup(QWidget):
    def __init__(self, parent=None):
        super(CompositeDroGroup, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(0, 6, 0, 0)

        axes = STATUS.axis_mask.getValue(format='list') or [0, 1, 3]

        needs_sep = False
        for anum in axes:

            if needs_sep:
                line = QFrame(self)
                line.setFrameShape(QFrame.HLine)
                self.layout.addWidget(line)

            dro = CompositeDroWidget(self, anum)
            self.layout.addWidget(dro)

            needs_sep = True

        self.setLayout(self.layout)