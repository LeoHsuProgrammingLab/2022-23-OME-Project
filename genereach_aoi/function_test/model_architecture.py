import torch
import torchvision.models as model_set
import torch.nn as nn

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

resnet18 = model_set.resnet18(weights = None)
resnet18.fc = nn.Linear(in_features= resnet18.fc.in_features, out_features = 2)

pre_resnet18 = model_set.resnet18(weights = model_set.ResNet18_Weights.DEFAULT)
pre_resnet18.fc = nn.Linear(in_features = pre_resnet18.fc.in_features, out_features = 2)


class Basic_CNN(nn.Module):
    def __init__(self):
        super(Basic_CNN, self).__init__()
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        # torch.nn.MaxPool2d(kernel_size, stride, padding)
        # input 維度 [3, 128, 128]
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, 3, 1, 1),  # [64, 128, 128]
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [64, 64, 64]

            nn.Conv2d(64, 128, 3, 1, 1), # [128, 64, 64]
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [128, 32, 32]

            nn.Conv2d(128, 256, 3, 1, 1), # [256, 32, 32]
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [256, 16, 16]

            nn.Conv2d(256, 512, 3, 1, 1), # [512, 16, 16]
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 8, 8]
            
            nn.Conv2d(512, 512, 3, 1, 1), # [512, 8, 8]
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 4, 4]

            nn.Dropout(0.5)
        )
        self.fc = nn.Sequential(
            nn.Linear(512*4*4, 256),
            nn.ReLU(),
            nn.Linear(256, 2)
        )
    def forward(self, x):
        out = self.cnn(x)
        out = out.view(out.size()[0], -1)
        return self.fc(out)