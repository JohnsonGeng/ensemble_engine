"""

Malconv malware detector implemented by Pytorch

"""


import os
import sys
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F

module_path = os.path.split(os.path.abspath(sys.modules[__name__].__file__))[0]
model_path = os.path.join(module_path, 'model/malconv_model.checkpoint')

class MalConv(nn.Module):
    # trained to minimize cross-entropy loss
    # criterion = nn.CrossEntropyLoss()
    def __init__(self, out_size=2, channels=128, window_size=512, embd_size=8):
        super(MalConv, self).__init__()
        self.embd = nn.Embedding(257, embd_size, padding_idx=0)

        self.window_size = window_size

        self.conv_1 = nn.Conv1d(embd_size, channels, window_size, stride=window_size, bias=True)
        self.conv_2 = nn.Conv1d(embd_size, channels, window_size, stride=window_size, bias=True)

        self.pooling = nn.AdaptiveMaxPool1d(1)

        self.fc_1 = nn.Linear(channels, channels)
        self.fc_2 = nn.Linear(channels, out_size)

    def forward(self, x):
        x = self.embd(x.long())
        x = torch.transpose(x, -1, -2)

        cnn_value = self.conv_1(x)
        gating_weight = torch.sigmoid(self.conv_2(x))

        x = cnn_value * gating_weight

        x = self.pooling(x)

        # Flatten
        x = x.view(x.size(0), -1)

        x = F.relu(self.fc_1(x))
        x = self.fc_2(x)

        return x


class MalConvModel(object):
    # Malconv threshold = 0.5
    def __init__(self, name='Malconv'):
        self.model = MalConv(channels=256, window_size=512, embd_size=8).train()
        weights = torch.load(model_path, map_location='cpu')
        # Load trained Malconv
        self.model.load_state_dict(weights['model_state_dict'])
        self.threshold = 0.5
        self.__name__ = name

    def predict(self, bytez):
        _inp = torch.from_numpy(np.frombuffer(bytez, dtype=np.uint8)[np.newaxis, :])
        with torch.no_grad():
            outputs = F.softmax(self.model(_inp), dim=-1)

        proba = outputs.detach().numpy()[0, 1]

        return proba

