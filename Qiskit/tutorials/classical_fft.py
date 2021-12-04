#%%
import numpy as np
from numpy.fft  import fft
# %%

a = np.array([1,0,0,0])
b = np.array([0,1,0,0])
c = np.array([0,0,1,0])
d =np.array([0,0,0,1])

a_fft = fft(a)
b_fft = fft(b)
c_fft = fft(c)
d_fft = fft(d)

# %%

t_4 = 0.25j*np.array([1,1.0j,-1,-1.0j])
fft(t_4)
# %%
