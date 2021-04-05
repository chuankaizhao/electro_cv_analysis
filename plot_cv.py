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
fontP.set_size('10')

def parse_plot_args(arg):
    plotArgs = {}
    
    if arg:
        for item in arg.split(','):
            key, value = item.split(':')
            key = key.strip()
            value = value.strip()
            if len(value.split()) == 1 and key != 'legends':
                plotArgs[key] = value
            else:
                plotArgs[key] = value.split("|")
    
    print(plotArgs)
        
    return plotArgs

def plot(plotArgs, data, ax, ls):
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    
    legends = plotArgs['legends'] if 'legends' in plotArgs else np.arange(len(data))

    for i, d in enumerate(data):
        color   = cmap(i+1/len(data))  
        ax.plot(d[0], d[1], lw=0.8, c=color, ls=ls, label=legends[i])

def plot_cv(args, inputData, smoothData, xlabel, ylabel):
    ax  = plt.subplot2grid((2,2),(0,0))
    
    plotArgs = parse_plot_args(args.plotArgs)
        
    xlabel = plotArgs['xlabel'] if 'xlabel' in plotArgs else xlabel
    ylabel = plotArgs['ylabel'] if 'ylabel' in plotArgs else ylabel
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if not args.smooth or (args.smooth and args.plotOriginal):
        print("Plotting CV curves based on original data")
        plot(plotArgs, inputData, ax, '--')
    
    if args.smooth:
        print("Plotting CV curves based on moving averages of original data")
        plot(plotArgs, smoothData, ax, '-')
        
    ax.legend(loc=2, ncol=1, frameon=False, prop=fontP)
    plt.tight_layout()
    plt.savefig(args.out + '.png', dpi=500, bbox_inches='tight')