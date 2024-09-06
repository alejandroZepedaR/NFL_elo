# NFL Elo Rating System

This project is a Python program that implements an Elo rating system for NFL teams. The program calculates and updates team ratings based on game results, predicts game outcomes, and provides a betting strategy by assigning confidence points to each game prediction.

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Features](#features)
4. [Usage](#usage)
5. [Dependencies](#dependencies)
6. [File Descriptions](#file-descriptions)
7. [Contributing](#contributing)

## Overview

The Elo rating system is a method for calculating the relative skill levels of players (or teams) in zero-sum games such as chess. This project applies the Elo system to NFL football teams, allowing for dynamic rating updates after each game. The program can calculate the probability of a team winning, predict weekly game outcomes, and provide confidence points for betting.

## How It Works

The program uses an Elo rating algorithm adjusted for the NFL:

1. **Expected Score Calculation**: The expected score of a team is calculated based on its Elo rating relative to its opponent's rating.

   `E_A = 1 / (1 + 10^((R_B - R_A) / 400))`

2. **Margin of Victory (MOV) Adjustment**: The K-factor, which determines how much ratings change after each game, is adjusted based on the margin of victory. Larger victories result in larger rating changes.

   `Adjusted K = K * (MOV / (MOV + 1)) * log(MOV + 1.5)`

3. **Rating Update**: After each game, ratings for both teams are updated based on the expected score and the actual result using the Elo formula.

## Features

- **Calculate Win Probability**: Computes the probability of a team winning against another based on their current Elo ratings.
- **Add Game Results**: Updates team ratings after a game result is input.
- **Display Current Ratings**: Prints the current Elo ratings for all teams.
- **Predict Weekly Game Outcomes**: Provides game outcome predictions for a week and assigns confidence points to each prediction based on the likelihood of winning.
- **Save and Load Ratings**: Elo ratings are saved to and loaded from a CSV file (`elo_scores.csv`).

## Usage

1. **Run the Program**: Execute the `nfl_elo.py` script in your Python environment.

   `python nfl_elo.py`

2. **Commands**:
   - `1`: **Calculate probability of team winning** - Input two teams to see their win probabilities.
   - `2`: **Add game result** - Input the result of a game (team names and scores) to update the Elo ratings.
   - `3`: **Display current ratings** - View the current Elo ratings for all teams.
   - `4`: **Get week prediction by points** - Predict the outcome of weekly games and assign confidence points.
   - `5`: **Save and exit** - Save the updated Elo ratings to `elo_scores.csv` and exit the program.

3. **Input Validation**: The program includes validation to ensure that valid team names are input.

## Dependencies

The program requires the following Python libraries:

- `pandas`
- `math`

Install them using pip if you haven't already:

`pip install pandas`

## File Descriptions

- **nfl_elo.py**: The main program file containing all the functionality for the Elo rating system.
- **elo_scores.csv**: A CSV file that stores the initial Elo ratings of NFL teams. This file is updated with new ratings after games are played.

### Key Functions in `nfl_elo.py`

- **`read_file(file_name)`**: Reads Elo ratings from a CSV file into a dictionary.
- **`calculate_expected_scores(rating1, rating2)`**: Calculates expected scores for two teams based on their Elo ratings.
- **`calculate_new_ratings(rating1, rating2, result, mov)`**: Calculates new ratings after a game result.
- **`get_mov_adjustment(mov)`**: Adjusts the K-factor based on the margin of victory.
- **`calculate_probability(team1, team2, ratings)`**: Computes the probability of a team winning against another.
- **`add_game_result(team1, team2, team1_score, team2_score, ratings)`**: Adds a game result and updates the Elo ratings.
- **`get_week_prediction_by_points(ratings)`**: Predicts weekly game outcomes and assigns confidence points.
- **`save_ratings(ratings)`**: Saves the updated ratings to the CSV file.

## Contributing

Contributions to improve this project are welcome! Feel free to fork this repository, make changes, and submit a pull request. Please ensure your code adheres to the project's style and passes all tests.


