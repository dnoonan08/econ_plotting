import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import matplotlib.colors as mcolors

import mplhep
mplhep.style.use(mplhep.style.CMS)

import json

def delay_scan_plots(fname,
                     title='ETx Delay Scan',
                     outputFileName=None,
                     ECOND=False):

    if 'json' in fname:
        data = json.load(open(fname))
        for t in data['tests']:
            if 'test_eTX_delayscan' in t['nodeid']:
                x = np.array(t['metadata']['eTX_errcounts'])
                y = np.array(t['metadata']['eTX_bitcounts'])
                break
        errorRates = (x/y).T.flatten()
        nBins = x.shape[0]

    else:
        data = np.load(f'./{fname}.npz',allow_pickle=True )
        x = data['errorcounts'].flatten()[0]
        y = data['bitcounts'].flatten()[0]
        errorRates = []

        for i in range(6):
            errorRates.append(list(np.array(x[i])/np.array(y[i])))

        errorRates = np.array(errorRates).T.flatten()

        if ECOND:
            nBins = 6
        else:
            nBins = 13

    a,b=np.meshgrid(np.arange(nBins),np.arange(63))
    fig,ax=plt.subplots()

    plt.hist2d(a.flatten(),b.flatten(),
               weights=errorRates,
               bins=(np.arange(nBins+1)-0.5,np.arange(64)-0.5),
               cmap='RdYlBu_r',
               alpha=errorRates>0,
               figure=fig);

    plt.colorbar().set_label(label='Transmission errors rate ',size=32)
    plt.title(title,size=32)
    plt.ylabel('Phase Select Setting', size=32)
    plt.xlabel('Channel Number', size=32)
    if outputFileName:
        plt.savefig(f'./ECOND_delay_scan_board{boardNum}_{freq}.png',dpi=300, facecolor = "w")
    plt.close(fig)

    return fig
