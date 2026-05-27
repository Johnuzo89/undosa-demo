import flwr as fl
import numpy as np
from typing import List, Tuple

def fit_config(server_round: int):
    return {"server_round": server_round}

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, server_round, results, failures):
        print(f"Round {server_round}: Received updates from {len(results)} nodes")
        aggregated = super().aggregate_fit(server_round, results, failures)
        print(f"Round {server_round} completed.")
        return aggregated

strategy = SaveModelStrategy(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=2,
    min_evaluate_clients=2,
    on_fit_config_fn=fit_config,
)

if __name__ == "__main__":
    print("🚀 Starting UndosaTech Federated Server...")
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=strategy,
    )
