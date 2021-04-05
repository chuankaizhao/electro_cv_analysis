import argparse
import parse_input
import plot_cv
import integrate_peak

def parse_cmdln():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('-i', '--input', action='store', dest='input',
                        help='File containing I-V data.', required=True)
    parser.add_argument('-c', '--current', dest='current',
                        type=str, nargs='*',
                        help='Excel location where current data pop up: -i D12, F12', required=True)
    parser.add_argument('-v', '--voltage', dest='voltage',
                        type=str, nargs='*', 
                        help='Excel location where voltage data pop up: -i C12, E12', required=True)
    parser.add_argument('-ps', '--performSmooth', action='store_true', dest='smooth', 
                        help='Smooth CV curve', default=False)
    parser.add_argument('-po', '--plotOriginal', action='store_true', dest='plotOriginal', 
                        help='Plot both original and smoothed CV curve when smooth method is used', default=False)
    parser.add_argument('-pa', '--performAnalysis', action='store_true', dest='analysis',
                        help='Perform analysis for peaks in CV curve', default=False)
    parser.add_argument('-pp', '--plotProperties', dest='plotArgs', 
                        help='Additional arguments for making CV plot')
    parser.add_argument('-o', '--output', dest='out',
                        help='Name of I-V plot and integration output', default='CV_analysis')
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    args = parse_cmdln()
    
    inputData, smoothData, xlabel, ylabel = parse_input.parse_input(args)
    
    plot_cv.plot_cv(args, inputData, smoothData, xlabel, ylabel)
    
    if args.analysis:
        if args.smooth:
            integrate_peak.integration(args, smoothData)
        else:
            integrate_peak.integration(args, inputData)