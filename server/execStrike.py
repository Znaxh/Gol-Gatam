import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import catboost
from catboost import CatBoostRegressor
from catboost.core import sys
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pickle


player_name = sys.argv[1] 
opponent_team = sys.argv[2] 

# def input(player,name):


# Define feature columns and label
df=pd.read_csv('/home/modiji/Balls/hack-a-sol/ml/merged_data.csv')
matching_indices = df[(df['Player_name'] == player_name) & 
                    (df['Team2'] == opponent_team)].index
df['Strike rate']=df['Runs_Scored']/df['Balls_faced']
df['Strike rate'] = df['Strike rate'].fillna(0)
df= df[~np.isinf(df['Strike rate'])]
y = df["Strike rate"]
X = df.drop(columns=["Runs_Scored","Team2","Player_name","Team1","Balls_faced",'Strike rate'])
label_encoder = LabelEncoder()

# Encode categorical features, if necessary
for column in X.select_dtypes(include=['object']).columns:
    X[column] = label_encoder.fit_transform(X[column])
with open('/home/modiji/Balls/hack-a-sol/server/strike_rate.pickle','rb') as f:
    mod=pickle.load(f)
    
X_train=np.array(X)
y_train=np.array(y)
X_test=np.array(X)
df.to_csv("loda2.csv")
y_test=np.array(y)
    
valid_indices_test = np.intersect1d(matching_indices, np.arange(len(X_test)))
valid_indices_train = np.intersect1d(matching_indices, np.arange(len(X_train)))
    #fined_tuned_mod=CatBoostRegressor()
fined_tuned_mod = catboost.CatBoostRegressor()
# Filter X_test and y_test using the valid indices
filtered_x_test = X_test[valid_indices_test]
filtered_y_test = y_test[valid_indices_test]

# Filter X_train and y_train using the valid indices
filtered_x_train = X_train[valid_indices_train]
filtered_y_train = y_train[valid_indices_train]
if len(filtered_y_train)!=0:
    fined_tuned_mod.fit(filtered_x_train,filtered_y_train,init_model=mod,verbose=False)
    y_pred = fined_tuned_mod.predict(filtered_x_test)  # Make predictions
    mse = mean_squared_error(filtered_y_test, y_pred)  # Calculate Mean Squared Error
    r2 = r2_score(filtered_y_test, y_pred)  # Calculate R^2 Score
        #print('runs',y_pred[0])
print(float(y_pred[0]))
