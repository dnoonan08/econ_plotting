\1;95;0cimport numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplhep
mplhep.style.use(mplhep.style.CMS)

allowed_cap_bank_vals=np.array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,
                                  13,  14,  15,  24,  25,  26,  27,  28,  29,  30,  31,  56,  57,
                                  58,  59,  60,  61,  62,  63,  120, 121, 122, 123, 124, 125, 126,
                                  127, 248, 249, 250, 251, 252, 253, 254, 255, 504, 505, 506, 507,
                                  508, 509, 510, 511])

def pll_scan_plots(fname,
                   dataArray = None,
                   lowFreq = None,
                   highFreq = None,
                   scale=8,
                   title='PLL CapBank Scan',
                   xlim=(35,50),
                   outputFileName=None,
                   ECOND=False):


    if dataArray is not None:

        locks = np.array(dataArray[0]['tests'][0]['metadata']['locks'])
        auto_vco = dataArray[0]['tests'][1]['metadata']['auto_vco']
        auto_locks = dataArray[0]['tests'][1]['metadata']['auto_locks']
        frequencies_used = dataArray[0]['tests'][1]['metadata']['frequencies_used']
        weights = locks.T.flatten()


    else:
        mainlist=[]
        with open(f"./{fname}.csv") as f:
            mainlist = [list(literal_eval(line)) for line in f]
        pllSettings = np.array(mainlist)[0]
        weights = pllSettings.T.flatten()


    b,a=np.meshgrid(np.arange(lowFreq,highFreq,(1/scale)),np.arange(56))
    bins=(np.arange(lowFreq,(highFreq+(1/scale)),(1/scale))-(0.5/scale),np.arange(57)-0.5)
    fig,ax=plt.subplots()
    plt.hist2d(b.flatten(),
               a.flatten(),
               weights=weights,
               bins=bins,
               alpha=d>0,
               cmap='Blues',
               figure=fig
               )

    handles, labels = plt.gca().get_legend_handles_labels()
    patch = mpatches.Patch(color='#08306b', label='PLL Lock with VCO Override')
    handles.append(patch)
    plt.xlabel('Frequency Setting (MHz)', size=32)
    plt.ylabel('CapBank Select Setting', size=32)
    plt.title(title)
    plt.xlim(xlim)


    if ECOND == True:


        # frequency list is first row, locking states are all subsequent rows                                                                                                                                                                                                                                                                                    
        freq=frequencies_used
        lockState=locks

        ## Get autolock cap and frequency                                                                                                                                                                                                                                                                                                                        
        autolock_capIndex = allowed_cap_bank_vals.searchsorted(auto_vco)[auto_locks==1]
        autolock_freq     = frequencies_used[auto_locks==1]

        ## Make the plots                                                                                                                                                                                                                                                                                                                                        
        plt.scatter((autolock_freq/scale),autolock_capIndex,color="red",label="Automatic Lock")

    plt.legend(handles=handles)
    if outputFileName:
        plt.savefig(outputFileName,dpi=300, facecolor = "w")
    plt.close(fig)
    return fig




