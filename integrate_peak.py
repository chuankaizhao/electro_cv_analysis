import peakutils
import numpy as np

BASE_CURRENT_POS = 0.1
BASE_CURRENT_NEG = -0.1

def get_peaks(inputData):
    print("Getting peaks ...")
    peaks = []
    for data in inputData:
        peak = []
        indexes = peakutils.indexes(np.abs(data[1]), min_dist=20)
        for index in indexes:
            peak.append([index, data[0][index], data[1][index]])
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

def get_peak_and_integrate(data, peak, file):
    valid_peak_info = []
    for i, p in enumerate(peak):
        print(f'Processing peak {i+1}:')
        file.write(f'Processing peak {i+1}:\n')
        
        index, peak_volt, peak_curr = p[0], p[1], p[2]
        volt, curr = data[0], data[1]
        file.write(f'Peak position: V {peak_volt:.4f}, C {peak_curr:.4f}\n')

        left_valid, left_index = find_left(curr, volt, index)
        right_valid, right_index = find_right(curr, volt, index)
        if left_valid and right_valid:
            print("Peak valid, computing integration ...")
            q = np.trapz(curr[left_index:right_index], x=volt[left_index:right_index])
            file.write(f'Integration results: {q:.6f}, computed over volatge between {min(volt[left_index], volt[right_index]):.4f} and {max(volt[left_index], volt[right_index]):.4f})\n')
            valid_peak_info.append([peak_volt, peak_curr, q])
        else:
            print("Peak invalid, continue ...")
            file.write(f'Integration results: invalid peak!\n')
    return valid_peak_info

def integration(args, inputData):
    print("Performing peak and integration analysis ...")
    peaks = get_peaks(inputData)
    file  = open(args['output'] + '_analysis.txt', 'w')
    for i, data in enumerate(inputData):
        print(f"Starting from CV curve {i+1}")
        file.write(f'Experiment {i}:\n')
        file.write(f'============================================\n')
        valid_peak_info = get_peak_and_integrate(data, peaks[i], file)
        if len(valid_peak_info) == 2:
            print(f'Summary: awesome, found two valid peaks ...')
            file.write(f'********Summary********\n')
            file.write(f'The average V between two peaks: {(valid_peak_info[0][0]+valid_peak_info[1][0])/2:.4f}')
    file.close()
    print(f"Peak and integration analysis done! Check the output file: {args['output'] + '.png'} and {args['output'] + '.txt'}\n")
    return valid_peak_info