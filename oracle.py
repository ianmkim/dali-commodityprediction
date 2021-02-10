import pandas as pd
import numpy as np

import pickle
from sklearn.preprocessing import MinMaxScaler

import joblib

from keras.models import load_model,Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint

# dict that holds different model names
model_sizes = {
    1 : "soybeanoil.h5",
    2 : "soybeanoil_20_dps.h5",
    3 : "soybeanoil_30_dps.h5",
}

# loads a trained LSTM model
def load_trained(model_filename):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape =(10, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=['accuracy'])
    model.load_weights(model_filename)
    return model

# predict the next price given the previous price list and model size
def predict_next_price(price_list, model_size):
    # get the model and if the model size is not within the size of the dict, then just use the first model
    model_filename = model_sizes[model_size]
    if model_size not in model_sizes.keys():
        model_filename=model_sizes[0]

    input_list = price_list
    # load the scaler to normalize input prices
    scaler = joblib.load("soybeanoil_scaler.save")
    model = load_trained(model_filename)
    input_list = scaler.transform(np.array(input_list).reshape(-1, 1))
    # reshape input
    X_test = np.reshape(input_list, (1, 10, 1))
    closing_price = model.predict(X_test)
    # get price instead of normalized price
    closing_price = scaler.inverse_transform(closing_price)
    return closing_price

