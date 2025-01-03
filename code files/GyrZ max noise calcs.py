import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Moving average for smoothing
data = pd.read_excel('IMU drift estimation_IMU2_2nd portion.xlsx')
GyrZ = list(data['GyrZ (rad/s)'])

window_size = 250
  
i = 0
moving_average = []
moving_sigma = []    

while i <= len(GyrZ) - window_size:
    n = 0
    sum_sigma = 0
    window_values = GyrZ[i : i + window_size]
    window_average = sum(window_values) / window_size
    while n <= window_size - 1:  
        sum_sigma += (GyrZ[i+n] - window_average)**2
        n += 1
    window_sigma = np.sqrt(sum_sigma / window_size)    
    
    moving_average.append(window_average)
    moving_sigma.append(window_sigma)    
    
    i += 1

add_array = [0]*(window_size - 1)

moving_average_total = add_array + moving_average
moving_sigma_total = add_array + moving_sigma

# Plotting commands
t = list(data['Time (s)'])
    
params = {'figure.figsize': (15, 9), 
          'axes.labelsize': 16,
          'axes.titlesize': 16,
          'xtick.labelsize': 10, 
          'ytick.labelsize' : 10}
plt.rcParams.update(params)

plt.xlabel("Time (s)")
plt.ylabel("GyrZ_moving_sigma (rad/s)")
plt.title("GyrZ_moving_sigma")

plt.plot(t, moving_sigma_total, color='b')

plt.xticks(np.arange(min(t), max(t)+1, 25))
plt.legend(fontsize=16)

plt.show()

max_moving_sigma_total = max(moving_sigma_total)
index_max_moving_sigma_total = moving_sigma_total.index(max(moving_sigma_total))

print("Max sigma =", max_moving_sigma_total, "rad/s")
print("Time of max sigma =", t[index_max_moving_sigma_total], "s")
print("Time of max sigma - 10 =", t[index_max_moving_sigma_total]-10, "s")