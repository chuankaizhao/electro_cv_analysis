import peakutils
import numpy as np

BASE_CURRENT_POS = 0.1
BASE_CURRENT_NEG = -0.1

def get_peaks(inputData):
    print("Getting peaks ...")
    peaks = []
    for data in inputData:
        peak = []
        indexes = peakutils.indexes(np.abs(data[2]), thres=0.1, min_dist=5)
        for index in indexes:
            peak.append([index, data[0][index], data[1][index], data[2][index]])
        peaks.append(peak)
    return peaks

def find_left(curr, volt, index):
    volt_break_point = np.argmax(volt)
    if curr[index] > 0:
        while index >= 0 and curr[index] > BASE_CURRENT_POS:
            index -= 1
        return (True, index) if index >= 0 else (False, index)
    if curr[index] < 0:
        while index >= volt_break_point and curr[index] < BASE_CURRENT_NEG:
            index -= 1
        return (True, index) if index >= volt_break_point else (False, index)

def find_right(curr, volt, index):
    volt_break_point = np.argmax(volt)
    if curr[index] > 0:
        while index <= volt_break_point and curr[index] > BASE_CURRENT_POS:
            index += 1
        return (True, index) if index <= volt_break_point else (False, index)
    if curr[index] < 0:
        while index < len(curr) and curr[index] < BASE_CURRENT_NEG:
            index += 1
        return (True, index) if index < len(curr) else (False, index)

def check_integration(expr_id, file, valid_peak_info):
    diff = abs(valid_peak_info[0][2] - valid_peak_info[1][2])/valid_peak_info[0][2]
    if diff > 0.05: 
        file.write(f"Are integration nearly equal for two peaks in experiment {expr_id}: No, you should CHECK the peaks!")
    else:
        file.write(f"Are integration nearly equal for two peaks in experiment {expr_id}: Yes, looks good!")
        
def filter_peak_integration(valid_peak_info):
    valid_peak_info.sort(key=lambda x: -x[4])
    return valid_peak_info[0:2]
    
def get_peak_and_integrate(data, peak, file):
    valid_peak_info = []
    for i, p in enumerate(peak):
        print(f'Processing peak {i+1}:')
        file.write(f'Processing peak {i+1}:\n')
        
        index, peak_volt, peak_curr_area, peak_curr = p[0], p[1], p[2], p[3]
        volt, curr_area, curr = data[0], data[1], data[2] 
        file.write(f'Peak position: V {peak_volt:.4f}, C/area {peak_curr_area:.4f}, C {peak_curr:.4f}\n')

        left_valid, left_index = find_left(curr_area, volt, index)
        right_valid, right_index = find_right(curr_area, volt, index)
        if left_valid and right_valid:
            print("Peak valid, computing integration ...")
            q = np.trapz(curr[left_index:right_index], x=volt[left_index:right_index])
            file.write(f'Integration results: {q:.6f}, computed over volatge between {min(volt[left_index], volt[right_index]):.4f} and {max(volt[left_index], volt[right_index]):.4f})\n')
            volt_span = max(volt[left_index], volt[right_index]) - min(volt[left_index], volt[right_index])
            valid_peak_info.append([peak_volt, peak_curr_area, peak_curr, q, volt_span])
        else:
            print("Peak invalid, continue ...")
            file.write(f'Integration results: invalid peak!\n')
    return valid_peak_info

def integration(args, inputData):
    print("Performing peak and integration analysis ...")
    peaks = get_peaks(inputData)
    valid_peak_infos = []
    file  = open(args['output'] + '_analysis.txt', 'w')
    for i, data in enumerate(inputData):
        file.write(f'Experiment {i+1}:\n')
        file.write(f'============================================\n')
        valid_peak_info = get_peak_and_integrate(data, peaks[i], file)
        file.write(f'********Summary********\n')
        if len(valid_peak_info) == 2:
            print(f'Summary: awesome, found two valid peaks ...')
            file.write(f'The average V between two peaks: {(valid_peak_info[0][0]+valid_peak_info[1][0])/2:.4f}\n')
            check_integration(i+1, file, valid_peak_info)
        elif len(valid_peak_info) > 2 and args['ignore_addtional_peaks']:
            valid_peak_info = filter_peak_integration(valid_peak_info)
            print(f'Summary: oops, found more than two valid peaks, will proceed with the two with the widest voltage span ...')
            file.write(f'The average V between two peaks: {(valid_peak_info[0][0]+valid_peak_info[1][0])/2:.4f}\n')
            check_integration(i+1, file, valid_peak_info)
        else:
            file.write(f'The average V between two peaks: :(, less than two peaks are found\n')
        valid_peak_infos.append(valid_peak_info)
    file.close()
    print(f"Peak and integration analysis done!")
    print(f"Check the output file: {args['output'] + '.png'} and {args['output'] + '.txt'}")
    return valid_peak_infos
