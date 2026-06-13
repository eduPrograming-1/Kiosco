import torch
import torch.nn as nn

class RedNeuronal(nn.Module):

    def __init__(self):
        super(RedNeuronal, self).__init__()

        self.red = nn.Sequential(
            nn.Linear(10,20),
            nn.ReLU(),
            nn.Linear(20,1)
        )

    def forward(self, x):
        return self.red(x)

modelo = RedNeuronal()
