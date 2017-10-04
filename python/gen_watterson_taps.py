import numpy as np
from matplotlib import pyplot as plt


def gaussian_tap(delay_spread, doppler_spread, num_taps):
    if mod(num_taps, 2) != 0:
        print "Warning, number of taps is not even."

    taps = np.ndarray((num_taps,), dtype=np.float32)
    for tap_index in range(-num_taps/2, num_taps/2, 1):
        #arg = np.pi*doppler_spread*tap_index/(samp_rate/2)
        arg = np.pi * doppler_spread * tap_index*2*delay_spread
        taps[tap_index + num_taps/2] = np.exp(-arg*arg)

    plt.plot(taps)
    plt.show()
    return taps


if __name__ == '__main__':
    gaussian_taps(1000, 1)
