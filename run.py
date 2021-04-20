import json
import parse_input
import parse_cmdln
import plot_cv
import integrate_peak

def cv_analysis(args):
    print("##########################################################################")
    print("####                CV Curve Visualization and Analysis               ####")
    print("##########################################################################")
    
    print("\n")
    
    print("####                          Reading Input                           ####")
    
    inputData, smoothData, xlabel, ylabel_a, ylabel_q = parse_input.parse_input(args)
    
    print("\n")
    
    print("####                      Peak and integration analysis               ####")
    
    if args['perform_analysis']:
        if args['perform_smooth']:
            valid_peak_infos=integrate_peak.integration(args, smoothData)
        else:
            valid_peak_infos=integrate_peak.integration(args, inputData)
        
    print("\n")
    
    print("####                          Plot CV curves                          ####")
    
    plot_cv.plot_cv_normalized_by_area(args, inputData, smoothData, xlabel, ylabel_a)
    if args['perform_analysis']:
        plot_cv.plot_cv_normalized_by_q(args, inputData, smoothData, xlabel, ylabel_q, valid_peak_infos)
    
    print("\n")
    
    print("##########################################################################")
    print("####                          Done!                                   ####")
    print("##########################################################################")
