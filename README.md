# My Chess Bot ♟️🤖

A machine learning project to build a chess engine that plays like me! 
This bot is trained on my personal games from Chess.com.

## Phase 1: Data Collection
The `Data-Collection.py` script automatically fetches all archived games for multiple accounts via the Chess.com public API and saves them locally in organized JSON files inside `data/raw/`.

## Phase 2: Data Cleaning & Preprocessing
The `data_cleaning.py` script processes the raw JSON files, filters for standard chess games, and uses the `python-chess` library to simulate the matches. It extracts the board state (FEN) and the exact move I played (UCI format). The output is a clean, ML-ready CSV file containing `(FEN, Move)` pairs saved in `data/processed/`.


## Phase 3: Dataset Preparation & Model Architecture
- **Dataset (`dataset.py`):** Converts the FEN strings into 12x8x8 PyTorch tensors (representing the 64 squares and 12 piece types) and builds a vocabulary mapping for all unique moves.
- **Model (`model.py`):** A custom Convolutional Neural Network (CNN) built with PyTorch. It features 4 Conv2d layers with Batch Normalization and LeakyReLU activations to extract spatial board patterns, followed by Fully Connected layers to predict the next move.


## Phase 4: Model Training
The `train.py` script connects the dataset and the model. It splits the data into training and validation sets, uses CrossEntropyLoss with the AdamW optimizer, and runs the training loop. It implements Early Stopping to save the best-performing model weights (`best_chess_model.pth`) and the move vocabulary (`move_vocab.json`) inside the `models/` directory.

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