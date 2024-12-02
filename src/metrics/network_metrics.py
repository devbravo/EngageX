import numpy as np
import networkx as nx
from networkx import average_clustering, degree_centrality, betweenness_centrality
from networkx import is_connected, eigenvector_centrality

class MetricsManager:
    def __init__(self, model):
        self.model = model

    def compute_follower_count(self):
        follower_counts = [agent.follower_count for agent in self.model.agents]
        return np.mean(follower_counts)

    def compute_clustering_coeff(self):
        return average_clustering(self.model.g)

    def compute_connectivity_ratio(self):
        total_possible_edges = self.model.n_users * (self.model.n_users - 1) / 2
        return self.model.g.number_of_edges() / total_possible_edges

    def compute_degree_centrality(self):
        degree_centrality_results = degree_centrality(self.model.g)
        return np.mean(list(degree_centrality_results.values()))

    def compute_betweenness_centrality(self):
        betweenness_centrality_result = betweenness_centrality(self.model.g)
        return np.mean(list(betweenness_centrality_result.values()))

    def compute_eigenvector_centrality(self):
        eigenvector_centrality_result = eigenvector_centrality(self.model.g)
        return np.mean(list(eigenvector_centrality_result.values()))

    def compute_avg_shortest_path_length(self):
        if is_connected(self.model.g.to_undirected()):
            return nx.average_shortest_path_length(self.model.g.to_undirected())
        return None  # If the network is not fully connected

    def compute_assortativity_coefficient(self):
        return nx.degree_assortativity_coefficient(self.model.g)
  

def compute_network_metrics(model, n_steps=5):
    # Initialize metric accumulators
    metrics = {
        "follower_counts": [],
        "clustering_coeffs": [],
        "connectivity_ratios": [],
        "degree_centralities": [],
        "betweenness_centralities": [],
        "eigenvector_centralities": [],
        "shortest_path_lengths": [],
        "assortativity_coeffs": [],
    }

    # Initialize the MetricsManager
    metrics_manager = MetricsManager(model)

    # Run simulation steps
    for step in range(n_steps):
        print(f"Step {step + 1}")
        model.step()

        # Compute and store metrics
        metrics["follower_counts"].append(metrics_manager.compute_follower_count())
        metrics["clustering_coeffs"].append(metrics_manager.compute_clustering_coeff())
        metrics["connectivity_ratios"].append(metrics_manager.compute_connectivity_ratio())
        metrics["degree_centralities"].append(metrics_manager.compute_degree_centrality())
        metrics["betweenness_centralities"].append(metrics_manager.compute_betweenness_centrality())
        metrics["eigenvector_centralities"].append(metrics_manager.compute_eigenvector_centrality())
        metrics["shortest_path_lengths"].append(metrics_manager.compute_avg_shortest_path_length())
        metrics["assortativity_coeffs"].append(metrics_manager.compute_assortativity_coefficient())

    return metrics
