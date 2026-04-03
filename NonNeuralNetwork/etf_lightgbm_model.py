## LightGBM Model Trained on CSVs generated through ETF data loader script

# Possible import of other LightGBM scripts

# DS imports
import pandas as pd
import numpy as np

# LightGBM
import lightgbm as lgb

#sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit     # Stock Prediction Must Use Time-Series Split

# Evaluation Metrics

# CSV Path to access histrical data
hist_path = r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\etf_historical\ASTS_hist.csv'

# Attempt to access and read CSV onto dataframe
try: 
    dframe = pd.read_csv(hist_path)
except FileNotFoundError:
    print ("Error: No suitable .csv found at " + hist_path)
    exit()

# Given successful access 
print ("CSV accessed successfully from: " + hist_path)
print (dframe.head())

# Dataframe Preprocessing

# Lag features back one time unit such that model is predicting next day closing price
lagged_frame = pd.DataFrame()               # New DataFrame with lagged features
lagged_frame['Prev_Open'] = dframe['Open'].shift(1)
lagged_frame['Prev_High'] = dframe['High'].shift(1)
lagged_frame['Prev_Low'] = dframe['Low'].shift(1)
lagged_frame['Prev_Close'] = dframe['Close'].shift(1)
lagged_frame['Prev_Volume'] = dframe['Volume'].shift(1)

label = dframe['Close']                    # Assign Closing Price as Label, no shift

# Recombine shifted features and centered label
time_series_frame = lagged_frame.copy()
time_series_frame['Close'] = label
time_series_frame = time_series_frame.dropna()         # Drop indices with null values created from shifting

# Save preprocessed CSV
#time_series_frame.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\time_series_frame' + '\\' 'time_series_RGTI-1.csv')

# Model Training Configuration
X = time_series_frame.drop('Close', axis = 1)     # Drop Closing price as feature
y = time_series_frame['Close']

# Split training and evaluation data
X_learn, X_test, y_learn, y_test = train_test_split(X,y, train_size = 0.8, shuffle = False)

# Scale features, normalize large values; attempt to train without scaled data
scale = StandardScaler()
#X_learn_scaled = scale.fit_transform(X_learn)
#X_test_scaled = scale.transform(X_test)

# Test/Evaluation Data Prepared; Initialize Model
lgb_model = lgb.LGBMRegressor(
    objective = 'regression',
    n_estimators = 200,
    learning_rate = 0.025,
    num_leaves = 256,
    min_child_samples = 2,

    )

# Hyperparameters
lgb_model.set_params (
    boosting_type='gbdt'
)

# Train Model on training set
lgb_model.fit(X_learn, y_learn)

# Evaluate Model using test after training
y_predicted = lgb_model.predict(X_test) 

## Performance Evaluation

# Direct Comparison
lgb_eval_frame = pd.DataFrame()
lgb_eval_frame['Actual_Close'] = y_test
lgb_eval_frame['Predicted_Close'] = y_predicted

# Store evalation dataframe to CSV
lgb_eval_frame.to_csv (r'C:\Users\merc1\OneDrive\Stock_Pred_ML\NonNeuralNetwork\label_eval' + '\\' 'lgb_eval_ASTS-1.csv')

# Echo Direct Comparison

# Direct comparison; predicted vs. actual value of test indices (LightGBM)
print("\n Test Label Values") 
for i in range(len(y_test)):
    print(f" ({i}) Actual Closing Price: {y_test.iloc[i]} || Predicted Closing Price: {y_predicted[i]}")