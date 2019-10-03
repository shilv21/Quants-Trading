import pandas as pd
import matplotlib as plt
import datetime as time
import datetime
import time
import fxcmpy
import sys
from functions import *

try:
    if len(sys.argv) != 2:
        print ("Usage: python fxcm.py [stock]")
        exit()

    stock_name= sys.argv[1]
    # Connect to FXCM broker plarform
    con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='demo')
    # Create a dataset
    data = con.get_candles(stock_name, period='m5', number=2500)
    #Preprocess data
    data = preprocess(data)
    #Save to csv file
    data.to_csv('data/'+ stock_name.split('/')[0] +'.csv',index= False)

except Exception as e:
	print("Error occured: {0}".format(e))
finally:
	exit()
