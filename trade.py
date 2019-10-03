import pandas as pd
import matplotlib as plt
import datetime as time
import datetime
import time
import fxcmpy
from agent.agent import Agent
from functions import *
import sys
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import keras
from keras.models import load_model

con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='demo')

model = load_model("models/" + 'model_ep0')
window_size = model.layers[0].input.shape.as_list()[1]

batch_size = 32
x = getStockDataVec('EUR')

agent = Agent(window_size, False, 'model_ep0')
state = getState(x[-2:], 0, window_size + 1)

total_profit = 0
agent.inventory = []

current = datetime.datetime.now().minute
while True:
	


	if datetime.datetime.now().minute != current:
		current = datetime.datetime.now().minute
		data2= con.get_candles('EUR/USD', period='m1', number=1)
		data2=preprocess(data2)
		with open('data/EUR.csv', 'a', newline='') as f:
			data2.to_csv(f, mode='a', index= False,header=f.tell()==0)
		x = getStockDataVec('EUR')
		for t in range(1):
			action = agent.act(state)

			# sit
			next_state = getState(x[-3:], t + 1, window_size + 1)
			reward = 0

			if action == 1: # buy
				agent.inventory.append(x[-(t+1)])
				order = con.create_market_buy_order('EUR/USD', 1)
				print ("Buy: " + formatPrice(x[-(t+1)]))

			elif action == 2 and len(agent.inventory) > 0: # sell
				bought_price = agent.inventory.pop(0)
				reward = max(x[-(t+1)] - bought_price, 0)
				total_profit += x[-(t+1)] - bought_price
				con.close_all_for_symbol('EUR/USD')
				print ("Sell: " + formatPrice(x[-(t+1)]) + " | Profit: " + formatPrice(x[-(t+1)] - bought_price))


			#     done = True if t == l - 1 else False
			done= False
			agent.memory.append((state, action, reward, next_state,done))
			state = next_state

			if done:
				print ("--------------------------------")
				print ('EUR' + " Total Profit: " + formatPrice(total_profit))
				print ("--------------------------------")

			if len(agent.memory) > batch_size:
				agent.expReplay(batch_size) 
