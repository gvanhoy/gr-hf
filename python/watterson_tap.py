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
from gnuradio import filter
from gnuradio import gr
from hf.gen_watterson_taps import gen_taps


class watterson_tap(gr.top_block):
    def __init__(self,
                 doppler_spread_hz=.001,
                 delay_spread_s=2,
                 num_taps=100):
        gr.top_block.__init__(self, "Watterson Tap Generation")

        ##################################################
        # Variables
        ##################################################
        self.num_taps = num_taps
        self.doppler_spread_hz = doppler_spread_hz
        self.delay_spread_s = delay_spread_s
        self.taps = taps = gen_taps(doppler_spread_hz, delay_spread_s, num_taps)
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.block_0 = blocks.probe_signal_c()
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.block_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))

    def get_num_taps(self):
        return self.num_taps

    def set_num_taps(self, num_taps):
        self.num_taps = num_taps
        self.set_taps(gen_taps(self.doppler_spread_hz, self.delay_spread_s, self.num_taps))

    def get_doppler_spread_hz(self):
        return self.doppler_spread_hz

    def set_doppler_spread_hz(self, doppler_spread_hz):
        self.doppler_spread_hz = doppler_spread_hz
        self.set_taps(gen_taps(self.doppler_spread_hz, self.delay_spread_s, self.num_taps))

    def get_delay_spread_s(self):
        return self.delay_spread_s

    def set_delay_spread_s(self, delay_spread_s):
        self.delay_spread_s = delay_spread_s
        self.set_taps(gen_taps(self.doppler_spread_hz, self.delay_spread_s, self.num_taps))

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.interp_fir_filter_xxx_0.set_taps((self.taps))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_tap(self):
        return self.block_0.level()
