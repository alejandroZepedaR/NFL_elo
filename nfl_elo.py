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
    print(f"Expected probabilty for {team1}: {expected_scores[0]:.2f}")
    print(f"Expected probabilty for {team2}: {expected_scores[1]:.2f}")

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
    # Convert the dictionary back to a DataFrame
    df = pd.DataFrame(list(ratings.items()), columns=['Team', 'Elo'])
    
    # Save the DataFrame to the CSV file
    df.to_csv('elo_scores.csv', index=False)

def validate_team_input(teams, team_num):
    possible_team = input(f"Enter team {team_num}: ")
    if possible_team not in teams:
        print("Invalid team. Please try again.")
        return validate_team_input(teams, team_num)
    return possible_team

def get_week_games(teams):
    games = []

    for i in range(0, 16):
        print(f"Game: {i+1}")
        
        team1 = validate_team_input(teams, 1)
        team2 = validate_team_input(teams, 2)
        games.append((team1, team2))

    return games

def get_week_prediction_by_points(ratings):
    # Get the weekly games
    games = get_week_games(ratings.keys())
    
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

    # Print results
    for game, (predicted_winner, points) in predictions_with_points.items():
        print(f"Predicted Winner: {predicted_winner} for game {game} with {points} points.")

    return predictions_with_points

        
def print_commands():
    print("Commands:")
    print("1. Calculate probability of team winning")
    print("2. Add game result")
    print("3. Display current ratings")
    print("4. Get week prediction by points")
    print("5. Save and exit")
    print()

def print_current_ratings(ratings):
    print("Current Ratings:")
    for team, rating in ratings.items():
        print(f"{team}: {rating}")

def main():
    elos_dict = read_file('elo_scores.csv')
    while True:
        print_commands()
        command = input("Enter a command: ")
        if command == '1':
            team1 = input("Enter the first team: ")
            team2 = input("Enter the second team: ")
            calculate_probability(team1, team2, elos_dict)
        elif command == '2':
            team1 = input("Enter the first team: ")
            team2 = input("Enter the second team: ")
            team1_score = int(input("Enter the score for the first team: "))
            team2_score = int(input("Enter the score for the second team: "))
            elos_dict = add_game_result(team1, team2, team1_score, team2_score, elos_dict)
        elif command == '3':
            print_current_ratings(elos_dict)
        elif command == '4':
            get_week_prediction_by_points(elos_dict)
        elif command == '5':
            save_ratings(elos_dict)
            break
        else:
            print("Invalid command. Please try again.")
        print()

main()