import os
import json
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader,Dataset, random_split
from dataset import ChessDataset
from model import ChessModel

def train_model():
    #path config

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    csv_path = os.path.join(project_root,"data","processed","cleaned_chess_data.csv")
    models_dir = os.path.join(project_root,"models")

    os.makedirs(models_dir,exist_ok=True)

    #device config
    device = torch.device("cuda" if torch.cuda.is_available()  else "cpu")
    print(f"training on {device}")

    #data prep

    dataset = ChessDataset(csv_path)
    num_classes = dataset.num_classes
    
    #Vocab dict used later when playing
    vocab_path = os.path.join(models_dir,"move_vocab.json")
    with open(vocab_path,"w",encoding="utf-8") as f:
        json.dump(dataset.int_to_move,f,ensure_ascii=False,indent=2)
    print(f"vocab saved on {vocab_path}")

    #split
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset,[train_size,val_size])

    batch_size =32
    train_loader = DataLoader(train_dataset,batch_size=batch_size,shuffle=True)
    val_loader = DataLoader(val_dataset,batch_size=batch_size,shuffle=False) # if u dont know way falsy go study more

    print(f"Train_samples = {train_size}")
    print(f"val_samples = {val_size}")

    #definition
    model = ChessModel(num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(),lr=0.001)

    #training loop 

    epochs=15
    best_val_loss = float("inf")
    for epoch in range(epochs):
        model.train()
        running_train_loss =0.0
        correct_train =0
        total_train =0

        for batch_idx, (X_batch,y_batch) in enumerate(train_loader):
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)

            outputs = model(X_batch)

            loss = criterion(outputs, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_train_loss += loss.item()

            #accuracy
            _, predicted = torch.max(outputs.data, 1)
            total_train += y_batch.size(0)
            correct_train += (predicted == y_batch).sum().item()

        train_loss = running_train_loss / len(train_loader)
        train_acc = 100 * correct_train / total_train

        #validation

        model.eval()
        running_val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for X_batch,y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)

                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                running_val_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                total_val += y_batch.size(0)
                correct_val += (predicted == y_batch).sum().item()

        val_loss = running_val_loss / len(val_loader)
        val_acc = 100 * correct_val / total_val        
        print(f"Epoch [{epoch+1}/{epochs}] "
              f"| Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% "
              f"| Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        # ---------------- save best model----------------
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            model_save_path = os.path.join(models_dir, "best_chess_model.pth")
            torch.save(model.state_dict(), model_save_path)
            print(f"   🌟 New best model saved! (Val Loss: {best_val_loss:.4f})")
    print("\n✅ Training complete!")
    print(f"Best Validation Loss: {best_val_loss:.4f}")

if __name__ == "__main__":
    train_model()

