"""

This module tests the GUI

Part of the Model Analysis Service VisTrails plugin.

"""

from vistrails.core.modules.vistrails_module import Module
from vistrails.core.modules.basic_modules import List, String

from PyQt4 import QtCore, QtGui
from Example import app_main as dsMain

import time
import logging
logger = logging.getLogger(__name__)

class Example_GUI(Module):
    """ Test

    """

    # Define ports.
    #_input_ports = []		# ?
    # _output_ports = [('result', List)]
    _output_ports = [('result', String)]
    logger.debug('_output_ports = %s' % _output_ports)

    def compute(self):
        logger.debug('compute() ...')

        # ds has a QLineEdit and a QPushButton
        ds = dsMain(verbose=True)		# launch the GUI; wait for user selections
        # ds = dsMain(verbose=False)		# launch the GUI; wait for user selections
        #ds.show()			# needed?
        logger.debug('ds = %s' % ds)
        #ds.exec_()				# wait for user selections (but ds has no "exec_" method)
        app = QtGui.QApplication.instance()
        logger.debug('app = %s' % app)
        logger.debug('app.processEvents = %s' % app.processEvents)
        while not ds.doneButton.isChecked():
            time.sleep(1)
            app.processEvents()
        logger.debug('ds.doneButton.isChecked() = %s' % ds.doneButton.isChecked())
        logger.debug('get result ...')
        in_string = ds.getResult()
        logger.debug('in_string = "%s"' % in_string)

        #self.setResult('result', output_cons)		# List
        self.setResult('result', in_string)		# String
