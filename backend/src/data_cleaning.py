import os
import json
import io
import chess.pgn
import pandas as pd

# This a list of all my chess accounts
USERNAMES =["iimo7a", "i-imo7a","l_gnedoy", "m_gnedoy"]

def clean_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    raw_data_folder = os.path.join(project_root, "data", "raw") #data his ere
    processed_data_folder = os.path.join(project_root, "data", "processed") #we will but data in here
    processed_file_path = os.path.join(processed_data_folder, "cleaned_chess_data.csv")

    os.makedirs(processed_data_folder, exist_ok=True)

    dataset =[]
    total_game_processed =0
    for username in USERNAMES:
        user_folder = os.path.join(raw_data_folder, username)
        if not os.path.exists(user_folder):
            print(f"There is no folder for {username}")
            continue
        print(f"Processing {username} games data")

        for filename in os.listdir(user_folder):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(user_folder,filename)
            with open(filepath,"r",encoding="utf-8") as f:
                month_data = json.load(f)
            for game in month_data.get("games",[]):
                if game.get("rules") != "chess" or "pgn" not in game:
                    continue

                white_player=game["white"]["username"].lower()
                black_player=game["black"]["username"].lower()
                
                playing_as_white = (white_player == username.lower())

                pgn_string = game["pgn"]

                #chess lib need file-like object to read
                pgn_io =io.StringIO(pgn_string)
                parsed_game = chess.pgn.read_game(pgn_io)

                if parsed_game is None:
                    continue
                board = parsed_game.board()

                for move in parsed_game.mainline_moves():
                    is_white_turn = board.turn
                    
                    #Here is the main idea
                    #we will save the FEN and what did i do in that position, only me
                    if(is_white_turn and playing_as_white) or (not is_white_turn and not playing_as_white):
                        dataset.append({
                            "fen": board.fen(),
                            "move":move.uci()
                        })
                    board.push(move)
                total_game_processed+=1
    print("Done Processing")
    print(f"total games Processed  {total_game_processed}")
    print(f"Each data point extracted (move,postion) {len(dataset)}")

    if dataset:
        df = pd.DataFrame(dataset)
        df.to_csv(processed_file_path,index=False)
        print(f"Data saved in {processed_file_path}")
    else:
        print("No data processd good")

if __name__ == "__main__":
    clean_data()