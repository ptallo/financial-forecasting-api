from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn import preprocessing

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Hyperparameters
BATCH_SIZE = 5
DROPOUT = 0.2
NUM_HIDDEN = 3

def create_model(BATCH_SIZE, DIMENSION_SIZE, NUM_HIDDEN=2, DROPOUT=0.5):
    model = Sequential()
    # Row length of data needed
    for i in range(0, NUM_HIDDEN):
        
        if i == 0:
            # First layer - return full sequence
            model.add(LSTM(units=50, return_sequences=True, input_shape=(1, DIMENSION_SIZE), batch_input_shape=(5, 1, DIMENSION_SIZE), stateful=True))
        elif i == NUM_HIDDEN - 1:
            # Last Layer before final fully connected - don't return full sequence
            model.add(LSTM(units=20, return_sequences=False))
        else:
            # Hidden Layers
            model.add(LSTM(units=50, return_sequences=True,))
        # Add dropout after every layer
        model.add(Dropout(DROPOUT))

    # Final fully connected layer - output is a single value
    model.add(Dense(1))

    return model



# def get_data():
# Reading in the data
data = pd.read_csv("data/VTI.csv")
data = data[:-59]


# Extracting the features we want to train on all numeric vars not close
x_train = train[['Open', 'Volume', 'Low', 'High']].copy()
y_train = train[['Close']].copy()
scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
x_train[['Open', 'Volume', 'Low', 'High']] = scaler.fit_transform(x_train[['Open', 'Volume', 'Low', 'High']])
y_train  = scaler.fit_transform(y_train)


x_test = test[['Open', 'Volume', 'Low', 'High']].copy()
y_test = test[['Close']].copy()
test[['Open', 'Volume', 'Low', 'High']] = scaler.fit_transform(x_test[['Open', 'Volume', 'Low', 'High']])
y_test  = scaler.fit_transform(y_test)

# Change to numpy arrays
x_train = x_train.to_numpy()
# y_train = y_train.to_numpy()
x_test = x_test.to_numpy()
# y_test = y_test.to_numpy()

# x_train = []
# y_train = []
# x_test = []
# y_test = []
for i in range(10, 1241):
    if i < 1200:
        x_train.append(training_set_scaled[i-10:i, 0])
        y_train.append(training_set_scaled[i, 0])
    else:
        x_test.append(training_set_scaled[i-10:i, 0])
        y_test.append(training_set_scaled[i, 0])
# Reshaping data for timeseries - steps of 1 for LSTM input
x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1]))

model = create_model(BATCH_SIZE, x_train.shape[2], NUM_HIDDEN, DROPOUT)
model.compile(loss='mean_squared_error', optimizer="adam", metrics=['accuracy'])
for i in range(0,100):
    print("Epoch # ", i)
    model.fit(x=x_train, y=y_train, epochs=1, batch_size=5, verbose=0, validation_data=(x_test, y_test), shuffle=False)
    model.reset_states()
