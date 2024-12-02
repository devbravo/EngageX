import random

class FollowBackManager:
    def __init__(self, agent, model):
        self.agent = agent
        self.model = model

    def follow_back(self, follower_agent):
        """Follows back an agent if they follow this agent first, based on a probability."""
        # Ensure the follower-agent relationship conditions are met
        if (follower_agent.unique_id in self.agent.followers and
            follower_agent.unique_id not in self.agent.following):

            # Check the probability condition for following back
            if random.random() < self.agent.follow_back_prob:
                # Update the agent's following list
                self.agent.following.add(follower_agent.unique_id)
                self.agent.following_count += 1

                # Update the follower agent's followers list
                follower_agent.followers.add(self.agent.unique_id)
                follower_agent.follower_count += 1

                # Update the network graph
                self.model.g.add_edge(self.agent.unique_id, follower_agent.unique_id)
                self.model.g.nodes[self.agent.unique_id]["following_count"] = self.agent.following_count
                self.model.g.nodes[follower_agent.unique_id]["follower_count"] = follower_agent.follower_count

                print(
                    f"Agent {self.agent.unique_id} ({self.agent.user_type}) followed back "
                    f"Agent {follower_agent.unique_id} ({follower_agent.user_type})"
                )