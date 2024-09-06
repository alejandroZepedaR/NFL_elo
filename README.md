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
8. [License](#license)

## Overview

The Elo rating system is a method for calculating the relative skill levels of players (or teams) in zero-sum games such as chess. This project applies the Elo system to NFL football teams, allowing for dynamic rating updates after each game. The program can calculate the probability of a team winning, predict weekly game outcomes, and provide confidence points for betting.

## How It Works

The program uses an Elo rating algorithm adjusted for the NFL:

1. **Expected Score Calculation**: The expected score of a team is calculated based on its Elo rating relative to its opponent's rating.
   
   \[
   E_A = \frac{1}{1 + 10^{(R_B - R_A) / 400}}
   \]

2. **Margin of Victory (MOV) Adjustment**: The K-factor, which determines how much ratings change after each game, is adjusted based on the margin of victory. Larger victories result in larger rating changes.

   \[
   \text{Adjusted K} = K \times \left( \frac{\text{MOV}}{\text{MOV} + 1} \right) \times \log(\text{MOV} + 1.5)
   \]

3. **Rating Update**: After each game, ratings for both teams are updated based on the expected score and the actual result using the Elo formula.

## Features

- **Calculate Win Probability**: Computes the probability of a team winning against another based on their current Elo ratings.
- **Add Game Results**: Updates team ratings after a game result is input.
- **Display Current Ratings**: Prints the current Elo ratings for all teams.
- **Predict Weekly Game Outcomes**: Provides game outcome predictions for a week and assigns confidence points to each prediction based on the likelihood of winning.
- **Save and Load Ratings**: Elo ratings are saved to and loaded from a CSV file (`elo_scores.csv`).

## Usage

1. **Run the Program**: Execute the `nfl_elo.py` script in your Python environment.
   ```bash
   python nfl_elo.py
