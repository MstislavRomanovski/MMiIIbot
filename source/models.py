import torch
import torch.nn as nn

class BERT_based(nn.Module):

    def __init__(self, bert):
        super(BERT_based, self).__init__()
        self.bert = bert
        self.dropout = nn.Dropout(0.1)
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(768,512)
        self.fc2 = nn.Linear(512,5)
        self.softmax = nn.LogSoftmax(dim = 1)

    def forward(self, sent_id, mask):
        _, cls_hs = self.bert(sent_id, attention_mask = mask, return_dict = False)
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x
        
class Autoencoder(nn.Module):
    def __init__(self, input_dim, hidden_dim=256):
        super(Autoencoder, self).__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.decoder = nn.LSTM(hidden_dim, input_dim, batch_first=True)

    def forward(self, x):
        x = x.unsqueeze(1)  
        _, (h, _) = self.encoder(x)
        h = h.repeat(1, x.shape[1], 1)  
        out, _ = self.decoder(h)
        return out.squeeze(1)  