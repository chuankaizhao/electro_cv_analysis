import pandas as pd
import numpy  as np

MOVING_WINDOW_SIZE = 3

def parse_input(args):
    try:
        df = pd.read_excel(args.input, header=None)
        print("Successfully read the input file ...")
    except:
        print(f"Error: Loading {args.input} failed!")
        
    inputData  = []
    smoothData = []
    
    currs = list(args.current)
    volts = list(args.voltage)
        
    for i, _ in enumerate(currs):
        curr, volt = currs[i], volts[i]
        
        curr_row, curr_col = int(curr[1:]), ord(curr[0].upper()) - ord('A')
        volt_row, volt_col = int(volt[1:]), ord(volt[0].upper()) - ord('A')        
        curr_data = df.loc[curr_row:, [curr_col]].to_numpy().transpose()[0]
        volt_data = df.loc[volt_row:, [volt_col]].to_numpy().transpose()[0]
        inputData.append([volt_data, curr_data])
        
        if i == 0:
            xlabel = list(df.loc[volt_row-1, [volt_col]])[0]
            ylabel = list(df.loc[curr_row-1, [curr_col]])[0]
        
        if args.smooth:
            curr_row, curr_col = int(curr[1:]), ord(curr[0].upper()) - ord('A')
            volt_row, volt_col = int(volt[1:]), ord(volt[0].upper()) - ord('A')
            curr_data = df.loc[curr_row:, [curr_col]].rolling(MOVING_WINDOW_SIZE, min_periods=1, 
                                                              center=True).mean().to_numpy().transpose()[0]
            volt_data = df.loc[volt_row:, [volt_col]].rolling(MOVING_WINDOW_SIZE, min_periods=1,
                                                              center=True).mean().to_numpy().transpose()[0]
            smoothData.append([volt_data, curr_data])
    
    print("Successfully processed the current and voltage data ...")
        
    return np.array(inputData), np.array(smoothData), xlabel, ylabel