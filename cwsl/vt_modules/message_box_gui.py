"""

This module tests the GUI

Part of the Model Analysis Service VisTrails plugin.

"""

from vistrails.core.modules.vistrails_module import Module
from vistrails.core.modules.basic_modules import List, String

#from Example import app_main as dsMain
from MessageBox import app_main as dsMain

import logging
logger = logging.getLogger(__name__)

class Message_Box_GUI(Module):
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
        logger.debug('ds = %s' % ds)
        #ds.exec_()				# wait for user selections (but ds has no "exec_" method)
        logger.debug('get result ...')
        in_string = ds.getResult()
        logger.debug('in_string = "%s"' % in_string)

        #self.setResult('result', output_cons)		# List
        self.setResult('result', in_string)		# String
