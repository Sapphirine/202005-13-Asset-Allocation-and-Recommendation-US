import pickle
from datetime import datetime
import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.dates as mdate
import matplotlib.dates as mdates


def get_data(stock_name):
    """ Returns a 3 x n_step array """
    data = pd.read_csv('data/{}.csv'.format(stock_name)).drop(columns="DateTime")
    data = np.array(data.T)
    return data


def get_scaler(env):
    """ Takes a env and returns a scaler for its observation space """
    low = [0] * (env.n_stock * 2 + 1)

    high = []
    max_price = env.stock_price_history.max(axis=1)
    min_price = env.stock_price_history.min(axis=1)
    max_cash = env.init_invest * 3  # 3 is a magic number...
    max_stock_owned = max_cash // min_price
    for i in max_stock_owned:
        high.append(i)
    for i in max_price:
        high.append(i)
    high.append(max_cash)

    scaler = StandardScaler()
    scaler.fit([low, high])
    return scaler


def maybe_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def buy_and_hold_benchmark(stock_name, init_invest, test):
    df = pd.read_csv('./data/{}.csv'.format(stock_name)).iloc[test:, :]
    dates = df['DateTime'].astype("str")
    per_num_holding = init_invest // 79
    num_holding = per_num_holding // df.iloc[0, 1:]
    balance_left = init_invest % 79 + ([per_num_holding for _ in range(79)] % df.iloc[0, 1:]).sum()
    buy_and_hold_portfolio_values = (df.iloc[:, 1:] * num_holding).sum(axis=1) + balance_left
    buy_and_hold_return = buy_and_hold_portfolio_values.iloc[-1] - init_invest
    return dates, buy_and_hold_portfolio_values, buy_and_hold_return


def plot_all(stock_name, daily_portfolio_value, env, test):
    """combined plots of plot_portfolio_transaction_history and plot_portfolio_performance_comparison"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 4), dpi=100)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    dates, buy_and_hold_portfolio_values, buy_and_hold_return = buy_and_hold_benchmark(stock_name, env.init_invest,
                                                                                       test)
    ax.set_title('fAPV of DQN Method')
    dates = [datetime.strptime(d, '%Y%m%d').date() for d in dates]
    ax.plot(dates, daily_portfolio_value, color='red',
            label='DQN')
    # ax.plot(dates, buy_and_hold_portfolio_values, color='blue', label='Buy and Hold')
    ax.set_ylabel('Portfolio Value (USD)')

    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
    # plt.xticks(pd.date_range('2019-01-05', '2019-12-31', freq='1m'))
    plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) 
    ax.legend()
    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(hspace=0.5)
    plt.show()

'''
def visualize_portfolio_val():
    """ visualize the portfolio_val file """
    with open('portfolio_val/201912141307-train.p', 'rb') as f:
        data = pickle.load(f)
    with open('portfolio_val/201912042043-train.p', 'rb') as f:
        data0 = pickle.load(f)
    print(sum(data) / 4000)
    print('data>>>', len(data))
    fig, ax = plt.subplots(2, 1, figsize=(16, 8), dpi=100)

    ax[0].plot(data0, linewidth=1)
    ax[0].set_title('DQN Training Performance: 2000 episodes', fontsize=24)
    ax[0].set_xlabel('episode', fontsize=24)
    ax[0].set_ylabel('final portfolio value', fontsize=24)
    ax[0].tick_params(axis='both', labelsize=12)

    ax[1].plot(data, linewidth=1)
    ax[1].set_title('DQN Training Performance: 4000 episodes', fontsize=24)
    ax[1].set_xlabel('episode', fontsize=24)
    ax[1].set_ylabel('final portfolio value', fontsize=24)
    ax[1].tick_params(axis='both', labelsize=12)

    plt.show()
'''