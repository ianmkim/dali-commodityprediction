import pandas as pd
import numpy as np

import pickle
from sklearn.preprocessing import MinMaxScaler

import joblib

from keras.models import load_model,Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint

def load_trained(model_filename):
    #model_filename = "soybeanoil.h5"
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape =(10, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=['accuracy'])
    model.load_weights(model_filename)
    return model

def predict_next_price(price_list, model_size):
    if model_size == 1:
        model_filename = "soybeanoil.h5"
    elif model_size == 2:
        model_filename = "soybeanoil_20_dps.h5"
    elif model_size == 3:
        model_filename = "soybeanoil_30_dps.h5"

    input_list = price_list
    scaler = joblib.load("soybeanoil_scaler.save")
    model = load_trained(model_filename)
    input_list = scaler.transform(np.array(input_list).reshape(-1, 1))
    X_test = np.reshape(input_list, (1, 10, 1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    return closing_price

