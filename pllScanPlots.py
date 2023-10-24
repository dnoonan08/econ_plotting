import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

import mplhep
mplhep.style.use(mplhep.style.CMS)

allowed_cap_bank_vals=np.array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,
                                  13,  14,  15,  24,  25,  26,  27,  28,  29,  30,  31,  56,  57,
                                  58,  59,  60,  61,  62,  63,  120, 121, 122, 123, 124, 125, 126,
                                  127, 248, 249, 250, 251, 252, 253, 254, 255, 504, 505, 506, 507,
                                  508, 509, 510, 511])

def pll_scan_plots(fname,
                   scale=8,
                   title='PLL CapBank Scan',
                   xlim=(35,50),
                   outputFileName=None,
                   ECOND=False):
    if ECOND==True:
        ## load the data
        autolockData = np.genfromtxt(f"./{fname}_autolocks.csv", delimiter=',')
        data = pd.read_csv(f"./{fname}_locks.csv", header=None)

        # frequency list is first row, locking states are all subsequent rows
        freq=data.loc[0].values
        lockState=data.dropna(axis=1).loc[1:].values

        ## Get autolock cap and frequency
        autolock_capIndex = allowed_cap_bank_vals.searchsorted(autolockData[1])[autolockData[2]==1]
        autolock_freq     = autolockData[0][autolockData[2]==1]

        ## Make the plots
        fig,ax=plt.subplots()
        bins=((np.array(list(freq) + [freq[-1]*2  - freq[-2]]) - (freq[1]-freq[0])/2.)/scale,np.arange(57)-0.5)
        _x,_y=np.meshgrid(freq/scale,np.arange(56))
        d=lockState.T.flatten()
        plt.hist2d(_x.flatten(),
                   _y.flatten(),
                   weights=d,
                   bins=bins,
                   alpha=d>0,
                   cmap='Blues',
                   figure=fig
                   )
        plt.scatter((autolock_freq/scale),autolock_capIndex,color="red",label="Automatic Lock")

        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Lock with VCO Override')
        handles.append(patch)
        plt.legend(handles=handles)

        plt.xlabel('Frequency Setting (MHz)', size=32)
        plt.ylabel('CapBank Select Setting', size=32)
        plt.title(title)
        plt.xlim(xlim)

        if outputFileName:
            plt.savefig(outputFileName,dpi=300, facecolor = "w")
        plt.close(fig)

        return fig
    else:
        mainlist=[]
        with open(f"./{fname}.txt") as f:
            mainlist = [list(literal_eval(line)) for line in f]
        pllSettings = np.array(mainlist)
        b,a=np.meshgrid(np.arange(35,44,(1/32)),np.arange(56))
        plt.hist2d(b.flatten(),a.flatten(),weights=pllSettings.T.flatten(),bins=(np.arange(34,45,(1/32)),np.arange(57)),cmap='Blues')
        plt.xlabel('Reference Clock Frequency Setting (MHz)', size=32)
        plt.ylabel('CapBank Select Setting', size=32)
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Lock with VCO Override')
        handles.append(patch)
        plt.legend(handles=handles, loc='lower left')
        plt.title(title)
        plt.axvline(40)
        plt.rcParams.update({'font.size': 15})
        plt.xlim([35,50])
        if outputFileName:
            plt.savefig(outputFileName,dpi=300, facecolor = "w")
        plt.figure()


