import catboost
from catboost.core import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from catboost import CatBoostRegressor
import numpy as np
import pickle

player_name = sys.argv[1] 
opponent_team = sys.argv[2] 

# Define feature columns and label
df=pd.read_csv('C:/Users/Anurag/Desktop/cricket/hack-a-sol/server/preprocessing_data.csv')
X = df.drop(columns=["Runs_Scored","Team2","Player_name","Team1"])
y = df["Runs_Scored"]

label_encoder = LabelEncoder()
# Encode categorical features, if necessary
for column in X.select_dtypes(include=['object']).columns:
    X[column] = label_encoder.fit_transform(X[column])
with open('/home/modiji/Balls/hack-a-sol/server/predict_score.pickle','rb') as f:
    mod=pickle.load(f)
X_train=np.array(X.iloc[:38000,:])
y_train=np.array(y.iloc[:38000])
X_test=np.array(X.iloc[38000:,:])
df.iloc[38000:,:].to_csv("loda.csv")
y_test=np.array(y.iloc[38000:])
filtered_x_test = X_test[np.array(df.iloc[38000:,:][((df.iloc[38000:,:]['Player_name'] == player_name) & (df.iloc[38000:,:]['Team2'] == opponent_team)) | ((df.iloc[38000:,:]['Player_name'] == player_name) & (df.iloc[38000:,:]['Team1'] == opponent_team))].index-38000)]
filtered_y_test = y_test[np.array(df.iloc[38000:,:][((df.iloc[38000:,:]['Player_name'] == player_name) & (df.iloc[38000:,:]['Team2'] == opponent_team)) | ((df.iloc[38000:,:]['Player_name'] == player_name) & (df.iloc[38000:,:]['Team1'] == opponent_team))].index-38000)]
filtered_x_train = X_train[np.array(df.iloc[:38000,:][((df.iloc[:38000,:]['Player_name'] == player_name) & (df.iloc[:38000,:]['Team2'] == opponent_team)) | ((df.iloc[:38000,:]['Player_name'] == player_name) & (df.iloc[:38000,:]['Team1'] == opponent_team))].index)]
filtered_y_train = y_train[np.array(df.iloc[:38000,:][((df.iloc[:38000,:]['Player_name'] == player_name) & (df.iloc[:38000,:]['Team2'] == opponent_team)) | ((df.iloc[:38000,:]['Player_name'] == player_name) & (df.iloc[:38000,:]['Team1'] == opponent_team))].index)]
fined_tuned_mod = catboost.CatBoostRegressor()
fined_tuned_mod.fit(filtered_x_train,filtered_y_train,init_model=mod,verbose = False)
y_pred = fined_tuned_mod.predict(filtered_x_test)  # Make predictions
print(int(y_pred[0]))

