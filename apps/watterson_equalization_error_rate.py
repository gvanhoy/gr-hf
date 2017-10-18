from hf.cma_watterson_experiment import cma_watterson_experiment
from hf.watterson_tap import watterson_tap
from matplotlib import pyplot as plt
import numpy as np


class WattersonEqualization:
    def __init__(self):
        self.simulation()

    def create_tap(self):
        tap_block = watterson_tap()
        print "run tap block"
        tap_block.start()
        tap = tap_block.get_tap()
        tap_block.stop()
        return tap

    def error_check(self):
        epsilon = 0.01+0.01*1j
        error_count = 0
        error = []
        for symbol in self.symbols:
            point = symbol - np.asarray(self.const_points)
            min_dist = np.min(point)
            error.append(min_dist)
            # if min_dist > epsilon:
            #     error_count = error_count + 1
        np.mean(np.square(min_dist))

    def simulation(self):
        tap1 = self.create_tap()
        tap2 = self.create_tap()


        top_block = cma_watterson_experiment(10, 4096, (tap1, tap2))
        top_block.start()
        top_block.wait()
        self.symbols = top_block.blocks_vector_sink_x_0.data()
        top_block.stop()

        plt.scatter(np.real(self.symbols)[3000:-1], np.imag(self.symbols)[3000:-1])
        plt.show()

        ## calculate the error rate
        self.const_points = top_block.const.points()
        self.error_check()



if __name__ == '__main__':
    WattersonEqualization()

