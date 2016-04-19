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


This module creates constraints from a constraint string

Part of the Model Analysis Service VisTrails plugin.

"""

from vistrails.core.modules.vistrails_module import Module
from vistrails.core.modules.basic_modules import List, String

from cwsl.core.constraint import Constraint

import logging
logger = logging.getLogger(__name__)

class ConstraintsConversion(Module):
    """ Outputs a set restrictions to feed into the CMIP5 VisTrails module.

    Enter the values that you want to restrict the DataSet to, with multiple
    values separated by a comma. If you do not want to restrict the values, leave
    the value blank.

    Path structure: <path>/<mip>/<product>/<institute>/<model>/<experiment>/<frequency>/<realm>/<variable>/<ensemble>/<filename>
      where:
          <path>: Configured via menu: Packages->CWSL->Configure: authorative_path 
          <filename>:  <variable>_<mip_table>_<model>_<experiment>_<ensemble>_<time_span>

    """

    # Define ports.
    _input_ports = [('in_string', String, {"defaults": str([''])})]
    _output_ports = [('constraint_set', List)]

    def compute(self):
        logger.debug('constraints_conversion.compute() starting ...')
        
        output_cons = []
        
        in_string = self.getInputFromPort('in_string').replace('\n', '')
        if len(in_string) > 0:
            split_strings = in_string.split(';')
            logger.debug('split_strings = %s' % split_strings)

            for cons_string in split_strings:
                logger.debug('cons_string = "%s"' % cons_string)
                constraint_list = cons_string.split('=')
                logger.debug('constraint_list = %s' % constraint_list)

                key = constraint_list[0].strip()
                logger.debug('key = "%s"' % key)
                raw_values = [val for val in constraint_list[1].split(',')]
                final_values = [val_string.strip() for val_string in raw_values]
                output_cons.append(Constraint(key, final_values))

        self.setResult('constraint_set', output_cons)
