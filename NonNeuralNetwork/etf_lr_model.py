## Linear RegressionModel Trained on CSVs generated through ETF data loader script

# Possible import of other Linear Regression scripts

# DS imports
import pandas as pd
import numpy as np
import os

# sklearn 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler    

# Evaluation Metrics
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score,
    roc_curve,
    precision_score,
    recall_score,
    f1_score
)

# Indicate CSV path from folder of generated ETF historical data
hist_path = 'NonNeuralNetwork/etf_historical/AAPL_hist.csv'

# Attempt access and read of CSV file
try:
    dframe = pd.read_csv(hist_path)
except FileNotFoundError:
    print ("Error: No suitable .csv found at " + hist_path)
    exit()

# Assumes successful read of CSV file; print head and proceed
print ("CSV accessed and read from: " + hist_path)
print (dframe.head())


# Preprocessing

# No assignment needed, headers and features labeled

## Key To Implementation
# Stocks are time series data thus
# 1. Data should be ordered, no shuffling or randomization
# 2. Label/Target is next day's closing price, thus model should be trained on previous closing price and predict future closing price

# Modify dataframe to use previous day's feature data to predict current or "future" closing price
lagged_frame = pd.DataFrame()
lagged_frame['Prev_Open'] = dframe['Open'].shift(1)
lagged_frame['Prev_High'] = dframe['High'].shift(1)
lagged_frame['Prev_Low'] = dframe['Low'].shift(1)
lagged_frame['Prev_Close'] = dframe['Close'].shift(1)
lagged_frame['Prev_Volume'] = dframe['Volume'].shift(1)

# Extract label, the closing price
label = dframe['Close']

#Concatenate lagged features with label into new dataframe
time_series_frame = lagged_frame.copy()                     # New dataframe first gets lagged features
time_series_frame['Close'] = label                          # Label column is added in its entirety
time_series_frame = time_series_frame.dropna()              # Indices with NaN feature values dropped to unify data frame dimensions

# Save time series dataframe to CSV for reference
time_series_frame.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\time_series_frame' + '\\' 'time_series_AAPL.csv')

# Assign closing price as label
X = time_series_frame.drop('Close', axis = 1)                         # Features/Training data includes all columns of feature values except for label and timestamp; indicates features are arranged by column
y = time_series_frame['Close']                                        # Label/Target data is closing price shifted by -1 to predict next day's closing price  

# Split data into training and testing sets
X_learn, X_test, y_learn, y_test = train_test_split(X, y, train_size = 0.7, shuffle = False)       # Splits data by percentage into training and evaluation, toggles off shuffling to maintain time series order

# Scale features, large values involved including volume
scale = StandardScaler()
X_learn_scaled = scale.fit_transform(X_learn) 
X_test_scaled = scale.transform(X_test)

# Initialize model instance and train model on scaled feature set
lin_model = LinearRegression()
lin_model.fit(X_learn_scaled, y_learn)

# Training finished, evaluate model against test set
y_predicted = lin_model.predict(X_test_scaled)

# Test labels and predicted labels dataframe
label_eval_frame = pd.DataFrame()
label_eval_frame['Actual_Close'] = y_test
label_eval_frame['Predicted_Close'] = y_predicted

# Save dataframe to CSV for reference
label_eval_frame.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\label_eval' + '\\' 'label_eval_AAPL.csv')

# Echo evaluation metrics

# Direct comparison; predicted vs. actual value of test indices
print("\n Test Label Values") 
for i in range(len(y_test)):
    print(f" ({i}) Actual Closing Price: {y_test.iloc[i]} || Predicted Closing Price: {y_predicted[i]}")