import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
params = {'mathtext.default': 'regular', 'xtick.direction':'out', 'ytick.direction':'out' }
plt.rcParams.update(params)

from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('6')

def get_catalyst_weight(q, molecular_weight):
    return (q / 96.485) * molecular_weight   ## unit is ug

def plot_a(plotArgs, data, ax, ls):
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    colors = ["#ff4c00", "#00d07c", "#ff9400", "#0772ca", ]
    
    legends = plotArgs['legends'] if 'legends' in plotArgs else np.arange(len(data))

    for i, d in enumerate(data):
        color   = cmap(i+1/len(data)) if len(data) > 4 else colors[i]
        ax.plot(d[0], d[1], lw=0.8, c=color, ls=ls, label=legends[i])

def plot_q(plotArgs, data, ax, ls, valid_peak_infos, molecular_weight):
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    colors = ["#ff4c00", "#00d07c", "#ff9400", "#0772ca", ]
    
    legends = plotArgs['legends'] if 'legends' in plotArgs else np.arange(len(data))
    
    for i, d in enumerate(data):
        valid_peak_info = valid_peak_infos[i]
        color   = cmap(i+1/len(data)) if len(data) > 4 else colors[i]
        if len(valid_peak_info) == 2:
            mean_integration = (valid_peak_info[0][3] + valid_peak_info[1][3]) / 2
            ax.plot(d[0], d[2]/get_catalyst_weight(mean_integration, molecular_weight), lw=0.8, c=color, ls=ls, label=legends[i])
        else:
            print("skipping plot current/q because number of valid peaks is not equal to 2 ...")

def plot_cv_normalized_by_area(args, inputData, smoothData, xlabel, ylabel):
    ax  = plt.subplot2grid((2,2),(0,0))
    
    plotArgs = args['plot_args_a']
        
    xlabel = plotArgs['xlabel'] if 'xlabel' in plotArgs else xlabel
    ylabel = plotArgs['ylabel'] if 'ylabel' in plotArgs else r'j (mA/cm$^{2}$)'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if 'xlim' in plotArgs: ax.set_xlim(plotArgs['xlim'][0], plotArgs['xlim'][1])
    if 'ylim' in plotArgs: ax.set_ylim(plotArgs['ylim'][0], plotArgs['ylim'][1])

    if not args['perform_smooth']:
        print("Plotting CV curves normalized by area based on original data")
        plot_a(plotArgs, inputData, ax, '-')
    
    if args['perform_smooth']:
        print("Plotting CV curves normalized by area based on moving averages of original data")
        plot_a(plotArgs, smoothData, ax, '-')
        
        if args['plot_curve_compare']: plot_a(plotArgs, inputData, ax, '--')
        
    ax.legend(loc=2, ncol=1, frameon=False, prop=fontP)
    plt.tight_layout()
    plt.savefig(args['output'] + '_a.png', dpi=500, bbox_inches='tight')

def plot_cv_normalized_by_q(args, inputData, smoothData, xlabel, ylabel, valid_peak_infos):
    ax  = plt.subplot2grid((2,2),(0,0))
    
    plotArgs = args['plot_args_q']
        
    xlabel = plotArgs['xlabel'] if 'xlabel' in plotArgs else xlabel
    ylabel = plotArgs['ylabel'] if 'ylabel' in plotArgs else r'I (mA/$\mu$g)'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if 'xlim' in plotArgs: ax.set_xlim(plotArgs['xlim'][0], plotArgs['xlim'][1])
    if 'ylim' in plotArgs: ax.set_ylim(plotArgs['ylim'][0], plotArgs['ylim'][1])

    if not args['perform_smooth']:
        print("Plotting CV curves normalized by q based on original data")
        plot_q(plotArgs, inputData, ax, '-', valid_peak_infos, args['molecular_weight'])
    
    if args['perform_smooth']:
        print("Plotting CV curves normalized by q based on moving averages of original data")
        plot_q(plotArgs, smoothData, ax, '-', valid_peak_infos, args['molecular_weight'])
        
        if args['plot_curve_compare']: plot_q(plotArgs, inputData, ax, '--', valid_peak_infos, args['molecular_weight'])
        
    ax.legend(loc=2, ncol=1, frameon=False, prop=fontP)
    plt.tight_layout()
    plt.savefig(args['output'] + '_q.png', dpi=500, bbox_inches='tight')