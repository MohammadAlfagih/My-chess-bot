# My Chess Bot ♟️🤖

A machine learning project to build a chess engine that plays like me! 
This bot is trained on my personal games from Chess.com. It features a custom Convolutional Neural Network (CNN) built with PyTorch and a  React/Vite frontend.

## ⚡ Quick Start (Run via Docker Hub)
run the pre-built Docker images directly

Run the Backend (AI Engine):
```bash
docker run -d -p 8000:8000 malfagih/chess-backend:latest
```
Run the Frontend (React UI):
```bash
docker run -d -p 3000:80 malfagih/chess-frontend:latest
```



##  How to Run the App (Using Docker Compse)
The easiest way to run the full-stack application (Frontend + AI Backend) is using Docker
1. Clone the repository: https://github.com/MohammadAlfagih/My-chess-bot
2. Start the application using Docker Compose: 
```bash
    docker-compose up --build
```
3. Open your browser and play against the bot at: http://localhost:3000 
(The FastAPI backend runs simultaneously on http://localhost:8000)

## 🏗️ Project Architecture & Phases
### Phase 1: Data Collection
The `Data-Collection.py` script automatically fetches all archived games for multiple accounts via the Chess.com public API and saves them locally in organized JSON files inside `data/raw/`.

### Phase 2: Data Cleaning & Preprocessing
The `data_cleaning.py` script processes the raw JSON files, filters for standard chess games, and uses the `python-chess` library to simulate the matches. It extracts the board state (FEN) and the exact move I played (UCI format). The output is a clean, ML-ready CSV file containing `(FEN, Move)` pairs saved in `data/processed/`.


### Phase 3: Dataset Preparation & Model Architecture
- **Dataset (`dataset.py`):** Converts the FEN strings into 12x8x8 PyTorch tensors (representing the 64 squares and 12 piece types) and builds a vocabulary mapping for all unique moves.
- **Model (`model.py`):** A custom Convolutional Neural Network (CNN) built with PyTorch. It features 4 Conv2d layers with Batch Normalization and LeakyReLU activations to extract spatial board patterns, followed by Fully Connected layers to predict the next move.


### Phase 4: Model Training
The `train.py` script connects the dataset and the model. It splits the data into training and validation sets, uses CrossEntropyLoss with the AdamW optimizer, and runs the training loop. It implements Early Stopping to save the best-performing model weights (`best_chess_model.pth`) and the move vocabulary (`move_vocab.json`) inside the `models/` directory.

### 🛠️ Manual Setup (Without Docker)
1. Clone the repository.
2. Install the required libraries: 
   ```bash
   cd backend
    pip install -r requirements.txt
   ```
3. Run data collection and cleaning: 
    ```bash
    python src/data-collection.py
    python src/data_cleaning.py
    ```
4. Start The backend:
    ```bash
    uvicorn src.app:app --reload
    ```
5. Start the frontend:
    ```bash
    cd frontend && npm install && npm run dev
    ```