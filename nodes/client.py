import flwr as fl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np
import os

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(32*13*13, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 32*13*13)
        x = self.fc1(x)
        return x

class FlowerClient(fl.client.NumPyClient):
    def __init__(self, node_id):
        self.model = SimpleCNN()
        self.node_id = node_id
        self.data_path = os.getenv("DATA_PATH", f"/app/data/node_{node_id.lower()}")

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        self.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        # Simulate training
        return self.get_parameters(config), 100, {"loss": 0.5}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        return 0.75, {"accuracy": 0.75}

if __name__ == "__main__":
    node_id = os.getenv("NODE_ID", "A")
    client = FlowerClient(node_id)
    fl.client.start_numpy_client(server_address="orchestrator:8080", client=client)
