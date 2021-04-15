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

def plot(plotArgs, data, ax, ls, plot_type, factor):
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    colors = ["#ff4c00", "#00d07c", "#ff9400", "#0772ca", ]
    
    legends = plotArgs['legends'] if 'legends' in plotArgs else np.arange(len(data))

    for i, d in enumerate(data):
        color   = cmap(i+1/len(data)) if len(data) > 4 else colors[i]
        if plot_type == 'area':
            ax.plot(d[0], d[1]/factor, lw=0.8, c=color, ls=ls, label=legends[i])
        else:
            ax.plot(d[0], d[2]/factor, lw=0.8, c=color, ls=ls, label=legends[i])

def plot_cv_normalized_by_area(args, inputData, smoothData, xlabel, ylabel):
    ax  = plt.subplot2grid((2,2),(0,0))
    
    plotArgs = args['plot_args_a']
        
    xlabel = plotArgs['xlabel'] if 'xlabel' in plotArgs else xlabel
    ylabel = plotArgs['ylabel'] if 'ylabel' in plotArgs else ylabel
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if 'xlim' in plotArgs: ax.set_xlim(plotArgs['xlim'][0], plotArgs['xlim'][1])
    if 'ylim' in plotArgs: ax.set_ylim(plotArgs['ylim'][0], plotArgs['ylim'][1])

    if not args['perform_smooth']:
        print("Plotting CV curves normalized by area based on original data")
        plot(plotArgs, inputData, ax, '-', "area", 1)
    
    if args['perform_smooth']:
        print("Plotting CV curves normalized by area based on moving averages of original data")
        plot(plotArgs, smoothData, ax, '-', "area", 1)
        
        if args['plot_curve_compare']: plot(plotArgs, inputData, ax, '--', "area", 1)
        
    ax.legend(loc=2, ncol=1, frameon=False, prop=fontP)
    plt.tight_layout()
    plt.savefig(args['output'] + '_a.png', dpi=500, bbox_inches='tight')

def plot_cv_normalized_by_q(args, inputData, smoothData, xlabel, ylabel, factor):
    ax  = plt.subplot2grid((2,2),(0,0))
    
    plotArgs = args['plot_args_q']
        
    xlabel = plotArgs['xlabel'] if 'xlabel' in plotArgs else xlabel
    ylabel = plotArgs['ylabel'] if 'ylabel' in plotArgs else ylabel
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if 'xlim' in plotArgs: ax.set_xlim(plotArgs['xlim'][0], plotArgs['xlim'][1])
    if 'ylim' in plotArgs: ax.set_ylim(plotArgs['ylim'][0], plotArgs['ylim'][1])

    if not args['perform_smooth']:
        print("Plotting CV curves normalized by q based on original data")
        plot(plotArgs, inputData, ax, '-', "q", factor)
    
    if args['perform_smooth']:
        print("Plotting CV curves normalized by q based on moving averages of original data")
        plot(plotArgs, smoothData, ax, '-', "q", factor)
        
        if args['plot_curve_compare']: plot(plotArgs, inputData, ax, '--', "area", 1)
        
    ax.legend(loc=2, ncol=1, frameon=False, prop=fontP)
    plt.tight_layout()
    plt.savefig(args['output'] + '_q.png', dpi=500, bbox_inches='tight')