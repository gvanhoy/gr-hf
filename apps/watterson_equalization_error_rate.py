from hf.cma_watterson_experiment import cma_watterson_experiment
from hf.watterson_tap import watterson_tap

class WattersonEqualization:
    def __init__(self):
        pass

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

        pass



