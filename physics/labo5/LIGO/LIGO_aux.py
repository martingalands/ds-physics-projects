from gwosc.locate import get_urls
import requests, os
import numpy as np

def downloadData(detector, t0):
    url = get_urls(detector, t0, t0)[-1][0:-4] + 'hdf5'

    print('\nDownloading data...\n')
    
    fn = os.path.basename(url)
    with open(fn,'wb') as strainfile:                 
        straindata = requests.get(url)
        strainfile.write(straindata.content)
        
    return fn


# function to cast TimeSeries data to python list
def toArray(v_in):
    v_out = np.ndarray(len(v_in))
    for i in range(0, len(v_in)):
        v_out[i] = np.double(v_in[i])
        
    return v_out
