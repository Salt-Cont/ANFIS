#!/usr/bin/env python
"""
Sample script that uses the anfis package created using
MATLAB Compiler SDK.

Refer to the MATLAB Compiler SDK documentation for more information.
"""

import anfis
# Import the matlab module only after you have imported 
# MATLAB Compiler SDK generated Python modules.
import matlab

try:
    my_anfis = anfis.initialize()
except Exception as e:
    print('Error initializing anfis package\\n:{}'.format(e))
    exit(1)

try:
    dataIn = matlab.double([1, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.1, 0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 1, 1, 1, 0.9, 0.8, 0.7, 0.6, 0, 0, 0, 0.9, 0.9, 0.9, 0, 0, 0, 0.8, 0.8, 0.8, 0, 0, 0, 0.7, 0.7, 0.7, 0, 0, 0, 0.6, 0.6, 0.6, 0, 0, 0, 0.5, 0.5, 0.5, 0, 1, 0, 0.2, 0.2, 0, 0, 0.2, 0.2, 0.1, 0, 0.1, 0.1, 0, 0, 0.1, 0.1, 0, 1, 1, 0, 0, 1, 0.9, 0.8, 0.7, 0.6, 0, 0.9, 0.9, 0, 0, 0.9, 0, 0.8, 0.8, 0, 0.8, 0, 0, 0.7, 0.7, 0, 0, 0.7, 0, 0.6, 0.6, 0, 0, 0.6, 0, 0.5, 0.5, 0, 0, 0.5, 0, 1, 0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0.1, 0.1, 0, 0.1, 0, 0.1, 0, 0.1, 1, 0, 1, 0, 1, 0, 0.9, 0.8, 0.7, 0.6, 0.9, 0, 0.9, 0, 0.9, 0, 0.8, 0, 0.8, 0.8, 0, 0, 0.7, 0, 0.7, 0, 0.7, 0, 0.6, 0, 0.6, 0, 0.6, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.9, 0.8, 0.7, 0.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], size=(57, 4))
    outOut = my_anfis.Anfis(dataIn)
    print(outOut, sep='\\n')
except Exception as e:
    print('Error occurred during program execution\\n:{}'.format(e))

my_anfis.terminate()