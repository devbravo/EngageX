import random

class UnfollowManager:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def unfollow(self):
        """Unfollows a user if certain conditions are met (e.g., low engagement)."""
        # Random chance to skip unfollowing
        if random.random() > 0.95:
            return

        candidates_to_unfollow = list(self.agent.following)
        if not candidates_to_unfollow:
            return

        unfollow_scores = self._calculate_unfollow_scores(candidates_to_unfollow)

        # Select the worst candidate to unfollow
        if unfollow_scores:
            worst_candidate = max(unfollow_scores, key=unfollow_scores.get)

            # Unfollow if the score is above a threshold
            if unfollow_scores[worst_candidate] > 0.7:
                self._update_unfollow_relationship(worst_candidate)

    def _calculate_unfollow_scores(self, candidates):
        """Calculates unfollow scores for all candidates."""
        unfollow_scores = {}
        for candidate_id in candidates:
            candidate = self.model.agents[candidate_id]

            low_engagement_score = self._calculate_low_engagement_score(candidate)
            content_fatigue_score = self._calculate_content_fatigue_score(candidate)
            # Additional scoring metrics can be added here

            unfollow_scores[candidate] = (
                0.5 * low_engagement_score +
                0.3 * content_fatigue_score
            )
        return unfollow_scores

    def _calculate_low_engagement_score(self, candidate):
        """Calculates a score based on low engagement from the candidate."""
        engagement = self.model.get_recent_engagements(candidate.unique_id, self.agent.unique_id)  # Assume this exists
        if engagement < 2:  # Low engagement threshold
            return 0.4  # High probability of unfollowing
        return 0

    def _calculate_content_fatigue_score(self, candidate):
        """Calculates a score based on posting frequency."""
        posting_frequency = self.model.get_posting_frequency(candidate.unique_id)  # Assume this exists
        if posting_frequency > 10:  # Overposting threshold
            return 0.3
        return 0

    def _update_unfollow_relationship(self, candidate):
        """Updates the relationships and network graph to reflect an unfollow."""
        self.agent.following.remove(candidate.unique_id)
        self.agent.following_count -= 1
        candidate.followers.remove(self.agent.unique_id)
        candidate.follower_count -= 1

        # Update the network graph
        self.model.g.remove_edge(self.agent.unique_id, candidate.unique_id)
        self.model.g.nodes[self.agent.unique_id]["following_count"] = self.agent.following_count
        self.model.g.nodes[candidate.unique_id]["follower_count"] = candidate.follower_count

        print(f"Agent {self.agent.unique_id} unfollowed Agent {candidate.unique_id}")