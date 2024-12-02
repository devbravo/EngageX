from math import log
from typing import List

class FollowManager:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def follow(self):
        """Improved follow method based on multiple motivations."""
        if self.agent.user_type == "Agent":
            return

        candidates = [
            candidate for candidate in self.model.agents
            if candidate.unique_id != self.agent.unique_id
            and candidate.unique_id not in self.agent.following
        ]

        if not candidates:
            return

        max_followers = max(agent.follower_count for agent in self.model.agents)
        threshold_score = 0.5

        scores = [
            (candidate, self.calculate_total_score(candidate, max_followers))
            for candidate in candidates
            if self.calculate_total_score(candidate, max_followers) > threshold_score
        ]

        if scores:
            best_candidate = max(scores, key=lambda x: x[1])[0]
            self.update_following(best_candidate)
            print(
                f"Agent {self.agent.unique_id} ({self.agent.user_type}) followed "
                f"Agent {best_candidate.unique_id} ({best_candidate.user_type})"
            )

    def _update_following(self, candidate):
        """Updates following relationship and network graph."""
        self.agent.following.add(candidate.unique_id)
        self.agent.following_count += 1
        candidate.followers.add(self.agent.unique_id)
        candidate.follower_count += 1

        # Update the network graph
        self.model.g.add_edge(self.agent.unique_id, candidate.unique_id)
        self.model.g.nodes[candidate.unique_id]["follower_count"] = candidate.follower_count
        self.model.g.nodes[self.agent.unique_id]["following_count"] = self.agent.following_count
        self.model.g.nodes[candidate.unique_id]["follower_count"] = len(candidate.followers)
        self.model.g.nodes[self.agent.unique_id]["following_count"] = len(self.agent.following)

    def _calculate_total_score(self, candidate, max_followers):
        """Calculates the total score for a follow candidate."""
        return (
            self.calculate_mutual_connection_score(candidate)
            + self.calculate_popularity_score(candidate, max_followers)
            + self.calculate_engagement_score(candidate)
            + self.calculate_reciprocity_score(candidate)
            + self.calculate_social_proof_score(candidate)
        )

    def _calculate_mutual_connection_score(self, candidate):
        """Calculates the mutual connection score."""
        return len(set(self.agent.followers) & set(candidate.following)) * 0.1

    def _calculate_popularity_score(self, candidate, max_followers):
        """Calculates the popularity score."""
        return log(1 + candidate.follower_count) / log(1 + max_followers)

    def _calculate_engagement_score(self, candidate):
        """Calculates the engagement score based on recent interactions."""
        return min(self.agent.recent_engagements[candidate.unique_id] * 0.05, 0.5)

    def _calculate_reciprocity_score(self, candidate):
        """Calculates the reciprocity score."""
        if self.agent.unique_id in candidate.followers:
            return candidate.follow_back_prob
        return 0

    def _calculate_social_proof_score(self, candidate):
        """Calculates the social proof score."""
        shared_followers = self.agent.followers & candidate.followers
        social_proof = len(shared_followers) * 0.1
        return min(social_proof, 0.5)