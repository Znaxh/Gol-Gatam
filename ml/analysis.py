import pandas as pd
df=pd.read_csv("merged_data.csv")

import pandas as pd
import matplotlib.pyplot as plt

def plot_player_strike_rate(df: pd.DataFrame, player_name: str, team2_name: str = None):
    """
    Plot the strike rate for a given player across different dates. Optionally, filter by opponent team.
    Applies binning by resampling the data if team2_name is not provided. Enhances UI with background color and styling.

    Parameters:
    - df: DataFrame containing the cricket data.
    - player_name: The name of the player.
    - team2_name: The name of the opponent team (optional).

    Returns:
    - None: Displays a plot of strike rate over time.
    """
    # Filter the DataFrame based on player name and optionally team
    if team2_name:
        filtered_df = df[(df['Player_name'] == player_name) & (df['Team2'] == team2_name)]
    else:
        filtered_df = df[df['Player_name'] == player_name]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player and team (if specified).")
        return

    # Ensure 'Date' column is in datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    # Group by date and calculate strike rate
    grouped_df = filtered_df.groupby('Date').agg({
        'Runs_Scored': 'sum',
        'Balls_faced': 'sum'
    }).reset_index()

    # Calculate strike rate
    grouped_df['Strike_Rate'] = (grouped_df['Runs_Scored'] / grouped_df['Balls_faced']) * 100

    # Apply binning by resampling if team2_name is not specified
    if not team2_name:
        # Set 'Date' as index
        grouped_df.set_index('Date', inplace=True)
        # Resample to monthly frequency and aggregate
        resampled_df = grouped_df.resample('M').agg({
            'Runs_Scored': 'sum',
            'Balls_faced': 'sum'
        }).dropna()

        # Calculate strike rate for resampled data
        resampled_df['Strike_Rate'] = (resampled_df['Runs_Scored'] / resampled_df['Balls_faced']) * 100

        # Interpolate missing values
        resampled_df.interpolate(method='linear', inplace=True)

        resampled_df.reset_index(inplace=True)
        grouped_df = resampled_df

    # Plot the strike rate
    plt.figure(figsize=(14, 7))
    plt.plot(grouped_df['Date'], grouped_df['Strike_Rate'], marker='o', linestyle='-', color='b', markersize=8, linewidth=2)
    plt.title(f'Strike Rate of {player_name} Over Time' + (f' Against {team2_name}' if team2_name else ''), fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Strike Rate', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set background colors
    plt.gca().set_facecolor('#f0f0f0')  # Light grey background for the plot area
    plt.gcf().set_facecolor('#ffffff')  # White background for the figure
    
    # Improve layout and aesthetics
    plt.tight_layout()
    plt.show()

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
#plot_player_strike_rate(df, 'MS Dhoni', 'Pakistan')  # With team2_name
#plot_player_strike_rate(df, 'MS Dhoni')  # Without team2_name

import pandas as pd
import matplotlib.pyplot as plt

def plot_player_runs_scored(df: pd.DataFrame, player_name: str, team2_name: str = None):
    """
    Plot the runs scored for a given player across different dates. Optionally, filter by opponent team.
    Applies binning by resampling the data if team2_name is not provided. Enhances UI with background color and styling.

    Parameters:
    - df: DataFrame containing the cricket data.
    - player_name: The name of the player.
    - team2_name: The name of the opponent team (optional).

    Returns:
    - None: Displays a plot of runs scored over time.
    """
    # Filter the DataFrame based on player name and optionally team
    if team2_name:
        filtered_df = df[(df['Player_name'] == player_name) & (df['Team2'] == team2_name)]
    else:
        filtered_df = df[df['Player_name'] == player_name]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player and team (if specified).")
        return

    # Ensure 'Date' column is in datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    # Group by date and calculate runs scored
    grouped_df = filtered_df.groupby('Date').agg({
        'Runs_Scored': 'sum'
    }).reset_index()

    # Apply binning by resampling if team2_name is not specified
    if not team2_name:
        # Set 'Date' as index
        grouped_df.set_index('Date', inplace=True)
        # Resample to monthly frequency and aggregate
        resampled_df = grouped_df.resample('M').agg({
            'Runs_Scored': 'sum'
        }).dropna()

        # Interpolate missing values
        resampled_df.interpolate(method='linear', inplace=True)

        resampled_df.reset_index(inplace=True)
        grouped_df = resampled_df

    # Plot the runs scored
    plt.figure(figsize=(14, 7))
    plt.plot(grouped_df['Date'], grouped_df['Runs_Scored'], marker='o', linestyle='-', color='b', markersize=8, linewidth=2)
    plt.title(f'Runs Scored by {player_name} Over Time' + (f' Against {team2_name}' if team2_name else ''), fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Runs Scored', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set background colors
    plt.gca().set_facecolor('#f0f0f0')  # Light grey background for the plot area
    plt.gcf().set_facecolor('#ffffff')  # White background for the figure
    
    # Improve layout and aesthetics
    plt.tight_layout()
    plt.show()

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
#plot_player_runs_scored(df, 'MS Dhoni', 'Pakistan')  # With team2_name
#plot_player_runs_scored(df, 'MS Dhoni')  # Without team2_name




import pandas as pd
import matplotlib.pyplot as plt

def plot_player_strike_rate(df: pd.DataFrame, player_name: str, team2_name: str = None):
    """
    Plot the runs scored in different categories (Twos, Threes, Fours, Sixes) for a given player across different dates.
    Optionally, filter by opponent team. Applies binning by resampling the data if team2_name is not provided.
    Enhances UI with background color and styling.

    Parameters:
    - df: DataFrame containing the cricket data.
    - player_name: The name of the player.
    - team2_name: The name of the opponent team (optional).

    Returns:
    - None: Displays a plot of runs scored in different categories over time.
    """
    # Filter the DataFrame based on player name and optionally team
    if team2_name:
        filtered_df = df[(df['Player_name'] == player_name) & (df['Team2'] == team2_name)]
    else:
        filtered_df = df[df['Player_name'] == player_name]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player and team (if specified).")
        return

    # Ensure 'Date' column is in datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    # Group by date and aggregate runs scored in different categories
    grouped_df = filtered_df.groupby('Date').agg({
        'Twos': 'sum',
        'Thress': 'sum',  # Spelling mistake as per your data
        'Fours': 'sum',
        'Sixs': 'sum'    # Spelling mistake as per your data
    }).reset_index()

    # Apply binning by resampling if team2_name is not specified
    if not team2_name:
        # Set 'Date' as index
        grouped_df.set_index('Date', inplace=True)
        # Resample to monthly frequency and aggregate
        resampled_df = grouped_df.resample('M').agg({
            'Twos': 'sum',
            'Thress': 'sum',  # Spelling mistake as per your data
            'Fours': 'sum',
            'Sixs': 'sum'    # Spelling mistake as per your data
        }).dropna()

        # Interpolate missing values
        resampled_df.interpolate(method='linear', inplace=True)

        resampled_df.reset_index(inplace=True)
        grouped_df = resampled_df

    # Filter out bins where all categories are zero
    grouped_df = grouped_df[(grouped_df[['Twos', 'Thress', 'Fours', 'Sixs']].sum(axis=1) > 0)]

    # Check if there is data left to plot
    if grouped_df.empty:
        print("No data available to plot after filtering.")
        return

    # Plot the runs scored in different categories
    plt.figure(figsize=(14, 7))
    plt.plot(grouped_df['Date'], grouped_df['Twos'], marker='o', linestyle='-', color='green', markersize=8, linewidth=2, label='Twos')
    plt.plot(grouped_df['Date'], grouped_df['Thress'], marker='o', linestyle='-', color='red', markersize=8, linewidth=2, label='Threes')
    plt.plot(grouped_df['Date'], grouped_df['Fours'], marker='o', linestyle='-', color='orange', markersize=8, linewidth=2, label='Fours')
    plt.plot(grouped_df['Date'], grouped_df['Sixs'], marker='o', linestyle='-', color='purple', markersize=8, linewidth=2, label='Sixes')
    
    plt.title(f'Runs Scored by {player_name} Over Time' + (f' Against {team2_name}' if team2_name else ''), fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Runs Scored', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Set background colors
    plt.gca().set_facecolor('#f0f0f0')  # Light grey background for the plot area
    plt.gcf().set_facecolor('#ffffff')  # White background for the figure
    
    # Improve layout and aesthetics
    plt.tight_layout()
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt

def plot_player_runs(df: pd.DataFrame, player_name: str, team2_name: str = None):
    """
    Plot the runs scored in different categories (Dots, Ones) for a given player across different dates.
    Optionally, filter by opponent team. Applies binning by resampling the data if team2_name is not provided.
    Enhances UI with background color and styling.

    Parameters:
    - df: DataFrame containing the cricket data.
    - player_name: The name of the player.
    - team2_name: The name of the opponent team (optional).

    Returns:
    - None: Displays a plot of runs scored in different categories over time.
    """
    # Filter the DataFrame based on player name and optionally team
    if team2_name:
        filtered_df = df[(df['Player_name'] == player_name) & (df['Team2'] == team2_name)]
    else:
        filtered_df = df[df['Player_name'] == player_name]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player and team (if specified).")
        return

    # Ensure 'Date' column is in datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    
    # Group by date and aggregate runs scored in different categories
    grouped_df = filtered_df.groupby('Date').agg({
        'Dots': 'sum',
        'Ones': 'sum'
    }).reset_index()

    # Apply binning by resampling if team2_name is not specified
    if not team2_name:
        # Set 'Date' as index
        grouped_df.set_index('Date', inplace=True)
        # Resample to monthly frequency and aggregate
        resampled_df = grouped_df.resample('M').agg({
            'Dots': 'sum',
            'Ones': 'sum'
        }).dropna()

        # Interpolate missing values
        resampled_df.interpolate(method='linear', inplace=True)

        resampled_df.reset_index(inplace=True)
        grouped_df = resampled_df

    # Filter out bins where all categories are zero
    grouped_df = grouped_df[(grouped_df[['Dots', 'Ones']].sum(axis=1) > 0)]

    # Check if there is data left to plot
    if grouped_df.empty:
        print("No data available to plot after filtering.")
        return

    # Plot the runs scored in different categories
    plt.figure(figsize=(14, 7))
    plt.plot(grouped_df['Date'], grouped_df['Dots'], marker='o', linestyle='-', color='grey', markersize=8, linewidth=2, label='Dots')
    plt.plot(grouped_df['Date'], grouped_df['Ones'], marker='o', linestyle='-', color='blue', markersize=8, linewidth=2, label='Ones')
    
    plt.title(f'Runs Scored by {player_name} Over Time' + (f' Against {team2_name}' if team2_name else ''), fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Runs Scored', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Set background colors
    plt.gca().set_facecolor('#f0f0f0')  # Light grey background for the plot area
    plt.gcf().set_facecolor('#ffffff')  # White background for the figure
    
    # Improve layout and aesthetics
    plt.tight_layout()
    plt.show()

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# plot_player_runs(df, 'MS Dhoni', 'Pakistan')  # With team2_name
#plot_player_runs(df, 'MS Dhoni')  # Without team2_name





import pandas as pd

def calculate_player_of_match_percentage(df: pd.DataFrame, player_name: str) -> float:
    """
    Calculate the percentage of matches in which a specified player has been named Player of the Match.

    Parameters:
    - df: DataFrame containing cricket match data.
    - player_name: The name of the player to check.

    Returns:
    - float: Percentage of matches in which the player has been named Player of the Match.
    """
    # Check if the 'Player_of_match' column exists in the DataFrame
    if 'Player_of_match' not in df.columns:
        raise ValueError("The DataFrame does not contain the 'Player_of_match' column.")
    
    # Total number of matches
    total_matches = len(df)

    # Number of matches where the player was named Player of the Match
    player_of_match_count = df['Player_of_match'].str.contains(player_name, case=False, na=False).sum()

    # Calculate the percentage
    percentage = (player_of_match_count / total_matches) * 100 if total_matches > 0 else 0

    return percentage

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
#percentage = calculate_player_of_match_percentage(df, 'MS Dhoni')
#print(f'Percentage of matches where MS Dhoni was Player of the Match: {percentage:.2f}%')




import pandas as pd

def calculate_player_win_percentage(df: pd.DataFrame, player_name: str) -> float:
    """
    Calculate the percentage of matches in which a specified player was on the winning team.
    The match is considered a win if Team1 and Winner are the same, and the player is listed in the Player_name column.

    Parameters:
    - df: DataFrame containing cricket match data.
    - player_name: The name of the player to check.

    Returns:
    - float: Percentage of matches where the player was on the winning team.
    """
    # Check if necessary columns exist in the DataFrame
    required_columns = {'Player_name', 'Team1', 'Winner'}
    if not required_columns.issubset(df.columns):
        raise ValueError("The DataFrame does not contain the required columns: 'Player_name', 'Team1', 'Winner'.")

    # Filter the DataFrame where Team1 and Winner are the same
    winning_matches_df = df[df['Team1'] == df['Winner']]

    # Filter further to include only rows where the player was part of the winning team
    player_winning_matches_df = winning_matches_df[winning_matches_df['Player_name'].str.contains(player_name, case=False, na=False)]

    # Total number of winning matches
    total_winning_matches = len(winning_matches_df)

    # Number of winning matches where the player was in the team
    player_winning_matches_count = len(player_winning_matches_df)

    # Calculate the percentage
    percentage = (player_winning_matches_count / total_winning_matches) * 100 if total_winning_matches > 0 else 0

    return percentage

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# percentage = calculate_player_win_percentage(df, 'MS Dhoni')
# print(f'Percentage of matches where MS Dhoni was on the winning team: {percentage:.2f}%')





import pandas as pd
import matplotlib.pyplot as plt

def plot_player_matches_yearly(df: pd.DataFrame, player_name: str, team2_name: str = None):
    """
    Plot the number of matches played by a given player per year. Optionally, filter by opponent team.
    Enhances UI with background color and styling.

    Parameters:
    - df: DataFrame containing the cricket data.
    - player_name: The name of the player.
    - team2_name: The name of the opponent team (optional).

    Returns:
    - None: Displays a plot of the number of matches played per year.
    """
    # Filter the DataFrame based on player name and optionally team
    if team2_name:
        filtered_df = df[(df['Player_name'] == player_name) & (df['Team2'] == team2_name)]
    else:
        filtered_df = df[df['Player_name'] == player_name]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player and team (if specified).")
        return

    # Ensure 'Date' column is in datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

    # Extract the year from the 'Date' column
    filtered_df['Year'] = filtered_df['Date'].dt.year

    # Group by year and count the number of matches played
    grouped_df = filtered_df.groupby('Year').size().reset_index(name='Matches_Played')

    # Plot the number of matches played per year
    plt.figure(figsize=(14, 7))
    plt.bar(grouped_df['Year'].astype(str), grouped_df['Matches_Played'], color='b')
    plt.title(f'Number of Matches Played by {player_name} Per Year' + (f' Against {team2_name}' if team2_name else ''), fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Matches Played', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set background colors
    plt.gca().set_facecolor('#f0f0f0')  # Light grey background for the plot area
    plt.gcf().set_facecolor('#ffffff')  # White background for the figure
    
    # Improve layout and aesthetics
    plt.tight_layout()
    plt.show()

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# plot_player_matches_yearly(df, 'MS Dhoni', 'Pakistan')  # With team2_name
# plot_player_matches_yearly(df, 'MS Dhoni')  # Without team2_name




import pandas as pd

def top_winning_places(df: pd.DataFrame, player_name: str) -> pd.DataFrame:
    """
    Return the top three places where a given player has won the most games.
    
    Parameters:
    - df: DataFrame containing cricket match data.
    - player_name: The name of the player.

    Returns:
    - DataFrame: A DataFrame with the top three places and the number of wins, with indices dropped.
    """
    # Check if the necessary columns exist in the DataFrame
    required_columns = ['Player_name', 'Team1', 'Winner', 'Venue']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The DataFrame does not contain the '{col}' column.")
    
    # Filter the DataFrame based on player name and where the player’s team won
    filtered_df = df[(df['Player_name'] == player_name) & (df['Team1'] == df['Winner'])]
    
    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player with the team winning information.")
        return pd.DataFrame(columns=['Venue', 'Wins'])
    
    # Group by venue and count the number of wins
    venue_wins = filtered_df.groupby('Venue').size().reset_index(name='Wins')
    
    # Sort by the number of wins in descending order and select the top three
    top_venues = venue_wins.sort_values(by='Wins', ascending=False).head(3)
    
    # Reset index and drop the original index column
    top_venues = top_venues.reset_index(drop=True)
    
    return top_venues

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# top_venues = top_winning_places(df, 'MS Dhoni')
# print("Top 3 Places Where MS Dhoni Won Most Games:")
# print(top_venues)



import pandas as pd

def top_series_competitions(df: pd.DataFrame, player_name: str) -> pd.DataFrame:
    """
    Return the top three series/competitions in which a given player has played the most matches.
    
    Parameters:
    - df: DataFrame containing cricket match data.
    - player_name: The name of the player.

    Returns:
    - DataFrame: A DataFrame with the top three series/competitions and the number of matches played.
    """
    # Check if the necessary columns exist in the DataFrame
    required_columns = ['Player_name', 'Series/Competition']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The DataFrame does not contain the '{col}' column.")
    
    # Filter the DataFrame based on player name
    filtered_df = df[df['Player_name'] == player_name]
    
    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the given player.")
        return pd.DataFrame(columns=['Series/Competition', 'Matches_Played'])
    
    # Group by Series/Competition and count the number of matches
    series_competitions = filtered_df.groupby('Series/Competition').size().reset_index(name='Matches_Played')
    
    # Sort by the number of matches played in descending order and select the top three
    top_series = series_competitions.sort_values(by='Matches_Played', ascending=False).head(3)
    
    # Reset index and drop the original index column
    top_series = top_series.reset_index(drop=True)
    
    return top_series

# Example usage:
# df = pd.read_csv('your_data.csv')  # Load your DataFrame
# top_series = top_series_competitions(df, 'MS Dhoni')
# print("Top 3 Series/Competitions Where MS Dhoni Played Most Matches:")
# print(top_series)

