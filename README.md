# My Chess Bot ♟️🤖

A machine learning project to build a chess engine that plays like me! 
This bot is trained on my personal games from Chess.com.

## Phase 1: Data Collection
The `Data-Collection.py` script automatically fetches all archived games for multiple accounts via the Chess.com public API and saves them locally in organized JSON files inside `data/raw/`.

## Phase 2: Data Cleaning & Preprocessing
The `data_cleaning.py` script processes the raw JSON files, filters for standard chess games, and uses the `python-chess` library to simulate the matches. It extracts the board state (FEN) and the exact move I played (UCI format). The output is a clean, ML-ready CSV file containing `(FEN, Move)` pairs saved in `data/processed/`.

## How to run
1. Clone the repository.
2. Install the required libraries: 
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Data Collection script to download the games: 
    ```bash
    python src/Data-Collection.py
    ```
4. Run the Data Cleaning script to extract board states and moves:
    ```bash
    python src/data_cleaning.py
    ```