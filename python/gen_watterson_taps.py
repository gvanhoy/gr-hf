import numpy as np


def gaussian_tap(delay_spread, doppler_spread, num_taps):
    if num_taps % 2 != 0:
        print "Warning, number of taps is not even."

    taps = np.ndarray((num_taps,), dtype=np.float32)
    for tap_index in range(-num_taps/2, num_taps/2, 1):
        arg = np.pi * doppler_spread * tap_index*2*delay_spread
        taps[tap_index + num_taps/2] = np.exp(-arg*arg)

    print '['
    for tap in taps:
        print str(tap) + ','
    print ']'


if __name__ == '__main__':
    gaussian_tap(.001, 2, 100)