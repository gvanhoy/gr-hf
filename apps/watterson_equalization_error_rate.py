from hf.cma_watterson_experiment import cma_watterson_experiment
from hf.watterson_tap import watterson_tap
from matplotlib import pyplot as plt
import numpy as np


class WattersonEqualization:
    def __init__(self):
        self.simulation()

    def simulation(self):
        tap_block = watterson_tap()
        tap_block.run()
        tap1 = tap_block.get_tap()
        tap_block.stop()

        tap_block = watterson_tap() # different parameters
        tap_block.run()
        tap2 = tap_block.get_tap()
        tap_block.stop()

        top_block = cma_watterson_experiment(10, 1024, (tap1, tap2))
        top_block.run()
        top_block.wait()
        symbols = top_block.blocks_vector_sink_x_0.data()
        top_block.stop()

        plt.plot(np.real(symbols), np.imag(symbols))
        plt.show()

        ## calculate the error rate
        top_block.const.points()


if __name__ == '__main__':
    WattersonEqualization()

