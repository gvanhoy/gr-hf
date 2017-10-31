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
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import numpy


class cma_watterson_experiment(gr.top_block):
    def __init__(self,
                 snr_db=10,
                 num_symbols=1024,
                 taps=[]):
        gr.top_block.__init__(self, "CMA Watterson Experiment")

        ##################################################
        # Variables
        ##################################################
        self.snr_db = snr_db
        self.samp_rate = samp_rate = 1000000
        self.num_symbols = num_symbols
        self.taps = taps

        self.const = const = digital.constellation_8psk().base()


        ##################################################
        # Blocks
        ##################################################
        #self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccc(2, (firdes.low_pass_2(1, 1, .25, .1, 80)))
        #self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(4, 1, .01, 2)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_symbols)
        self.analog_random_source_x_1 = blocks.vector_source_b(map(int, numpy.random.randint(0, const.arity(), 1000)), True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex * 1, 2)
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_ccc(1, (
        self.taps[0]/ numpy.sqrt((numpy.abs(self.taps[0]) ** 2 + numpy.abs(self.taps[1]) ** 2)),
        self.taps[1]/ numpy.sqrt((numpy.abs(self.taps[0]) ** 2 + numpy.abs(self.taps[1]) ** 2))))
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, .1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_1, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_vector_sink_x_0, 0))

        #self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.blocks_head_0, 0))
        #self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.blocks_repeat_0, 0))




        self.connect((self.interp_fir_filter_xxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0, 2))

    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.channels_channel_model_0.set_noise_voltage(10**(-self.snr_db/20.0)/numpy.sqrt(2))

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
