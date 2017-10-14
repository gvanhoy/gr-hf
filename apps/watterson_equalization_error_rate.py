from hf.cma_watterson_experiment import cma_watterson_experiment
from hf.watterson_tap import watterson_tap
from matplotlib import pyplot as plt
import numpy as np


class WattersonEqualization:
    def __init__(self):
        self.simulation()

    def simulation(self):
        tap_block = watterson_tap()
        print "run tap block"
        tap_block.start()
        tap1 = tap_block.get_tap()
        tap_block.stop()

        print "run tap block"
        tap_block = watterson_tap()  # different parameters
        tap_block.start()
        tap2 = tap_block.get_tap()
        tap_block.stop()

        top_block = cma_watterson_experiment(10, 4096, (tap1, tap2))
        top_block.start()
        top_block.wait()
        symbols = top_block.blocks_vector_sink_x_0.data()
        top_block.stop()

        plt.scatter(np.real(symbols)[3000:-1], np.imag(symbols)[3000:-1])
        plt.show()

        ## calculate the error rate
        top_block.const.points()


if __name__ == '__main__':
    WattersonEqualization()

