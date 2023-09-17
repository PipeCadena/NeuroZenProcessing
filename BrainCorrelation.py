import scipy.io as sio
import numpy as np
from Functions.f_SignalProcFuncLibs import *
from visbrain.objects import TopoObj, ColorbarObj, SceneObj
from matplotlib.colors import ListedColormap
from scipy.stats import pearsonr
import seaborn as sn

import matplotlib.pyplot as plt

str_DataPath = 'Data/'  # path file where the data is stored
str_FileName = 'PSD.mat'  # Name of the File

dict_allData = sio.loadmat(str_DataPath + str_FileName)  # Load .mat data
m_Data = dict_allData['m_Data']
d_SampleRate = np.double(dict_allData['d_SampleRate'][0])
v_ChanNames = np.array(dict_allData['v_ChanNames'])
v_FreqBands = np.array(dict_allData['v_FreqBands'])
v_SessionTimes = np.array(dict_allData['v_SessionTimes'][0])
d_Time1 = v_SessionTimes[0]
d_Time2 = v_SessionTimes[1]
v_FreqBands_Names = ['Delta', 'Alpha', 'Fast Beta']  # Names of the frequency bands
d_WindSec = 25
d_stepSec = 10
d_SampleRate = 1/2.5
d_WindSam = int(d_WindSec * d_SampleRate)
d_stepSam = int(d_stepSec * d_SampleRate)

m_AllCorrelation_Bef = []
m_AllCorrelation_Dur = []
m_AllCorrelation_Aft = []


for i_band in range(len(m_Data[0])):
    print(f'##################################################')
    print(f'PSD - processing freq band: {v_FreqBands_Names[i_band]}')
    print(f'##################################################')

    m_channCorrelation_Bef = np.zeros([len(m_Data), len(m_Data)])
    m_channCorrelation_Dur = np.zeros([len(m_Data), len(m_Data)])
    m_channCorrelation_Aft = np.zeros([len(m_Data), len(m_Data)])

    for i_chan1 in range(len(m_Data)):
        v_PSDEvolution1 = m_Data[i_chan1][i_band]

        for i_chan2 in range(len(m_Data)):
            v_PSDEvolution2 = m_Data[i_chan2][i_band]

            if i_chan1 != i_chan2:

                d_indexStart = 0
                d_indexEnd = int(d_indexStart + d_WindSam)
                v_PSDCorr = []
                d_count = 0
                while d_indexEnd <= len(v_PSDEvolution1):
                    i_dataWind1 = v_PSDEvolution1[d_indexStart:d_indexEnd]
                    i_dataWind2 = v_PSDEvolution2[d_indexStart:d_indexEnd]

                    d_PSDCorr = pearsonr(i_dataWind1, i_dataWind2)[0]
                    v_PSDCorr.append(d_PSDCorr)
                    d_count += 1

                    d_indexStart = int(d_indexStart + d_stepSam)
                    d_indexEnd = int(d_indexStart + d_WindSam)

                m_channCorrelation_Bef[i_chan1, i_chan2] = np.mean(v_PSDCorr[0:int(v_SessionTimes[0] / d_stepSec)])
                m_channCorrelation_Dur[i_chan1, i_chan2] = np.mean(v_PSDCorr[int(v_SessionTimes[0] / d_stepSec):int(v_SessionTimes[1] / d_stepSec)])
                m_channCorrelation_Aft[i_chan1, i_chan2] = np.mean(v_PSDCorr[int(v_SessionTimes[1] / d_stepSec):])

            else:
                m_channCorrelation_Bef[i_chan1, i_chan2] = 0
                m_channCorrelation_Dur[i_chan1, i_chan2] = 0
                m_channCorrelation_Aft[i_chan1, i_chan2] = 0

    m_AllCorrelation_Bef.append(np.mean(m_channCorrelation_Bef,1))
    m_AllCorrelation_Dur.append(np.mean(m_channCorrelation_Dur,1))
    m_AllCorrelation_Aft.append(np.mean(m_channCorrelation_Aft,1))

m_AllCorrelation_Bef = np.array(m_AllCorrelation_Bef)


import pandas as pd

df = pd.DataFrame(m_AllCorrelation_Dur[0])
corr = df.corr()
#tick_labels =  ['Fp1', 'Fpz','Fp2','F7','F3','Fz','F4','F8','FC5','FC1','FC2','FC6','T7','C3','Cz','C4','T8','CP5','CP1','CP2',
#            'CP6','P7','P3','Pz','P4','P8','POz','O1','O2','AF7','AF3','AF4','AF8','F5','F1','F2','F6','FC3','FCz','FC4',
#            'C5','C1','C2','C6','CP3','CP4','P5','P1','P2','P6','PO5','PO3','PO4','PO6','FT7','FT8','TP7','TP8','PO7','PO8','Oz']

tick_labels = ['Fp1', 'Fp2', 'T3', 'T4', 'C3', 'C4', 'O1', 'O2']

sn.heatmap(corr, xticklabels=tick_labels, yticklabels=tick_labels, cmap = 'RdYlBu')


title_props = {'family': 'serif', 'size': 20, 'weight': 'bold', 'color': 'black'}
plt.title("Effective connectivity (weighted directed network)", fontdict=title_props)
plt.show()
#corr.style.background_gradient(cmap='coolwarm')


