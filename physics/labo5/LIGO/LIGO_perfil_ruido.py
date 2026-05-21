import numpy as np
import matplotlib.pyplot as plt

# from pycbc.waveform import get_fd_waveform
# from pycbc.filter import matched_filter
# from pycbc import vetoes

from gwpy.timeseries import TimeSeries
import gwpy.signal.filter_design

from LIGO_aux import downloadData

#%% - Data input and signal plor

detector = 'H1'
t0 = 1126259450

# sample rate in Hz
sample_rate = 4096

data_length_L = 16
data_length_R = 16

# downloads data in current working directory
file_name = downloadData(detector, t0)

# read desired channel from data
strain = TimeSeries.read(file_name, format='hdf5.losc')
center = int(t0)
strain = strain.crop(center - data_length_L, center + data_length_R)


sample_rate = strain.sample_rate
t = np.linspace(t0 - data_length_L, t0 + data_length_R, 4096*(data_length_L + data_length_R))

# plt.figure(1)
# plt.plot(t, strain)
# plt.xlabel('Time [s]')
# plt.ylabel('Strain [Adim.]')


#%% - Filtering the signal 

f_low = 50
f_high = 250

# There is a method too to whiten the data
strain_w = strain.whiten(4, 2)

# bandpass filter
bp = gwpy.signal.filter_design.bandpass(f_low, f_high, strain.sample_rate)



# notches
notches = [gwpy.signal.filter_design.notch(line, strain.sample_rate) for line in (60, 120, 180)]


zpk = gwpy.signal.filter_design.concatenate_zpks(bp, *notches)

# we apply filter
strain_filt = strain.filter(zpk, filtfilt=True)

    

# notice the filter wraparound which corrupts edge of signal
# plt.figure(2)
# plt.plot(t, strain_w)
# plt.xlabel('Time [s]')
# plt.ylabel('Strain [Adim.]')


plt.figure(5)
plt.plot(t, strain_filt)
plt.xlabel('Time [s]')
plt.xlim(t0-3 , t0 + 3)
plt.ylabel('Strain [Adim.]')

#%% - Generating some plots

# amplitude spectral density (asd)

asd = strain_w.asd(fftlength=8, overlap=4)
asdpost = strain_filt.asd(fftlength=8, overlap=4)


plt.figure(3)
plt.loglog(asd)
plt.xlabel('Frequency [Hz]')
plt.ylabel("ASD [1/\u221AHz]")

#deberia plotear post filtro
plt.figure(6)
plt.loglog(asdpost)
plt.xlabel('Frequency [Hz]')
plt.ylabel("POST FILTRO ASD [1/\u221AHz]")


# Q-transform (spectrogram with constant Q = f/df)

# -- q-transform plot (log-frequency spectrogram)
dt = 8  #-- Set width of q-transform plot, in seconds
hq = strain_filt.q_transform(outseg=(t0-dt, t0+dt))

plt.figure(4)
p = plt.pcolormesh(hq)
plt.colorbar(p, label='Normalized energy')
plt.yscale('log')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.xlim(t0 - 8, t0 + 8)
plt.show()

# picos = plt.ginput(10)
# print(picos[1])

#%% - accesssing data quality flags using gwpy

from gwpy.segments import DataQualityFlag

t1 = 1126259450
detector_f = 'L1'

start_time = t1 - data_length_L
end_time = t1 + data_length_R

# get CBC and BURST flags
cbc_flag = DataQualityFlag.fetch_open_data(f'{detector_f}_CBC_CAT2', start_time, end_time)
burst_flag = DataQualityFlag.fetch_open_data(f'{detector_f}_BURST_CAT2', start_time, end_time)

# print the segments in which flags say data is ok
print(cbc_flag.active)
print(burst_flag.active)
