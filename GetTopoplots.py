import numpy as np
import scipy.io as sio
from scipy.signal import welch
from scipy.integrate import simps
from Topoplots_functions import *

#str_DataPath = 'C:/Users/afcad/Desktop/Taller EEG/Analisis/Resultados/Sujeto 5/'  # path file where the data is stored
str_DataPath = 'C:/Users/Sebastian/Documents/NeuroZenProcessing/Preprocessed/'
#str_FileName = 'Mindfulness/Sujeto5_preprocesadomf.mat'  # Name of the File
str_FileName = 'Suj_6_R_v2'
dict_allData = sio.loadmat(str_DataPath + str_FileName)

#dict_allData = sio.loadmat(str_DataPath + str_FileName)['data']  # Load .mat data

d_SampleRate = np.double(dict_allData['srate'][0][0])

arr = (np.array(dict_allData['chanlocs']['labels'][0][0:58]))
names_array = np.array([item[0] for item in arr])
print((names_array))
v_ChanNames = names_array
    
v_FreqBands = [[1, 4], [4, 8], [8, 12], [18, 30]]
v_FreqBands_Names = ['Delta', 'Theta', 'Alpha', 'Beta']
    
d_WindSec = 3
d_stepSec = 1.5

m_Data_MF = dict_allData['data']
print(m_Data_MF)

m_PSDData_MF = getWelch(m_Data_MF, d_SampleRate, v_ChanNames, v_FreqBands, v_FreqBands_Names, d_WindSec, d_stepSec)  # Get PSD data for MF

str_FileName = 'Suj_6_MF'  # Name of the File

#dict_allData = sio.loadmat(str_DataPath + str_FileName)['data']  # Load .mat data
dict_allData = sio.loadmat(str_DataPath + str_FileName)
m_Data_R = dict_allData['data']

m_PSDData_R = getWelch(m_Data_R, d_SampleRate, v_ChanNames, v_FreqBands, v_FreqBands_Names, d_WindSec, d_stepSec)   # Get PSD data for R

### normalize data

m_PSDData_MF_norm = normalize(m_PSDData_MF, m_PSDData_R) 

### mean of normalized data

m_PSDData_MF_norm_mean = meanofNormalizedData(m_PSDData_MF_norm)

##PSD Evolution Graph

v_TimeArray = np.arange(0,len(m_PSDData_MF[0][0]))*d_stepSec
fig, axs = plt.subplots(len(v_FreqBands), 1, figsize=(10, 8))
for i in range(len(v_FreqBands)):
    for j in range(len(v_ChanNames)):
        axs[i].plot(v_TimeArray, m_PSDData_MF_norm[j][i], linewidth=0.5)
        axs[i].set_title("Ondas " + str(v_FreqBands_Names[i]))
        axs[i].set_xlabel("Time")
        axs[i].set_ylabel("Amplitude")
fig.suptitle("      PSD Evolution", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.show()


##Save data in mat

str_DataPath_Save='C:/Users/Sebastian/Documents/NeuroZenProcessing/Preprocessed/'

sio.savemat(str_DataPath_Save + 'm_PSDData_MF_norm_mean.mat', mdict={'m_Data': m_PSDData_MF_norm,
                                             'v_ChanNames': v_ChanNames,
                                             'chanlocs': dict_allData['chanlocs'],
                                             'd_SampleRate': d_SampleRate,
                                             'v_FreqBands': v_FreqBands})

### topos

getTopoplots(m_PSDData_MF_norm_mean, v_FreqBands_Names,len(v_ChanNames),v_ChanNames)

### connectivity
connectivity(m_PSDData_MF_norm, v_FreqBands_Names,v_ChanNames)
#print(Connectivity(m_PSDData_MF_norm_mean))