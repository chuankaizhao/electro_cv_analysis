import pandas as pd
import numpy  as np
import re

MOVING_WINDOW_SIZE = 10

regex = re.compile(r'(\d+|\s+)')

def parse_key(location):
    location = regex.split(location)
    row, col = location[1], location[0]
    if len(col) == 1:
        col = ord(col[0].upper()) - ord('A')
    else:
        col = (ord(col[0].upper()) - ord('A') + 1) * 26 + ord(col[1].upper()) - ord('A')   
    return int(row), col

def parse_data(df, location):
    row, col = parse_key(location)
    data = df.loc[row:, [col]].to_numpy().transpose()[0]
    return row, col, data

def parse_smooth_data(df, location):
    row, col = parse_key(location)
    data = df.loc[row:, [col]].rolling(MOVING_WINDOW_SIZE, min_periods=1, 
                                                              center=True).mean().to_numpy().transpose()[0]
    return row, col, data

def parse_input(args):
    try:
        df = pd.read_excel(args['input'], header=None)
        print("Successfully read the input file ...")
    except:
        print(f"Error: Loading {args['input']} failed!")
        
    inputData  = []
    smoothData = []
    
    currs = args['current']
    curr_areas = args['current_area']
    volts = args['voltage']
        
    for i, _ in enumerate(currs):
        curr, curr_area, volt = currs[i], curr_areas[i], volts[i]
        
        curr_row, curr_col, curr_data = parse_data(df, curr)
        curr_area_row, curr_area_col, curr_area_data = parse_data(df, curr_area)
        volt_row, volt_col, volt_data = parse_data(df, volt)
        
        inputData.append([volt_data, curr_area_data, curr_data])
        
        if i == 0:
            xlabel = list(df.loc[volt_row-1, [volt_col]])[0]
            ylabel_q = list(df.loc[curr_row-1, [curr_col]])[0]
            ylabel_a = list(df.loc[curr_area_row-1, [curr_area_col]])[0]
        
        if args['perform_smooth']:
            curr_row, curr_col, curr_data = parse_smooth_data(df, curr)
            curr_area_row, curr_area_col, curr_area_data = parse_smooth_data(df, curr_area)
            volt_row, volt_col, volt_data = parse_smooth_data(df, volt)
            smoothData.append([volt_data, curr_area_data, curr_data])
    
    print("Successfully processed the current and voltage data ...")
        
    return np.array(inputData), np.array(smoothData), xlabel, ylabel_a, ylabel_q
