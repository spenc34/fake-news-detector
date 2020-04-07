import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

class FakeNewsNetwork(nn.Module):
    def __init__(self, in_dim, out_dim=2):
        super().__init__()

        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        self.hidden1 = nn.Linear(in_dim, 32)
        self.hidden2 = nn.Linear(32, 16)
        self.output = nn.Linear(16, out_dim)

        self.activation = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.hidden1(x)
        x = self.activation(x)
        x = self.hidden2(x)
        x = self.activation(x)
        x = self.output(x)
        x = self.softmax(x)
        return x

    def load_weights(self, path):
        self.load_state_dict(torch.load(path, map_location=self.device))

    def dict_to_tensor(self, info):
        # This is to make sure that we always have the data in the proper order
        # Should be in this order: entropy, perplexity, clean_entropy, clean_perplexity, edit_distance, has_wp_content, num_iframes
        data = [
            info['entropy'],
            info['perplexity'],
            info['clean_entropy'],
            info['clean_perplexity'],
            info['edit_distance'],
            info['has_wp_content'],
            info['num_iframes']
        ]
        return torch.tensor([data], device=self.device)