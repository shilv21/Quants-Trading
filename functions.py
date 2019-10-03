import numpy as np
import math
import fxcmpy
import datetime as time
import datetime
import time

# prints formatted price
def formatPrice(n):
	return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

# returns the vector containing stock data from a fixed file
def getStockDataVec(key):
	vec = []
	lines = open("data/" + key + ".csv", "r").read().splitlines()

	for line in lines[1:]:
		vec.append(float(line.split(",")[4]))

	return vec

# returns the sigmoid
def sigmoid(x):
	try:
		if x < 0:
			return 1 - 1 / (1 + math.exp(x))
		return 1 / (1 + math.exp(-x))
	except OverflowError as err:
		print("Overflow err: {0} - Val of x: {1}".format(err, x))
	except ZeroDivisionError:
		print("division by zero!")
	except Exception as err:
		print("Error in sigmoid: " + err)
	

# returns an an n-day state representation ending at time t
def getState(data, t, n):
	d = t - n + 1
	block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
	res = []
	for i in range(n - 1):
		res.append(sigmoid(block[i + 1] - block[i]))

	return np.array([res])

#Preprocess data
def preprocess(df):
    if df.shape[1]==9: df.reset_index(inplace=True)
    df = df.drop(columns=['askopen','askclose','askhigh','asklow'])
    df.rename(columns={'date':'Date','bidopen':'Open','bidclose':'Close','bidhigh':'High','bidlow':'Low','tickqty':'Volume'})
    # df['Adj Close']= df['Close']-40
    df.columns=(['Date','Open','High','Low','Close','Volume'])
    return df

#Automated update data
def updateAuto():
	current= datetime.datetime.now().minute
	con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='demo')
	while True:
		time.sleep(5)
		if datetime.datetime.now().minute != current:
			current = datetime.datetime.now().minute
			data2= con.get_candles('BTC/USD', period='m1', number=1)
			data2=preprocess(data2)
			print(current)
			with open('data/BTC.csv', 'a', newline='') as f:
				data2.to_csv(f, mode='a', index= False,header=f.tell()==0)
		else: continue