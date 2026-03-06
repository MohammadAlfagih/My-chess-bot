import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio
import chess
import torch
from fastapi.middleware.cors import CORSMiddleware
from model import ChessModel
import random
import numpy as np



#paths 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(BACKEND_DIR, "models")

VOCAB_PATH = os.path.join(MODELS_DIR, "move_vocab.json")
MODEL_PATH = os.path.join(MODELS_DIR, "best_chess_model.pth")


app = FastAPI(title="Lord Mohammed Chess bot api")


app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],)

device = torch.device("cpu")
print("Loading The brain")

with open(VOCAB_PATH,"r", encoding="utf-8") as f:
    int_to_move = json.load(f)

num_classes = len(int_to_move)
model = ChessModel(num_classes=num_classes).to(device)

model.load_state_dict(torch.load(MODEL_PATH,device))
model.eval()

#model functions

def fen_to_tensor(fen):
    piece_to_channel = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5, 
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
    }
    tensor = np.zeros((12, 8, 8), dtype=np.float32)
    board_layout = fen.split(' ')[0]
    
    row, col = 0, 0
    for char in board_layout:
        if char == '/':
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            channel = piece_to_channel[char]
            tensor[channel, row, col] = 1.0
            col += 1
            
    return torch.from_numpy(tensor)

def predict_move(board: chess.Board) -> chess.Move:
    #returns best leagl move
    input_tensor = fen_to_tensor(board.fen()).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    sorted_probs, sorted_indices = torch.sort(probabilities, descending=True)
    
    for i in range(len(sorted_indices)):
        move_idx = str(sorted_indices[i].item())
        predicted_move_uci = int_to_move[move_idx]
        
        try:
            bot_move = chess.Move.from_uci(predicted_move_uci)
            if bot_move in board.legal_moves:
                confidence = sorted_probs[i].item() * 100
                print(f"bot chossing {predicted_move_uci} (confidence: {confidence:.2f}%)")
                return bot_move
        except ValueError:
            continue
            
    #emrgency 
    print("random move so the server dont stop")
    return random.choice(list(board.legal_moves))

#api

@app.websocket("/ws/play")
async def play_chess(websocket : WebSocket):
    await websocket.accept()
    print("New Connection")

    try:
        while True:
            data = await websocket.receive_json()
            fen = data.get("fen")
            bot_color = data.get("bot_color","b")

            board = chess.Board(fen)
            is_white_turn = board.turn
            bot_is_white = (bot_color == "w")

            #is it the bot turn ?
            if(is_white_turn and bot_is_white) or( not is_white_turn and not bot_is_white):
                print("Bot is thinkking")

                await asyncio.sleep(0.5)
                
                best_move = predict_move(board)

                board.push(best_move)

                new_fen = board.fen()

                await websocket.send_json({
                    "status":"success",
                    "move": best_move.uci(),
                    "fen": new_fen
                })
    except WebSocketDisconnect:
        print("play left")
    except Exception as e:
        print(f"Error {e}")
