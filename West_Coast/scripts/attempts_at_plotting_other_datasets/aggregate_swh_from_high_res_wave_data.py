import pandas as pd
import numpy as np
from rex import Resource, WaveResource
from rex.temporal_stats.temporal_stats import TemporalStats # https://nrel.github.io/rex/_autosummary/rex.temporal_stats.temporal_stats.TemporalStats.html#rex.temporal_stats.temporal_stats.TemporalStats
import h5py


##### Assign region

region = 'West_Coast'

# load dataset
datapath = "/datasets/US_wave/v1.0.0/" + region + "/"  # wave dataset https://www.nrel.gov/water/wave-hindcast-dataset.html
year = 1999
ifile = datapath + 'West_Coast_wave_' + str(year) + '.h5'

# L202 in https://github.com/NREL/rex/blob/bc12dd3e850b564bd5131767b6dd83c83d99e886/tests/test_temporal_stats.py#L212-L216
dset = 'significant_wave_height'
with WaveResource(ifile) as res:
	meta = res.meta
out = TemporalStats.run(ifile, dset, statistics='mean', month=False,
			combinations=False, res_cls=WaveResource, max_workers=1, sites=[0])
print(out)

'''# initial attempt
year = 1999

# create temporal stats class instance
class_instance = temporal_stats.TemporalStats(ifile, statistics='mean')

# extract dataset
h5f = h5py.File(ifile, 'r')
ds_swh = h5f['significant_wave_height']

#class_instance.monthly(ifile, ds_swh) # https://nrel.github.io/rex/_autosummary/rex.temporal_stats.temporal_stats.TemporalStats.html#rex.temporal_stats.temporal_stats.TemporalStats.monthly
class_instance.monthly(ifile, 'significant_wave_height') '''



##### Plot the wave data on a map

