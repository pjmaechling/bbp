#!/usr/bin/env python
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
import os
import sys
import unittest

# Import Broadband modules
import cmp_bbp
import rotd100
import seqnum
import bband_utils
import install_cfg

class TestRotD100(unittest.TestCase):
    """
    Unit test for the rotd100.py module
    """

    def setUp(self):
        """
        Sets up the environment for the test
        """
        self.install = install_cfg.InstallCfg.getInstance()
        self.sim_id = int(seqnum.get_seq_num())

        # Make sure all directories exist
        self.indir = os.path.join(self.install.A_IN_DATA_DIR,
                                  str(self.sim_id))
        self.tmpdir = os.path.join(self.install.A_TMP_DATA_DIR,
                                   str(self.sim_id))
        self.outdir = os.path.join(self.install.A_OUT_DATA_DIR,
                                   str(self.sim_id))
        self.logdir = os.path.join(self.install.A_OUT_LOG_DIR,
                                   str(self.sim_id))
        bband_utils.mkdirs([self.indir, self.tmpdir, self.outdir, self.logdir],
                           print_cmd=False)

    def test_rotd100(self):
        """
        Test the rotd100 module
        """
        # Load configuration, set sim_id
        sim_id = self.sim_id
        # Reference directory
        ref_dir = os.path.join(self.install.A_TEST_REF_DIR, "ucb")

        r_station_list = "rotd50.stl"
        a_src_station_list = os.path.join(ref_dir, r_station_list)
        a_dst_station_list = os.path.join(self.indir, r_station_list)

        # Copy station list to indir
        cmd = "cp %s %s" % (a_src_station_list, a_dst_station_list)
        bband_utils.runprog(cmd)

        # Copy velocity bbp files to outdir
        for i in range(1, 6):
            src_bbp = os.path.join(ref_dir, "8000%d.vel.bbp" % (i))
            dst_bbp = os.path.join(self.outdir, "%d.8000%d.vel.bbp" %
                                   (sim_id, i))
            cmd = "cp %s %s" % (src_bbp, dst_bbp)
            bband_utils.runprog(cmd)

        rotd100_obj = rotd100.RotD100(r_station_list, sim_id=sim_id)
        rotd100_obj.run()

        # Check results
        for i in range(1, 6):
            ref_rd100 = os.path.join(ref_dir, "8000%d.rd100" % (i))
            ref_rd100_v = os.path.join(ref_dir, "8000%d.rd100.vertical" % (i))
            new_rd100 = os.path.join(self.outdir, "%d.8000%d.rd100" %
                                     (sim_id, i))
            new_rd100_v = os.path.join(self.outdir, "%d.8000%d.rd100.vertical" %
                                       (sim_id, i))
            self.assertFalse(cmp_bbp.cmp_files_generic(ref_rd100,
                                                       new_rd100) != 0,
                             "Output file %s does not match reference file: %s" %
                             (new_rd100, ref_rd100))
            self.assertFalse(cmp_bbp.cmp_files_generic(ref_rd100_v,
                                                       new_rd100_v) != 0,
                             "Output file %s does not match reference file: %s" %
                             (new_rd100_v, ref_rd100_v))

if __name__ == "__main__":
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestRotD100)
    RETURN_CODE = unittest.TextTestRunner(verbosity=2).run(SUITE)
    sys.exit(not RETURN_CODE.wasSuccessful())
