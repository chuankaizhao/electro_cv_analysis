# electro_cv_analysis
Visualize and analyze electrochemical current–voltage curve 

### Dependencies
The following dependencies are used, which can be installed via conda/pip:
<pre>
numpy 
pandas
matplotlib
peakutils
</pre>

### Usage

<pre>

usage: python main.py

optional arguments in inputfile.txt:

input="0.1M KOH NO BA Processed Data.xlsx"     # input excel file name
output="0.1M_KOH_NO_BA"                        # output file name
current=['B12', 'H12']                         # current columns in excel
current_area=['D12', 'J12']                    # current/area columns in excel
voltage=['C12', 'I12']                         # voltage columns
perform_smooth=true                            # perform curve smoothing 
perform_analysis=true                          # perform peak and integration analysis
plot_curve_compare=false                       # plot both original and smooth curve to compare smoothing effect
# Addtional tuning of plot_args
# {"xlim":[0.1, 0.5], "ylim":[-0.2, 0.7], "xlabel":"test1", "ylabel":"test2", "legends":["0.1M KOH NO BA", "0.2M KOH NO BA"]}
# CV curve normalized by area
plot_args_a={"xlabel":"E - iRu (V vs RHE)", "legends":["cycle 1", "cycle 2"]}  
# CV curve normalized by q
plot_args_q={"xlabel":"E - iRu (V vs RHE)", "legends":["cycle 1", "cycle 2"]}      
# System specific parameters
molecular_weight=58.6934                       # molecular weight of catalyst: unit g/mol
  
</pre>
