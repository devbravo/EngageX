class PostManager:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def post(self):
        """Creates new content that other agents can engage with."""
        current_day = self.model.current_step % 7
    

        # Check if the agent is active on the current day
        if current_day not in self.agent.active_days:
            return

        # Check if the agent decides to post based on probabilities
        if self.agent._random.random() < self.agent.post_frequency * self.agent.engagement_level:
            content_id = f'post_{self.agent.unique_id}_{self.model.current_step}'

            # Add the new post to the model's content pool
            self.model.content_pool.append({
                "content_id": content_id,
                "author_id": self.agent.unique_id,
                "user_type": self.agent.user_type,
                "timestamp": self.model.current_step,
                "engagement_count": 0
            })

            # Add the post to the agent's personal content list
            self.agent.agent_content.add(content_id)

            # Propagate the post to followers
            visibility_probability = 0.7
            for follower_id in self.agent.followers:
                if self.agent._random.random() < visibility_probability:
                    follower = self.model.agents[follower_id - 1]
                    follower.agent_content_pool.add(content_id)

            print(f'Agent {self.agent.unique_id} ({self.agent.user_type}) posted content: {content_id}')