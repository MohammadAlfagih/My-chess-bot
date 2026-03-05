import torch
from torch import nn
import torch.nn.functional as F

class ChessModel(nn.Module):
    #Num of classes Represtint all the unique moves in the dataset
    #meaning each move i have made
    def __init__(self,num_classes):
        super(ChessModel,self).__init__()

        #Convolutional Layers
        # 12 is the number of pieces == 12 Channels

        self.conv1 = nn.Conv2d(in_channels=12,out_channels=32, kernel_size=3,padding=1)
        self.bn1 = nn.BatchNorm2d(32)

        self.conv2 = nn.Conv2d(in_channels=32,out_channels=64,kernel_size=3,padding=1)
        self.bn2 = nn.BatchNorm2d(64)

        self.conv3 = nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,padding=1)
        self.bn3 = nn.BatchNorm2d(128)

        self.conv4 = nn.Conv2d(in_channels=128,out_channels=128,kernel_size=3,padding=1)
        self.bn4 = nn.BatchNorm2d(128)

        # Fully connected layers
        # No pooling so we dont loss the place of pieces
        #So its still 8 x 8 but the chnnels are now 128
        self.fc1 = nn.Linear(128 * 8 * 8,512)

        self.dropout = nn.Dropout(0.5)
        self.Lrelu = nn.LeakyReLU()

        self.fc2 = nn.Linear(512,num_classes)
    def forward(self, x):
        #conb
        x= self.Lrelu(self.bn1(self.conv1(x)))
        x= self.Lrelu(self.bn2(self.conv2(x)))
        x= self.Lrelu(self.bn3(self.conv3(x)))
        x= self.Lrelu(self.bn4(self.conv4(x)))


        x = x.view(x.size(0),-1) #flatten

        x = self.Lrelu(self.fc1(x))
        x= self.dropout(x)
        x = self.fc2(x)  

        #no softmax, and if u dont know why go study

        return x

#testing code

if __name__ == '__main__':
    # لنفترض أن عدد النقلات الفريدة التي استخرجناها في dataset.py هو 1500
    dummy_num_classes = 1500 
    model = ChessModel(num_classes=dummy_num_classes)
    
    # محاكاة لدفعة بيانات (Batch) قادمة من الـ DataLoader
    # 32 رقعة، 12 قناة، أبعاد 8x8
    dummy_input = torch.randn(32, 12, 8, 8) 
    
    # تمرير البيانات عبر المودل
    output = model(dummy_input)
    
    print("\n✅ تم بناء المودل بنجاح!")
    print("-" * 30)
    print(f"شكل المدخلات (Input Shape) : {dummy_input.shape}")
    print(f"شكل المخرجات (Output Shape): {output.shape}")
    print(f"هل المخرجات مطابقة للمتوقع؟  : {output.shape == (32, dummy_num_classes)}")