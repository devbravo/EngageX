import numpy as np
from mesa import Agent
from collections import defaultdict
from agent.actions.follow import FollowManager
from agent.actions.post import PostManager
from agent.actions.engage import EngagementManager
from agent.actions.unfollow import UnfollowManager
from agent.actions.follow_back import FollowBackManager


class XUserAgent(Agent):
    def __init__(self,
                 unique_id, model, user_type,
                 post_frequency, engagement_level, network_building_propensity,
                 follow_back_prob, unfollow_prob, color, seed):
        super().__init__(model)
        self.user_type = user_type
        self.unique_id = unique_id
        self._random = np.random.default_rng(seed=self.unique_id)
        self.follower_count = 0
        self.following_count = 0
        self.followers = set()
        self.following = set()
        self.post_frequency = post_frequency
        self.engagement_level = engagement_level
        self.network_building_propensity = network_building_propensity
        self.follow_back_prob = follow_back_prob
        self.unfollow_prob = unfollow_prob
        self.color = color
        self.recent_engagements = defaultdict(lambda: {"like": 0, "comment": 0, "share": 0})
        self.agent_content_pool = set()
        self.agent_content = set()

        self.follower_growth = 0  # Tracks the number of new followers gained
        self.unfollow_count = 0  # Tracks the number of users unfollowed
        self.follow_back_count = 0
        
        self.follow_manager = FollowManager(self, model)
        self.post_manager = PostManager(self, model)
        self.engagement_manager = EngagementManager(self, model)
        self.unfollow_manager = UnfollowManager(self, model)
        self.follow_back_manager = FollowBackManager(self, model)

        self.active_days = self._assign_active_days()

    def _assign_active_days(self):
        """Randomly assign active days based on user type."""
        if self.user_type == "Lurker":
            return set(np.random.choice(range(7), size=2, replace=False))  # 1-2 active days
        elif self.user_type == "Casual":
            return set(np.random.choice(range(7), size=4, replace=False))  # 3-4 active days
        elif self.user_type == "Active":
            return set(np.random.choice(range(7), size=6, replace=False))  # 5-6 active days
        elif self.user_type == "Influencer":
            return set(range(7))  # Active every day
        elif self.user_type == "Bot":
            return set(np.random.choice(range(7), size=7, replace=False))  # Bots are active every day
        else:
            return set()  # No active days by default

    def step(self):
        """Defines the agent’s actions in each step, based on action-specific probabilities."""
        # Decide whether to post content
        noisy_post_frequency = self.post_frequency + self._random.uniform(-0.02, 0.02)
        if self._random.random() < noisy_post_frequency:
            self.post_manager.post()

        # Decide whether to engage with content
        if self._random.random() < self.engagement_level:
            self.engagement_manager.engage()

        # # Decide whether to follow a new user
        # if random.random() < self.network_building_propensity:
        #     self.follow()

        # # Decide whether to follow back
        # if random.random() < self.follow_back_prob:
        #     self.follow_back()

        # # Decide whether to unfollow
        # if random.random() < self.unfollow_prob:
        #     self.unfollow()
