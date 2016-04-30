import numpy as np
import os



def class Stock(object):
    def __init__(self, stock, file.location = 'C:/scripts/Python/Quote')
        if os.path.isfile(file.location + "/" + stock + '.csv'):
            self.info = np.genfromtxt(fname = file.location + "/" + stock + '.csv',delimiter = ",", names = True)
        else:
            raise FileNotFoundError

    def moving_average(self, min_num_of_days = 3, max_num_of_days = len(self) - 1):
        tempArry = np.zeros(len(self))
        for x in range(max(min_num_of_days - 1,0), max_num_of_days - 1):
            for y in range(x,len(self) - 1):
                tempmean = mean()

    def moving_average_simple(a, n=3) :
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def smooth(x,window_len=11,window='hanning'):
   4     """smooth the data using a window with requested size.
   5
   6     This method is based on the convolution of a scaled window with the signal.
   7     The signal is prepared by introducing reflected copies of the signal
   8     (with the window size) in both ends so that transient parts are minimized
   9     in the begining and end part of the output signal.
  10
  11     input:
  12         x: the input signal
  13         window_len: the dimension of the smoothing window; should be an odd integer
  14         window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
  15             flat window will produce a moving average smoothing.
  16
  17     output:
  18         the smoothed signal
  19
  20     example:
  21
  22     t=linspace(-2,2,0.1)
  23     x=sin(t)+randn(len(t))*0.1
  24     y=smooth(x)
  25
  26     see also:
  27
  28     numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
  29     scipy.signal.lfilter
  30
  31     TODO: the window parameter could be the window itself if an array instead of a string
  32     NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
  33     """
  34
  35     if x.ndim != 1:
  36         raise ValueError, "smooth only accepts 1 dimension arrays."
  37
  38     if x.size < window_len:
  39         raise ValueError, "Input vector needs to be bigger than window size."
  40
  41
  42     if window_len<3:
  43         return x
  44
  45
  46     if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
  47         raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
  48
  49
  50     s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
  51     #print(len(s))
  52     if window == 'flat': #moving average
  53         w=np.ones(window_len,'d')
  54     else:
  55         w=eval('numpy.'+window+'(window_len)')
  56
  57     y=np.convolve(w/w.sum(),s,mode='valid')
  58     return y
  59
__author__ = 'Asmodi'
