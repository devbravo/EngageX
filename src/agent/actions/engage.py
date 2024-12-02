import random

class EngagementManager:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def engage(self):
        """Engages with content by liking, commenting, or sharing."""
        if not self.agent.agent_content_pool:
            return

        # Select visible content to engage with
        visible_content = list(self.agent.agent_content_pool)
        chosen_content_id = random.choice(visible_content)

        # Decide whether to engage based on engagement level
        if self.agent._random.random() < self.agent.engagement_level:
            engagement_type = random.choices(
                ["like", "comment", "share"],
                weights=[0.6, 0.3, 0.1]
            )[0]

            # Update global engagement count
            self._update_global_engagement_count(chosen_content_id)

            # Update recent engagements
            self._update_recent_engagements(chosen_content_id, engagement_type)

            print(
                f"Agent {self.agent.unique_id} ({self.agent.user_type}) "
                f"{engagement_type}d content: {chosen_content_id}"
            )

            # Handle content sharing
            if engagement_type == "share":
                self._share_content(chosen_content_id)

            # Cleanup stale content from the agent's content pool
            self._cleanup_content_pool()

    def _update_global_engagement_count(self, content_id):
        """Updates the engagement count for a specific content item."""
        for content in self.model.content_pool:
            if content["content_id"] == content_id:
                content["engagement_count"] += 1
                break

    def _update_recent_engagements(self, content_id, engagement_type):
        """Tracks recent engagement activity."""
        self.agent.recent_engagements[content_id][engagement_type] += 1

    def _share_content(self, content_id):
        """Amplifies content reach by sharing it with followers."""
        for follower_id in self.agent.followers:
            follower = self.model.agents[follower_id - 1]
            if content_id not in follower.agent_content_pool:
                follower.agent_content_pool.add(content_id)

    def _cleanup_content_pool(self):
        """Removes stale content from the agent's local content pool."""
        max_content_age = 10
        self.agent.agent_content_pool = {
            content_id for content_id in self.agent.agent_content_pool
            if any(
                content["content_id"] == content_id
                and self.model.current_step - content["timestamp"] <= max_content_age
                for content in self.model.content_pool
            )
        }