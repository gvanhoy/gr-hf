#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: LMS Watterson Experiment
# Author: Garrett Vanhoy, Noel Teku
# Generated: Sun Oct 22 02:39:38 2017
##################################################

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


class lms_watterson_experiment(gr.top_block):

    def __init__(self, snr_db=10, taps=[]):
        gr.top_block.__init__(self, "LMS Watterson Experiment")

        ##################################################
        # Variables
        ##################################################
        self.snr_db = snr_db
        self.samp_rate = samp_rate = 1000000
        self.num_symbols = num_symbols = 4096
        self.taps = taps

        self.const = const = digital.constellation_8psk().base()


        ##################################################
        # Blocks
        ##################################################
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccc(2, (firdes.low_pass_2(1, 1, .25, .1, 80)))
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(2, 1, 2, const)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=0,
        	frequency_offset=0.0,
        	epsilon=1.0,
        	taps=self.taps,
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, num_symbols)
        self.analog_random_source_x_1 = blocks.vector_source_b(map(int, numpy.random.randint(0, const.arity(), 1000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_1, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.blocks_head_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.channels_channel_model_0, 0))

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
