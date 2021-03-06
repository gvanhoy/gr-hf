from hf.cma_watterson_experiment import cma_watterson_experiment
from hf.watterson_tap import watterson_tap
from hf.lms_watterson_experiment import lms_watterson_experiment
from hf.cma_nonlinear_experiment import cma_nonlinear_experiment
from hf.lms_nonlinear_experiment import lms_nonlinear_experiment
#from python import lms_watterson_experiment
from matplotlib import pyplot as plt
import numpy as np

SNR_RANGE = range(10, 60, 5)
#SAMPLES = range(50, 310, 10)

class WattersonEqualization:
    def __init__(self):
        self.simulation()

    def create_tap(self):
        #tap_block = watterson_tap(delay_spread_s=.001, doppler_spread_hz=0.5, num_taps=101)
        tap_block = watterson_tap(delay_spread_s=.002, doppler_spread_hz=1, num_taps=101)
        tap_block.start()
        tap = tap_block.get_tap()
        while np.abs(tap) < 0.001:
            tap = tap_block.get_tap()
        tap_block.stop()
        return tap

    def error_check(self):
        epsilon = 0.01+0.01*1j
        error_count = 0
        error = []
        for symbol in self.symbols:
            point = symbol - np.asarray(self.const_points)
            point = np.abs(point)
            min_dist = np.min(point)
            error.append(min_dist)
            #error.append(np.square(min_dist))
        #a = np.square(min_dist)
        #np.mean(np.square(min_dist))
        mse = np.abs(np.mean(error))
        return mse

    def simulation(self):
        mse_avg_list = []
        mse_avg_list_lms = []
        mse_avg_list_nonlinear = []
        mse_avg_list_nonlinear_lms = []
        num_trials = 5000
        #snr = 10
        for snr in SNR_RANGE:
        #for samp in SAMPLES:
            mse_avg = 0
            mse_avg_lms = 0
            mse_avg_nonlinear = 0
            mse_avg_nonlinear_lms = 0
            for i in range(num_trials):

                tap1 = self.create_tap()
                tap2 = self.create_tap()
                scale_factor = 1.0 / np.sqrt((tap1 * np.conj(tap1)) + (tap2 * np.conj(tap2)))
                tap1 = scale_factor * tap1
                tap2 = scale_factor * tap2


                top_block = cma_nonlinear_experiment(snr, 4096, (tap1, tap2))
                #top_block = cma_watterson_experiment(snr, 4096, (tap1, tap2))
                #top_block = cma_nonlinear_experiment(snr, samp, (tap1, tap2))
                #top_block = cma_watterson_experiment(snr, samp, (tap1, tap2))
                top_block.start()
                top_block.wait()
                self.symbols = top_block.blocks_vector_sink_x_0.data()
                top_block.stop()
                top_block.wait()



                #lms_block.start()
                #self.symbols_lms =

                #plt.figure(1)
                #plt.scatter(np.real(self.symbols)[0:100], np.imag(self.symbols)[0:100])

                #plt.figure(1)
                #plt.scatter(np.real(self.symbols)[3000:-1], np.imag(self.symbols)[3000:-1])
                #plt.show()

                #plt.title('Constellation Prior to Equalization - ' + str(snr_db) + ' dB')
                #plt.xlabel('In-Phase')
                #plt.ylabel('Quadrature')
                #plt.show()

                ## calculate the error rate
                self.const_points = top_block.const.points()

                mse = self.error_check()
                mse_avg = mse_avg + mse/num_trials



                top_block_nonlinear = cma_watterson_experiment(snr, 4096, (tap1, tap2))
                top_block_nonlinear.start()
                top_block_nonlinear.wait()
                self.symbols = top_block_nonlinear.blocks_vector_sink_x_0.data()
                top_block_nonlinear.stop()
                top_block_nonlinear.wait()
                mse_nonlinear = self.error_check()
                mse_avg_nonlinear = mse_avg_nonlinear + mse_nonlinear / num_trials

                #lms_block = lms_nonlinear_experiment(snr, 4096, (tap1, tap2))
                #lms_block = lms_watterson_experiment(snr, samp, (tap1, tap2))
                lms_block = lms_watterson_experiment(snr, 4096, (tap1, tap2))
                lms_block.start()
                lms_block.wait()
                self.symbols = lms_block.blocks_vector_sink_x_0.data()
                lms_block.stop()
                lms_block.wait()

                #plt.figure(1)
                #plt.scatter(np.real(self.symbols)[3000:-1], np.imag(self.symbols)[3000:-1])
                #plt.show()
                #print str(i)

                mse_lms = self.error_check()
                mse_avg_lms = mse_avg_lms + mse_lms/num_trials

                lms_block_nonlinear = lms_nonlinear_experiment(snr, 4096, (tap1, tap2))
                lms_block_nonlinear.start()
                lms_block_nonlinear.wait()
                self.symbols = lms_block_nonlinear.blocks_vector_sink_x_0.data()
                lms_block_nonlinear.stop()
                lms_block_nonlinear.wait()
                mse_lms_nonlinear = self.error_check()
                mse_avg_nonlinear_lms = mse_avg_nonlinear_lms + mse_lms_nonlinear/num_trials

            mse_avg_list.append(mse_avg)
            mse_avg_list_lms.append(mse_avg_lms)
            mse_avg_list_nonlinear.append(mse_avg_nonlinear)
            mse_avg_list_nonlinear_lms.append(mse_avg_nonlinear_lms)
            print mse_avg
            print mse_avg_lms
            print mse_avg_nonlinear
            print mse_avg_nonlinear_lms


        mse_avg_list = 10*np.log10(mse_avg_list)
        mse_avg_list_lms = 10*np.log10(mse_avg_list_lms)
        plt.figure(1)
        plt.plot(SNR_RANGE, mse_avg_list)
        plt.plot(SNR_RANGE, mse_avg_list_nonlinear)

        plt.legend(['CMA- Watterson Model', 'CMA- Nonlinear Model'])
        #plt.plot(SAMPLES, mse_avg_list)
        plt.xlabel('SNR (dB)')
        #plt.xlabel('Number of Samples')
        plt.ylabel('MSE (dB)')
        plt.title(' Mean Squared Error of CMA Equalizer: Poor Non-Linear Channel')
        plt.show()
        plt.figure(2)
        plt.plot(SNR_RANGE, mse_avg_list_lms)
        plt.plot(SNR_RANGE,mse_avg_list_nonlinear_lms)
        plt.legend(['LMS- Watterson Model', 'LMS- Nonlinear Model'])
        #plt.plot(SAMPLES, mse_avg_list_lms)
        plt.xlabel('SNR (dB)')
        #plt.xlabel('Number of Samples')
        plt.ylabel('MSE (dB)')
        plt.title(' Mean Squared Error of LMS Equalizer: Poor Non-Linear Channel')
        plt.show()






        '''    
        scale_factor = 1.0/np.sqrt((tap1*np.conj(tap1))+(tap2*np.conj(tap2)))
        tap1 = scale_factor * tap1 * .5
        tap2 = scale_factor * tap2 * .5


        top_block = cma_watterson_experiment(50, 4096, (tap1, tap2))
        top_block.start()
        top_block.wait()
        self.symbols = top_block.blocks_vector_sink_x_0.data()
        top_block.stop()

        plt.figure(1)
        plt.scatter(np.real(self.symbols)[0:100], np.imag(self.symbols)[0:100])

        plt.figure(2)
        plt.scatter(np.real(self.symbols)[3000:-1], np.imag(self.symbols)[3000:-1])
        plt.show()

        ## calculate the error rate
        self.const_points = top_block.const.points()
        self.error_check()
        '''



if __name__ == '__main__':
    WattersonEqualization()

