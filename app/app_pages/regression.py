# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
from scipy import interpolate

response_scale = [1, 0.75, 0.5, 0.25, 0]
sil_mean = [0.5, 0.05, 0.005, 0.0005, 0.00005]
sil_lower = [0.1, 0.01, 0.001, 0.0001, 0.00001]
sil_upper = [1, 0.1, 0.01, 0.001, 0.0001]

interp_mean = interpolate.interp1d(response_scale, np.log(sil_mean), kind='linear')
interp_lower = interpolate.interp1d(response_scale, np.log(sil_lower), kind='linear')
interp_upper = interpolate.interp1d(response_scale, np.log(sil_upper), kind='linear')

def get_sil_val(scale):
  mean =  np.exp(interp_mean(scale))
  lower = np.exp(interp_lower(scale))
  upper = np.exp(interp_upper(scale))
  return lower, mean, upper

