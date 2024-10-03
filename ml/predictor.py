import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score

import pandas as pd
df1=pd.read_csv("clear_df.csv")


def train_and_predict(df1, player_name, opponent_team, innings, over_start_number, balls_faced, venue, toss_winner, toss_decision):
    # Create a copy of df1 to avoid modifying the original DataFrame
    df_copy = df1.copy()
    
    # Encode categorical features in the entire dataset copy
    label_encoders = {}
    categorical_cols = df_copy.select_dtypes(include=['object']).columns
    
    for column in categorical_cols:
        label_encoders[column] = LabelEncoder()
        df_copy[column] = label_encoders[column].fit_transform(df_copy[column])
    
    # Filter the DataFrame based on player_name and opponent_team
    filtered_df = df_copy[(df_copy['Player_name'] == label_encoders['Player_name'].transform([player_name])[0]) &
                          (df_copy['Team2'] == label_encoders['Team2'].transform([opponent_team])[0])]
    
    # Sort the filtered DataFrame in descending order based on 'Runs_Scored'
    filtered_df = filtered_df.sort_values(by='Runs_Scored', ascending=False)
    
    # Drop columns that are not needed
    columns_to_remove = ['Player_name', 'Team2','Winner','Team1']
    filtered_df = filtered_df.drop(columns=columns_to_remove)
    
    # Define feature columns and label
    X = filtered_df.drop(columns=["Runs_Scored"])
    y = filtered_df["Runs_Scored"]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the Logistic Regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Logistic Regression - MSE: {mse:.4f}, R^2: {r2:.4f}")

    # Display feature importance
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': model.coef_[0]
    }).sort_values(by='Coefficient', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Prepare input data for prediction
    input_data = pd.DataFrame({
        'Innings': [innings],
        'Over_start_number': [over_start_number],
        'Balls_faced': [balls_faced],
        'Venue': [venue],
        'Toss_winner': [toss_winner],
        'Toss_decision': [toss_decision]
    })
    
    # Ensure all required columns are present in input_data
    for column in X.columns:
        if column not in input_data.columns:
            input_data[column] = 0  # Use a default value or handle as appropriate
    
    # Encode categorical features in input data
    for column in input_data.select_dtypes(include=['object']).columns:
        if column in label_encoders:
            input_data[column] = label_encoders[column].transform(input_data[column])
        else:
            raise ValueError(f"Unexpected categorical column: {column}")
    
    # Ensure input_data has the same columns and order as X_train
    input_data = input_data[X.columns]
    
    # Predict Runs_Scored based on the input data
    prediction = model.predict(input_data)
    
    return prediction[0]

# Example usage
# result = train_and_predict(df1, 'MS Dhoni', 'Pakistan', 1, 3, 10, '"Brisbane Cricket Ground', 'Australia', 'bat')
# print(f"Predicted Runs Scored: {result}")
