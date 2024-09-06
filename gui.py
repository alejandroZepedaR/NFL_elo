import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
from tkinter import ttk  # For Treeview
import pandas as pd
import math

def read_file(file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    team_elo_dict = df.set_index('Team')['Elo'].to_dict()
    return team_elo_dict

def calculate_expected_scores(rating1, rating2):
    # Calculate expected score for team 1
    expected_score1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    # Calculate expected score for team 2
    expected_score2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))
    return expected_score1, expected_score2

def calculate_new_ratings(rating1, rating2, result, mov):
    # Calculate expected scores for both teams
    expected_score1, expected_score2 = calculate_expected_scores(rating1, rating2)
    # Get the adjusted K-factor based on the margin of victory
    adjusted_k = get_mov_adjustment(mov)
    # Determine the actual scores based on the result
    if result == 1:  # Team 1 wins
        actual_score1 = 1
        actual_score2 = 0
    elif result == 0:  # Team 2 wins
        actual_score1 = 0
        actual_score2 = 1
    else:  # Draw
        actual_score1 = 0.5
        actual_score2 = 0.5
    # Calculate new ratings using the Elo formula
    new_rating1 = rating1 + adjusted_k * (actual_score1 - expected_score1)
    new_rating2 = rating2 + adjusted_k * (actual_score2 - expected_score2)
    return new_rating1, new_rating2

def get_mov_adjustment(mov):
    # Base K-factor
    K = 30
    # Calculate the MOV adjustment factor
    mov_adjustment = K * (mov / (mov + 1)) * math.log(mov + 1.5)
    return mov_adjustment

def calculate_probability(team1, team2, ratings):
    expected_scores = calculate_expected_scores(ratings[team1], ratings[team2])
    messagebox.showinfo("Probability", f"Expected probability for {team1}: {expected_scores[0]:.2f}\nExpected probability for {team2}: {expected_scores[1]:.2f}")

def add_game_result(team1, team2, team1_score, team2_score, ratings):
    # Calculate margin of victory
    mov = abs(team1_score - team2_score)
    # Determine the result of the game
    if team1_score > team2_score:
        result = 1
    elif team2_score > team1_score:
        result = 0
    else:
        result = 0.5
    # Calculate new ratings for both teams
    new_ratings = calculate_new_ratings(ratings[team1], ratings[team2], result, mov)
    # Update the ratings dictionary with the new ratings
    ratings[team1] = new_ratings[0]
    ratings[team2] = new_ratings[1]
    return ratings

def save_ratings(ratings):
    file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    # Convert the dictionary back to a DataFrame
    df = pd.DataFrame(list(ratings.items()), columns=['Team', 'Elo'])
    # Save the DataFrame to the CSV file
    df.to_csv(file_name, index=False)
    messagebox.showinfo("Save", "Ratings saved successfully!")

def print_current_ratings(ratings, text_widget):
    text_widget.delete('1.0', tk.END)
    for team, rating in ratings.items():
        text_widget.insert(tk.END, f"{team}: {rating}\n")

def load_ratings():
    file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_name:
        ratings = read_file(file_name)
        return ratings
    else:
        return {}

def display_predictions_table(predictions):
    # Create a new window for displaying predictions in a table
    table_window = Toplevel(window)
    table_window.title("Predictions Table")

    # Create a Treeview widget
    tree = ttk.Treeview(table_window, columns=("Game", "Predicted Winner", "Points"), show="headings")
    tree.heading("Game", text="Game")
    tree.heading("Predicted Winner", text="Predicted Winner")
    tree.heading("Points", text="Points")

    # Insert data into the Treeview
    for i, (game, (predicted_winner, points)) in enumerate(predictions.items(), start=1):
        game_text = f"{game[0]} vs {game[1]}"
        tree.insert("", "end", values=(game_text, predicted_winner, points))

    tree.pack(fill="both", expand=True)

def get_week_prediction_by_points(ratings):
    # Create a new window for entering the 16 games
    prediction_window = Toplevel(window)
    prediction_window.title("Enter Week Games")

    # Create entries for 16 games
    game_entries = []
    
    for i in range(16):
        frame = tk.Frame(prediction_window)
        frame.pack(padx=10, pady=5)

        tk.Label(frame, text=f"Game {i+1} Team 1:").grid(row=0, column=0)
        team1_entry = tk.Entry(frame)
        team1_entry.grid(row=0, column=1)

        tk.Label(frame, text="Team 2:").grid(row=0, column=2)
        team2_entry = tk.Entry(frame)
        team2_entry.grid(row=0, column=3)

        game_entries.append((team1_entry, team2_entry))

    def calculate_predictions():
        games = []
        for team1_entry, team2_entry in game_entries:
            team1 = team1_entry.get()
            team2 = team2_entry.get()
            if team1 in ratings and team2 in ratings:
                games.append((team1, team2))
            else:
                messagebox.showwarning("Invalid Input", "One or both teams are not in the ratings. Please try again.")
                return

        # Dictionary to store predicted winners and their confidence differences
        games_points = {}

        for game in games:
            team1, team2 = game
            # Calculate expected scores for both teams
            expected_scores = calculate_expected_scores(ratings[team1], ratings[team2])
            
            # Determine the predicted winner
            if expected_scores[0] > expected_scores[1]:
                predicted_winner = team1
                difference = expected_scores[0] - expected_scores[1]
            else:
                predicted_winner = team2
                difference = expected_scores[1] - expected_scores[0]
            
            # Store the game with the predicted winner and its difference
            games_points[game] = (predicted_winner, difference)
        
        # Sort the games by the confidence difference in descending order
        sorted_games = sorted(games_points.items(), key=lambda x: x[1][1], reverse=True)

        # Assign points from 16 to 1 based on the sorted order
        points = 16
        predictions_with_points = {}
        for game, (predicted_winner, difference) in sorted_games:
            predictions_with_points[game] = (predicted_winner, points)
            points -= 1

        # Display predictions in a table
        display_predictions_table(predictions_with_points)

    # Calculate button
    calculate_button = tk.Button(prediction_window, text="Calculate Predictions", command=calculate_predictions)
    calculate_button.pack(pady=10)

def gui_app():
    global window
    # Initialize the main window
    window = tk.Tk()
    window.title("Elo Rating System")

    # Load Ratings Button
    ratings = {}
    
    def load_ratings_button():
        nonlocal ratings
        ratings = load_ratings()
        if ratings:
            messagebox.showinfo("Load", "Ratings loaded successfully!")

    load_button = tk.Button(window, text="Load Ratings", command=load_ratings_button)
    load_button.grid(row=0, column=0, padx=10, pady=10)

    # Calculate Probability Button
    def calculate_probability_button():
        if not ratings:
            messagebox.showwarning("Error", "Load ratings first!")
            return
        team1 = team1_entry.get()
        team2 = team2_entry.get()
        if team1 in ratings and team2 in ratings:
            calculate_probability(team1, team2, ratings)
        else:
            messagebox.showwarning("Error", "Invalid team names!")

    team1_entry = tk.Entry(window)
    team1_entry.grid(row=1, column=1)
    team2_entry = tk.Entry(window)
    team2_entry.grid(row=2, column=1)

    team1_label = tk.Label(window, text="Team 1:")
    team1_label.grid(row=1, column=0)
    team2_label = tk.Label(window, text="Team 2:")
    team2_label.grid(row=2, column=0)

    prob_button = tk.Button(window, text="Calculate Probability", command=calculate_probability_button)
    prob_button.grid(row=3, column=1, padx=10, pady=10)

    # Add Game Result
    def add_game_result_button():
        if not ratings:
            messagebox.showwarning("Error", "Load ratings first!")
            return
        team1 = team1_entry.get()
        team2 = team2_entry.get()
        try:
            team1_score = int(team1_score_entry.get())
            team2_score = int(team2_score_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Scores must be integers!")
            return

        if team1 in ratings and team2 in ratings:
            add_game_result(team1, team2, team1_score, team2_score, ratings)
            messagebox.showinfo("Success", "Game result added and ratings updated!")
        else:
            messagebox.showwarning("Error", "Invalid team names!")

    team1_score_entry = tk.Entry(window)
    team1_score_entry.grid(row=4, column=1)
    team2_score_entry = tk.Entry(window)
    team2_score_entry.grid(row=5, column=1)

    team1_score_label = tk.Label(window, text="Team 1 Score:")
    team1_score_label.grid(row=4, column=0)
    team2_score_label = tk.Label(window, text="Team 2 Score:")
    team2_score_label.grid(row=5, column=0)

    add_result_button = tk.Button(window, text="Add Game Result", command=add_game_result_button)
    add_result_button.grid(row=6, column=1, padx=10, pady=10)

    # Display Current Ratings
    ratings_text = tk.Text(window, height=10, width=50)
    ratings_text.grid(row=7, column=0, columnspan=2)

    def display_ratings_button():
        if ratings:
            print_current_ratings(ratings, ratings_text)
        else:
            messagebox.showwarning("Error", "Load ratings first!")

    display_button = tk.Button(window, text="Display Current Ratings", command=display_ratings_button)
    display_button.grid(row=8, column=0, padx=10, pady=10)

    # Save Ratings
    def save_ratings_button():
        if ratings:
            save_ratings(ratings)
        else:
            messagebox.showwarning("Error", "Load ratings first!")

    save_button = tk.Button(window, text="Save Ratings", command=save_ratings_button)
    save_button.grid(row=8, column=1, padx=10, pady=10)

    # Get Week Prediction by Points Button
    def get_week_prediction_button():
        if ratings:
            get_week_prediction_by_points(ratings)
        else:
            messagebox.showwarning("Error", "Load ratings first!")

    week_prediction_button = tk.Button(window, text="Get Week Predictions", command=get_week_prediction_button)
    week_prediction_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    # Start the GUI loop
    window.mainloop()

gui_app()





