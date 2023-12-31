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

These are acceptance tests for the SONG RMG module
"""
from __future__ import division, print_function

# Import Python modules
import os
import sys
import unittest

# Import Broadband modules
import seqnum
import bband_utils
import cmp_bbp
from install_cfg import InstallCfg
from song_rmg_single_seg import SongRMGSS

class TestRMG(unittest.TestCase):
    """
    Unit Test for rmg.py
    """

    def setUp(self):
        self.install = InstallCfg()
        os.chdir(self.install.A_COMP_DIR)
        self.sim_id = int(seqnum.get_seq_num())
        self.srcfile = "test_whittier_song.src"
        self.outsrf = "%d_test_eq.srf" % self.sim_id

        indir = os.path.join(self.install.A_IN_DATA_DIR, str(self.sim_id))
        tmpdir = os.path.join(self.install.A_TMP_DATA_DIR, str(self.sim_id))
        outdir = os.path.join(self.install.A_OUT_DATA_DIR, str(self.sim_id))
        logdir = os.path.join(self.install.A_OUT_LOG_DIR, str(self.sim_id))
        # Create all directories
        bband_utils.mkdirs([indir, tmpdir, outdir, logdir],
                           print_cmd=False)

        cmd = "cp %s %s" % (os.path.join(self.install.A_TEST_REF_DIR,
                                         "song",
                                         self.srcfile),
                            os.path.join(self.install.A_IN_DATA_DIR,
                                         str(self.sim_id)))
        bband_utils.runprog(cmd)

    def tearDown(self):
        os.chdir(self.install.A_TEST_DIR)

    def test_rmg(self):
        a_ref_dir = os.path.join(self.install.A_TEST_REF_DIR, "song")
        a_res_dir = os.path.join(self.install.A_TMP_DATA_DIR, str(self.sim_id))

        rmg = SongRMGSS(None, self.srcfile, self.outsrf, None, sim_id=self.sim_id)
        rmg.run()
        #
        # Test conversion from RMG to srf file
        #

        a_ref_file = os.path.join(a_ref_dir, "song_test_whittier.srf")
        a_newfile = os.path.join(a_res_dir, self.outsrf)
        errmsg = ("Output file %s does not match reference file %s" %
                  (a_newfile, a_ref_file))
        self.assertFalse(not cmp_bbp.cmp_srf(a_ref_file, a_newfile,
                                             tolerance=0.0011) == 0, errmsg)

if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRMG)
    RETURN_CODE = unittest.TextTestRunner(verbosity=2).run(SUITE)
    sys.exit(not RETURN_CODE.wasSuccessful())
