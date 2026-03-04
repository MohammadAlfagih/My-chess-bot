import os 
import torch 
import pandas as pd
import numpy as np

from torch.utils.data import DataLoader, Dataset


class ChessDataset(Dataset):
    def __init__(self,csv_file):

        self.data = pd.read_csv(csv_file)
        
        # Limting the moves
        self.unique_moves = self.data["move"].unique()
        self.num_classes = len(self.unique_moves)

        #Createing A mapping. the moves to int and vice versa
        self.move_to_int = {move: idx for idx, move in enumerate(self.unique_moves)}
        self.int_to_move = {idx: move for move, idx in self.move_to_int.items()}


        #Dictonry for each piece and Crossponding channels
        #Caps letters = (white), small Letters =(Black)
        self.piece_to_channel ={
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5, #w
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11 #b
        }
    def __len__(self):
        return len(self.data)
    
    #the big problem
    def fen_to_tensor(self,fen):
        #we will have (12,8,8) 12 pieces, 8 cols , 8 rows

        tensor = np.zeros((12,8,8), dtype=np.float32)

        #normal FEN :1r6/5pp1/R1R4p/1r1pP3/2pkQPP1/7P/1P6/2K5 w - - 0 41
        #we want only the board :1r6/5pp1/R1R4p/1r1pP3/2pkQPP1/7P/1P6/2K5

        board_leyout = fen.split(" ")[0]

        row = 0
        col=0
        for char in board_leyout:
            #new row
            if char == "/":
                row +=1

                #make col agin zero
                col =0
            elif char.isdigit():
                #fen represnt empty squers as numbers
                col += int(char)
            else:
                #putting 1 in the channel of the piece
                channel = self.piece_to_channel[char]
                tensor[channel,row,col] =1 
                col+= 1
        return torch.from_numpy(tensor)
    def __getitem__(self,idx):

        row_data = self.data.iloc[idx]
        fen = row_data["fen"]
        move_string= row_data["move"]

        #input 
        X= self.fen_to_tensor(fen)

        #target

        y= torch.tensor(self.move_to_int[move_string],dtype=torch.long) #for Cross entropy loss
        return X,y



#checking code only, from ai

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "processed", "cleaned_chess_data.csv")
    

    chess_dataset = ChessDataset(csv_path)
    

    dataloader = DataLoader(chess_dataset, batch_size=32, shuffle=True)
    

    X_batch, y_batch = next(iter(dataloader))
    
    print("\n--- Tensor Shapes ---")
    print(f"X (Input) shape: {X_batch.shape} --> [Batch_Size, Channels, Height, Width]")
    print(f"y (Target) shape: {y_batch.shape} --> [Batch_Size]")
    print(f"Example Target labels (Indices): {y_batch[:5]}")

