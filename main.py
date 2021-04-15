import json
import parse_input
import parse_cmdln
import plot_cv
import integrate_peak

def main(args):
    
    inputData, smoothData, xlabel, ylabel_a, ylabel_q = parse_input.parse_input(args)
    
    plot_cv.plot_cv_normalized_by_area(args, inputData, smoothData, xlabel, ylabel_a)
    
    if args['perform_analysis']:
        if args['perform_smooth']:
            valid_peak_info=integrate_peak.integration(args, smoothData)
        else:
            valid_peak_info=integrate_peak.integration(args, inputData)
    
    if len(valid_peak_info) == 2:
        mean_integration = (valid_peak_info[0][2] + valid_peak_info[0][2]) / 2
        plot_cv.plot_cv_normalized_by_q(args, inputData, smoothData, xlabel, ylabel_q, mean_integration)
    
if __name__ == '__main__':
    args = parse_cmdln.parse_cmdln("inputfile.txt")
    main(args)