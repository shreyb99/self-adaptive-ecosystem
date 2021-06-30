import pandas as pd
import numpy as np
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import tensorflow as tf
from datetime import datetime

dataset = pd.read_csv('D:\ML Datasets\household_power_consumption.txt', parse_dates={'dt' : ['Date', 'Time']}, infer_datetime_format=True, index_col= 0, na_values=['nan','?'], sep=';')

dataset.fillna(0, inplace=True)
values = dataset.values
# ensure all data is float
values = values.astype('float32')

# normalizing input features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
scaled = pd.DataFrame(scaled)

def create_ts_data(dataset, lookback=1, predicted_col=1):
    temp=dataset.copy()
    temp["id"]= range(1, len(temp)+1)
    temp = temp.iloc[:-lookback, :]
    temp.set_index('id', inplace =True)
    predicted_value=dataset.copy()
    predicted_value = predicted_value.iloc[lookback:,predicted_col]
    predicted_value.columns=["Predcited"]
    predicted_value= pd.DataFrame(predicted_value)
    
    predicted_value["id"]= range(1, len(predicted_value)+1)
    predicted_value.set_index('id', inplace =True)
    final_df= pd.concat([temp, predicted_value], axis=1)
    #final_df.columns = ['var1(t-1)', 'var2(t-1)', 'var3(t-1)', 'var4(t-1)', 'var5(t-1)', 'var6(t-1)', 'var7(t-1)', 'var8(t-1)','var1(t)']
    #final_df.set_index('Date', inplace=True)
    return final_df

reframed_df= create_ts_data(scaled, 1,0)
reframed_df.fillna(0, inplace=True)
reframed_df.columns = ['var1(t-1)', 'var2(t-1)', 'var3(t-1)', 'var4(t-1)', 'var5(t-1)', 'var6(t-1)', 'var7(t-1)','var1(t)']
# display(reframed_df.head(4))

y=reframed_df['var1(t)']
X=reframed_df.drop(['var1(t)'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print("X_train.shape: ", X_train.shape)
print("y_train.shape: ", y_train.shape)
print("X_test.shape: ", X_test.shape)
print("y_test.shape: ", y_test.shape) 

# reshape input to be 3D [samples, time steps, features]
X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

lstm_model = Sequential()
lstm_model.add(LSTM(75, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
lstm_model.add(LSTM(units=30, return_sequences=True))
lstm_model.add(LSTM(units=30))
lstm_model.add(Dense(units=1))
lstm_model.compile(loss='mae', optimizer='adam')
lstm_model.summary()

history_lstm = lstm_model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test),  shuffle=False)

# Plotting Loss
pyplot.plot(history_lstm.history['loss'], label='LSTM train', color='red')
pyplot.plot(history_lstm.history['val_loss'], label='LSTM test', color= 'green')
pyplot.legend()
pyplot.show()

# make a prediction
yhat_test = lstm_model.predict(X_test)
X_test = X_test.reshape((X_test.shape[0], 7))

# invert scaling for forecast
print(yhat_test.shape, X_test.shape)
inv_yhat_test = np.concatenate((yhat_test, X_test[:, -6:]), axis=1)
print(inv_yhat_test.shape)
inv_yhat_test = scaler.inverse_transform(inv_yhat_test)
inv_yhat_test = inv_yhat_test[:,0]

# invert scaling for actual
y_test = y_test.values.reshape((len(y_test), 1))
inv_y = np.concatenate((y_test, X_test[:, -6:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]

# calculate RMSE
rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat_test))
print('Test RMSE: %.3f' % rmse)

# Compare predictions with actual values
## time steps, every step is one hour (you can easily convert the time step to the actual time index)
## for a demonstration purpose, I only compare the predictions in 200 hours. 
pyplot.figure(figsize=(12,8))
aa=[x for x in range(200)]
pyplot.plot(aa, inv_y[:200], marker='.', label="actual")
pyplot.plot(aa, inv_yhat_test[:200], 'r', label="prediction")
pyplot.ylabel('Global_active_power', size=15)
pyplot.xlabel('Time step', size=15)
pyplot.legend(fontsize=15)
pyplot.show()