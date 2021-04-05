# electro_cv_analysis
Visualize and analyze electrochemical current–voltage curve 

### Dependencies
The following dependencies are used, which can be installed via conda/pip:
Numpy 
Pandas
matplotlib
peakutils

### Usage

usage: python main.py [-h] -i INPUT -c [CURRENT [CURRENT ...]] -v
               [VOLTAGE [VOLTAGE ...]] [-ps] [-po] [-pa] [-pp PLOTARGS]
               [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        File containing I-V data.
  -c [CURRENT [CURRENT ...]], --current [CURRENT [CURRENT ...]]
                        Excel location where current data pop up: -i D12, F12
  -v [VOLTAGE [VOLTAGE ...]], --voltage [VOLTAGE [VOLTAGE ...]]
                        Excel location where voltage data pop up: -i C12, E12
  -ps, --performSmooth  Smooth CV curve
  -po, --plotOriginal   Plot both original and smoothed CV curve when smooth
                        method is used
  -pa, --performAnalysis
                        Perform analysis for peaks in CV curve
  -pp PLOTARGS, --plotProperties PLOTARGS
                        Additional arguments for making CV plot
  -o OUT, --output OUT  Name of I-V plot
  
### Example 
  python main.py -i "0.1M KOH NO BA Processed Data.xlsx" -c D12 -v C12 -ps -pa -pp "legends : 0.1M KOH NO BA"
  
  
