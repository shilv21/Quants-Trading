# Quantitative trading

## Overview 
### Begin from the scratch, there are 4 problems which require to solve:
* Which data will be used for the project: prices, chart of prices or pictures of group of single price.
* The way to preprocess the data.
* Which model will be suitable for predicting the future trend of stock or forein exchange.
* Applying it to a platform to make an automated trading system.

In order to approach the resolution, I try to make a simple prediction based on the Moving average and leading to apply LSTM model.
![](https://i.imgur.com/MElYnV8.png)
And in the advanced step, LTSM model made the prediction more effective with the entry points.
![](https://i.imgur.com/5Os7oqe.png)

But It was quite hard to define the entry point with high frequency trading. So I continue to solve the problem with Reinforcement learning. It seems more suitable for predict entry point and out point more accurate and faster. These are some backtest.
![](https://i.imgur.com/tc8slq0.png)
![](https://i.imgur.com/Lb38it0.png)


## Deploy model
I chose FXCM trading station for trading purpose. You can download the platform on this link [FXCM](https://www.fxcm.com/uk/platforms/trading-station/download/).

## Running the Code
To train the model, download a training and test csv files from Platform.

mkdir models
python train.py [stock_name]

Then when training finishes (minimum 200 episodes for results):

python evaluate.py [stock_name] [model_name]


## References
[Deep Q-Learning with Keras and Gym](https://keon.io/deep-q-learning/)- Q-learning overview and Agent skeleton code




