#    This file is part of pyrlsdr.
#    Copyright (C) 2013 by Roger <https://github.com/roger-/pyrtlsdr>
#
#    pyrlsdr is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pyrlsdr is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyrlsdr.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division
import numpy as np
import numpy
from numpy import NaN, Inf, arange, isscalar, asarray, array
import sys
from rtlsdr import RtlSdr
from pylab import *
from rtlsdr import *
from pylab import *
from rtlsdr.rtlsdraio import RtlSdrAio
import csv
from math import exp, expm1
from multiprocessing import Pool
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
import time

#
#  Radio stations SNR level detection: www.behindthesciences.com
#  contact@behindthesciences.com
#   


class Scan: 
    def scan(self, id, object):   
        
        #Read iq data
        samples = object.read_samples(256*1024)
        
       #get the maximum amplitude in frequency
        sp = np.fft.fft(samples)
        ps_real=sp.real
        ps_imag=sp.imag
        sq=np.power(ps_real,2)+np.power(ps_imag,2)
        sqrt=np.sqrt(sq)
        psd=sqrt/1024
        max=np.max(psd)
        log=10*math.log10(max)
        object.close()
        freq=object.get_center_freq()
        return log, freq


if __name__ == '__main__':
    
    # Find the device index for a given serial number
    sdr = RtlSdr(serial_number='00000001')
    sdr2 = RtlSdr(serial_number='00000002')
    
        
    #Set Center Frequency
    cntr_freq1=sdr.set_center_freq(88200000)
    cntr_freq2=sdr2.set_center_freq(103500000)
    
    #Set Gain
   
    sdr.gain = 15
    sdr2.gain = 15
    
    #Set sample rate
    sdr.rs = 2.4e6
    sdr2.rs = 2.4e6
    
    #we save the sdr and sdr2 in the same array
    radios = [ sdr, sdr2]
    pool = ThreadPool(4)
    #create an object of class Scan
    s=Scan()
    def scan(args_tuple):
        global s
        id, code = args_tuple
        return s.scan(id, code)
    [log, freq]=pool.map(scan, enumerate(radios))
    print("Amplitude (dB), frequency(Hz)")
    print(log, freq)
    pool.close() 
    pool.join()

