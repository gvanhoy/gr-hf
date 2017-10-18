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
import numpy as np


def gen_taps(delay_spread, doppler_spread, num_taps):
    if num_taps % 2 == 0:
        print "Warning, number of taps is not odd."

    taps = []
    for tap_index in range(-num_taps/2, num_taps/2 + 1, 1):
        arg = np.pi * doppler_spread * tap_index*2*delay_spread
        taps.append(np.exp(-arg*arg))

    energy = taps[len(taps)/2]
    for x in range(len(taps)):
        if x != len(taps)/2:
            energy += 2*taps[x]

    return map(lambda x: x/energy, taps)
