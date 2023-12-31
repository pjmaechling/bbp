#! /usr/bin/env python
"""
BSD 3-Clause License

Copyright (c) 2021, University of Southern California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import division, print_function

# Import Python modules
import sys
import unittest

# Import Broadband modules
from test_bbtoolbox import TestBBToolbox
from test_wcc_siteamp import TestWccSiteamp
from test_rotd50 import TestRotD50
from test_gp_gof import TestGPGof
from test_sdsu_mogof import TestSDSUMOGof

class SDSUTestSuite(unittest.TestSuite):
    """
    Tests for the SDSU method
    """
    def __init__(self):
        """
        Adds individual tests to the suite
        """
        unittest.TestSuite.__init__(self)
        self.addTest(unittest.makeSuite(TestBBToolbox))
        self.addTest(unittest.makeSuite(TestWccSiteamp))
        self.addTest(unittest.makeSuite(TestRotD50))
        self.addTest(unittest.makeSuite(TestGPGof))
        self.addTest(unittest.makeSuite(TestSDSUMOGof))

if __name__ == '__main__':
    STS = SDSUTestSuite()
    RETURN_CODE = unittest.TextTestRunner(verbosity=2).run(STS)
    sys.exit(not RETURN_CODE.wasSuccessful())
