from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getData(data):
    # data = pd.read_csv(location)
    x = np.arange(0, len(data)).reshape(-1, 1)
    y = data.iloc[:, 5].values.reshape(-1, 1)
    return x, y

def createModel():
    lr = LinearRegression()
    return lr

def predict(model, forecast, x, y):
    forecast = 30
    for day in range(1, forecast+1):
        model.fit(x, y)
        
        x_pred = np.arange(len(x), len(x) + 1).reshape(-1, 1)
        y_pred = model.predict(x_pred)
        x = np.append(x, x_pred)
        y = np.append(y, y_pred)
        y_pred = np.delete(y_pred, 0)
        x = x.reshape(-1, 1)
    
    return x, y


def normalizeLRpredict(y, forecast, data_len):
    diffy = y[len(y)-forecast-1] - y[len(y)-forecast]
    for i in range(data_len, data_len + forecast):
        y[i] = y[i] + diffy

    return y

def plotPred(x, y, data_len):
    y_pred = y[data_len:data_len + forecast]
    x_pred = x[data_len:data_len + forecast]
    x = x[0:data_len]
    y = y[0:data_len]
    plt.plot(x, y)
    plt.plot(x_pred, y_pred)
    plt.show()


if __name__ == '__main__':
    dataloc = "../data/VTI.csv"
    forecast = 30

    x, y = getData(dataloc)
    data_len = len(x)

    model = createModel()
    x, y = predict(model, forecast, x, y)

    y = normalizeLRpredict(y, forecast, data_len)

    # plotPred(x, y, data_len)


