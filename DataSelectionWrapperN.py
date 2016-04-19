#!/opt/cloudapps/python-vlab/ep1_2/2.7.5/bin/python
#
# #!/usr/bin/python
# doesn't work with python2.6.6; works with python2.7.5


"""

Wrapper for the "data selection" widget; prints out the "constraintString" result

"""

import sys
from cwsl.vt_modules.DataSelectionN import main as dsMain

def main():

    (constraintString, num_files) = dsMain()

    #print 'constraintString = "%s"' % constraintString
    print constraintString		# the output of this function; used by the CLTools wrapper as an "stdout" output port
    return num_files			# the result of this function

if __name__ == '__main__':
    num_files = main()
    sys.exit(num_files)			# automatically used by the CLTools wrapper, as the "return_code" output port

