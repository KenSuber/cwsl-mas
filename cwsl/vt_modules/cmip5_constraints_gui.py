"""

Authors: Tim Bedin, Tim Erwin

Copyright 2014 CSIRO

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


This module creates constraints to restrict the CMIP5 dataset with:
    Path structure: <path>/<mip>/<product>/<institute>/<model>/<experiment>/<frequency>/<realm>/<variable>/<ensemble>/<filename>
      where:
          <path>: Configured via menu: Packages->CWSL->Configure: authorative_path 
          <filename>:  <variable>_<mip_table>_<model>_<experiment>_<ensemble>_<time_span>

Part of the Model Analysis Service VisTrails plugin.

"""

from vistrails.core.modules.vistrails_module import Module
from vistrails.core.modules.basic_modules import List, String

from cwsl.core.constraint import Constraint
from DataSelection5 import app_main as dsMain

import logging
logger = logging.getLogger(__name__)

class CMIP5Constraints_GUI(Module):
    """ Outputs a set restrictions to feed into the CMIP5 VisTrails module.

    Select the values that you want to restrict the DataSet to; you can select multiple
    values. If you do not want to restrict the values of a parameter, use the "All" button.

    Path structure: <path>/<mip>/<product>/<institute>/<model>/<experiment>/<frequency>/<realm>/<variable>/<ensemble>/<filename>
      where:
          <path>: Configured via menu: Packages->CWSL->Configure: authorative_path 
          <filename>:  <variable>_<mip_table>_<model>_<experiment>_<ensemble>_<time_span>

    """

    # Define ports.
    #_input_ports = []		# ?
    _output_ports = [('constraint_set', List)]
    logger.debug('_output_ports = %s' % _output_ports)

    def compute(self):
        logger.debug('compute() ...')

        #in_string = self.getInputFromPort('constraint_string')
        # ds = dsMain(verbose=True)		# launch the GUI; wait for user selections
        ds = dsMain(verbose=False)		# launch the GUI; wait for user selections

        # We want to wait here until the user clicks the "Done" button; how do we do that?

        logger.debug('ds = %s' % ds)
        in_string = ds.getConstraintString()
        logger.debug('in_string = %s' % in_string)

        output_cons = []

        if len(in_string) > 0:
            split_strings = in_string.split(';')
            logger.debug('split_strings = %s' % split_strings)

            for cons_string in split_strings:
                logger.debug('cons_string = %s' % cons_string)
                constraint_list = cons_string.split('=')
                logger.debug('constraint_list = %s' % constraint_list)

                key = constraint_list[0].strip()
                logger.debug('key = %s' % key)
                raw_values = [val for val in constraint_list[1].split(',')]
                final_values = [val_string.strip() for val_string in raw_values]
                output_cons.append(Constraint(key, final_values))

        logger.debug('output_cons = %s' % output_cons)
        self.setResult('constraint_set', output_cons)
