#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from hf.gen_watterson_taps import gen_taps
from optparse import OptionParser
import numpy
import threading
import time

class lms_watterson_experiment(gr.top_block):

    def __init__(self, snr_db=10, num_symbols = 4096, taps=[]):
        gr.top_block.__init__(self, "LMS Watterson Experiment")

        ##################################################
        # Variables
        ##################################################
        self.snr_db = snr_db
        self.samp_rate = samp_rate = 1000000
        self.num_symbols = num_symbols
        self.taps = taps

        self.const = const = digital.constellation_8psk().base()
        self.tap_1 =  .1
        self.tap_0 =  .1
        self.poll_rate = 1

        ##################################################
        # Blocks
        ##################################################
        self.block_1 = blocks.probe_signal_c()
        self.block_0 = blocks.probe_signal_c()

        def _tap_1_probe():
            while True:
                val = self.block_1.level()
                try:
                    self.set_tap_1(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (self.poll_rate))

        _tap_1_thread = threading.Thread(target=_tap_1_probe)
        _tap_1_thread.daemon = True
        _tap_1_thread.start()

        def _tap_0_probe():
            while True:
                val = self.block_0.level()
                try:
                    self.set_tap_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (self.poll_rate))

        _tap_0_thread = threading.Thread(target=_tap_0_probe)
        _tap_0_thread.daemon = True
        _tap_0_thread.start()



        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccc(2, (firdes.low_pass_2(1, 1, .25, .1, 80)))
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0_1 = filter.interp_fir_filter_ccc(1, self.taps)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, self.taps)
        self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(4, .01, 2, const)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=10**(-self.snr_db/20.0)/numpy.sqrt(2),
        	frequency_offset=0.0,
        	epsilon=1.0,
        	taps=(self.tap_0/numpy.sqrt((numpy.abs(self.tap_0)**2  + numpy.abs(self.tap_1)**2)), self.tap_1/numpy.sqrt((numpy.abs(self.tap_0)**2  + numpy.abs(self.tap_1)**2))),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_symbols)
        self.analog_random_source_x_1 = blocks.vector_source_b(map(int, numpy.random.randint(0, const.arity(), 1000)), True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex * 1, 2)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 133701)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 42)

        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex * 1, samp_rate, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex * 1, samp_rate, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_1, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
        #self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.blocks_head_0, 0))
        #self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.blocks_repeat_0, 0))

        self.connect((self.analog_noise_source_x_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.interp_fir_filter_xxx_0_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_1, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.block_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.block_1, 0))


    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.channels_channel_model_0.set_noise_voltage(10**(-self.snr_db/20)/numpy.sqrt(2))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_num_symbols(self):
        return self.num_symbols

    def set_num_symbols(self, num_symbols):
        self.num_symbols = num_symbols
        self.blocks_head_0.set_length(self.num_symbols)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def set_tap_1(self, tap_1):
        self.tap_1 = tap_1
        self.channels_channel_model_0.set_taps((self.tap_0 / numpy.sqrt(
            (numpy.abs(self.tap_0) ** 2 + numpy.abs(self.tap_1) ** 2)), self.tap_1 / numpy.sqrt(
            (numpy.abs(self.tap_0) ** 2 + numpy.abs(self.tap_1) ** 2))))

    def get_tap_0(self):
        return self.tap_0

    def set_tap_0(self, tap_0):
        self.tap_0 = tap_0
        self.channels_channel_model_0.set_taps((self.tap_0 / numpy.sqrt(
            (numpy.abs(self.tap_0) ** 2 + numpy.abs(self.tap_1) ** 2)), self.tap_1 / numpy.sqrt(
            (numpy.abs(self.tap_0) ** 2 + numpy.abs(self.tap_1) ** 2))))

def main(top_block_cls=lms_watterson_experiment, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
