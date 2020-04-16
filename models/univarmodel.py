import tensorflow as tf

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from math import floor

# Matplotlib fig params
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

# Enable eager for easy to use TF
#tf.enable_eager_execution()


def univariate_data(dataset, start_index, end_index, history_size, target_size):
    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
        end_index = len(dataset) - target_size

    for i in range(start_index, end_index):
        # Every group of 20
        indices = range(i - history_size, i)
        # Reshape data from (history_size,) to (history_size, 1)
        # Data is now groups of 20 records - x data
        data.append(np.reshape(dataset[indices], (history_size, 1)))
        # Labels = the day to predict in question - y data
        labels.append(dataset[i + target_size])
    return np.array(data), np.array(labels)


def getData(location):
    # Get the data into pandas df
    data = pd.read_csv(location)

    # Univariate data for close indexed on data -> numpy array
    uni_data = data.iloc[:, 5]
    uni_data.index = data['Date']
    uni_data = uni_data.values

    return uni_data


def normalizeData(TRAIN, uni_data):
    # Getting training data metrics
    uni_train_min = np.amin(uni_data[:TRAIN])
    uni_train_max = np.amax(uni_data[:TRAIN])
    uni_data = (uni_data - uni_train_min) / uni_train_max

    return uni_data, uni_train_min, uni_train_max


def trainValSplit(uni_data, TRAIN, HISTORIC_REC, TARGET_REC):
    # This will be:
    # x = previous records
    # y = next record prediction
    x_train_uni, y_train_uni = univariate_data(uni_data, 0, TRAIN,
                                               HISTORIC_REC,
                                               TARGET_REC)

    x_val_uni, y_val_uni = univariate_data(uni_data, TRAIN, None,
                                           HISTORIC_REC,
                                           TARGET_REC)

    return x_train_uni, y_train_uni, x_val_uni, y_val_uni


def create_time_steps(length):
    return list(range(-length, 0))


def show_plot(plot_data, delta, title):
    labels = ['History', 'True Future', 'Model Prediction']
    marker = ['.-', 'rx', 'go']
    time_steps = create_time_steps(plot_data[0].shape[0])
    if delta:
        future = delta
    else:
        future = 0

    plt.title(title)
    for i, x in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10,
                     label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], (future + 5) * 2])
    plt.xlabel('Time-Step')
    return plt


def showSampleExample(x_train_uni, y_train_uni, val):
    plot = show_plot([x_train_uni[val], y_train_uni[val]], 0, 'Sample Example')
    plt.show()


def baseline(history):
    return np.mean(history)


def showBaselinePrediction(x_train_uni, y_train_uni, val):
    plot = show_plot([x_train_uni[val], y_train_uni[val], baseline(x_train_uni[val])], 0,
                     'Baseline Prediction Example')
    plt.show()


def batchAndShuffleData(BUFFER_SIZE, BATCH_SIZE, x_train_uni, y_train_uni, x_val_uni, y_val_uni):
    train_univariate = tf.data.Dataset.from_tensor_slices((x_train_uni, y_train_uni))
    train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True).repeat()

    val_univariate = tf.data.Dataset.from_tensor_slices((x_val_uni, y_val_uni))
    val_univariate = val_univariate.batch(BATCH_SIZE, drop_remainder=True).repeat()

    return train_univariate, val_univariate


def createModel(tensorShape):
    simple_lstm_model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(8, input_shape=tensorShape),
        tf.keras.layers.Dense(1)
    ])

    simple_lstm_model.compile(optimizer='adam', loss='mae')

    return simple_lstm_model


# for x, y in val_univariate.take(1):
#     print(simple_lstm_model.predict_on_batch(x).shape)

##### 2
def CreateModel(train_data_shape):
    model = createModel(train_data_shape[-2:])

    return model


##### 1
def PrepTrainData(location):
    HISTORIC_REC = 30
    TARGET_REC = 0
    BATCH_SIZE = 1
    BUFFER_SIZE = 200

    data = getData(location)
    TRAIN = floor(0.8 * len(data))

    ndata, nmin, nmax = normalizeData(TRAIN, data)
    x_train_uni, y_train_uni, x_val_uni, y_val_uni = trainValSplit(ndata, TRAIN, HISTORIC_REC, TARGET_REC)
    train_univariate, val_univariate = batchAndShuffleData(BUFFER_SIZE, BATCH_SIZE, x_train_uni, y_train_uni, x_val_uni, y_val_uni)

    return train_univariate, val_univariate, x_train_uni.shape


#### 3
def TrainModel(model, train_univariate, val_univariate):
    EVALUATION_INTERVAL = 200
    EPOCHS = 100
    model.fit(train_univariate, epochs=EPOCHS,
              steps_per_epoch=EVALUATION_INTERVAL,
              validation_steps=50,
              validation_data=val_univariate)

    model.save("trained/trained_model")

    return model


def LoadModel(m_name):
    model = tf.keras.models.load_model(m_name)
    return model


def GetPrediction(dataset, model, forecast):
    if forecast > 30:
        forecast = 30

    data = getData(dataset)
    # plt.plot(data)
    hdata, nmin, nmax = normalizeData(len(data), data)
    hdata = hdata[-30:]
    # hdata = data.reshape(1, 30, 1)

    # p_y = x_val_uni[-1]
    p_ya = np.array([])
    p_x = np.arange(len(data), len(data) + forecast)

    for x in range(0, forecast):
        hdata = hdata.reshape(1, 30, 1)
        y_hat = model.predict(hdata)

        hdata = np.append(hdata, y_hat)
        hdata = np.delete(hdata, 0)
        p_ya = np.append(p_ya, y_hat)

    p_ya = p_ya * nmax + nmin
    diffy = data[-1] - p_ya[0]
    p_ya = p_ya + diffy
    # plt.plot(p_x, p_ya)

    # plt.show()

    return p_ya


# t_m = LoadModel('trained/trained_model')
# GetPrediction('../data/AAPL.csv', t_m, 20)


def TrainSet():
    model = CreateModel((30, 1))
    for filename in os.listdir('../data'):
        if filename.endswith(".csv"):
            print('../data/' + filename)
            train, val, t_shape = PrepTrainData('../data/' + filename)
            model = TrainModel(model, train, val)
