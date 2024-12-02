import random
from typing import Dict
import networkx as nx
from mesa import Model
from agent.agent import XUserAgent


class XNetworkModel(Model):
    def __init__(self,
                 n_users: int,
                 seed: int = None,
                 user_types: Dict = None):
        super().__init__()
        if seed:
          self.seed = random.seed(seed)

        self.n_users = n_users
        self.user_types = user_types
        self.g = nx.DiGraph()

        self.content_pool = []
        self.current_step = 0

        self._initialize_agents()
        self._initialize_graph()


    def reset(self):
        """Resets the model to its initial state."""
        # Clear the graph and reinitialize agents
        self.remove_all_agents()
        self.g.clear()
        self.current_step = 0
        self._initialize_agents()
        self._initialize_graph()
        print(f"Number of agents after reset: {len(self._all_agents)}")



    def _initialize_agents(self):
        """Create agents, add them to the schedule, and set up their initial followers."""
        user_type_names = list(self.user_types.keys())
        user_type_dist = [self.user_types[user_type]["distribution"] for user_type in user_type_names]

        ai_agent = None
        agent_id_counter = 1

        for i in range(self.n_users):
            if i == 0: # Designate our Agent
                user_type = "Agent"
                user_config = {
                    "follower_range": (0, 0),
                    "following_range": (0, 0),
                    "post_frequency_range": (0, 0),
                    "engagement_range": (0.6, 0.6),
                    "network_building_range": (0, 0),
                    "follow_back_prob": 0.0,
                    "unfollow_prob": 0.0,
                    "color": "black",
                                }
            else:
                user_type = random.choices(user_type_names, weights=user_type_dist)[0]
                user_config = self.user_types[user_type]

            follower_count = self.n_users * random.uniform(*user_config["follower_range"])
            following_count = self.n_users * random.uniform(*user_config["following_range"])
            post_frequency = random.uniform(*user_config['post_frequency_range'])
            engagement_level = random.uniform(*user_config["engagement_range"])
            network_building_propensity = random.uniform(*user_config["network_building_range"])
            follow_back_prob = user_config["follow_back_prob"]
            unfollow_prob = user_config["unfollow_prob"]
            color = user_config["color"]

            agent = XUserAgent(
                unique_id=agent_id_counter,
                model=self,
                user_type=user_type,
                post_frequency = post_frequency,
                engagement_level=engagement_level,
                network_building_propensity=network_building_propensity,
                follow_back_prob=follow_back_prob,
                unfollow_prob = unfollow_prob,
                color=color,
                seed=self.seed
            )
            agent_id_counter += 1
            agent.follower_count = int(follower_count)
            agent.following_count = int(following_count)
            self._all_agents.add(agent)


            self.g.add_node(
                agent.unique_id,
                user_type=agent.user_type,
                # engagement_level=agent.engagement_level,
                follower_count=agent.follower_count,
                following_count=agent.following_count,
                followers = set(),
                following = set(),
                visible_content=set(),
                color=agent.color
                )

            if user_type == "Agent":
                ai_agent = agent

        if ai_agent:
            potential_followers = random.sample([a for a in self._all_agents if a.user_type != "Agent"], 2)
            for follower in potential_followers:
                self._add_connection(follower, ai_agent)

            # Assign three random following connections for the "Agent"
            potential_following = random.sample([a for a in self._all_agents if a.user_type != "Agent"], 2)
            for follow in potential_following:
                self._add_connection(ai_agent, follow)



    def _initialize_graph(self):
        """Initialize in-network and out-of-network following relationships."""
        agent_id = None
        for agent in self._all_agents:
            if agent.user_type == "Agent":
                agent_id = agent.unique_id
                continue


            follower_count = int(agent.follower_count)
            following_count =  int(agent.following_count)

            potential_followers = random.sample(
                [a for a in self._all_agents if a.unique_id != agent_id],
                min(follower_count, len(self._all_agents) - 1)
              )


            potential_following = random.sample(
                 [a for a in self._all_agents if a.unique_id != agent_id],
                min(following_count, len(self._all_agents) - 1)
                )

            for follower_user in potential_followers:
                if (follower_user.unique_id != agent_id
                    and follower_user.unique_id not in agent.followers):
                    self._add_connection(follower_user, agent)

            for follow_user in potential_following:
                if len(agent.following) >= following_count:
                  break
                if (follow_user.unique_id != agent_id
                    and follow_user.unique_id not in agent.following):
                    self._add_connection(agent, follow_user)


    def _add_connection(self, source_agent, target_agent):
        """Helper function to add a connection between two agents without duplicates."""
        # Only add edge if it doesn't already exist in the network
        if not self.g.has_edge(source_agent.unique_id, target_agent.unique_id):
            self.g.add_edge(source_agent.unique_id, target_agent.unique_id)
            source_agent.following.add(target_agent.unique_id)
            target_agent.followers.add(source_agent.unique_id)

            # Update the nodes in the network to match the agent
            source_agent.following_count += 1
            target_agent.follower_count += 1
            self._update_network_node(source_agent)
            self._update_network_node(target_agent)


    def _update_network_node(self, agent):
        """Helper function to keep network nodes in sync with agent attributes."""
        self.g.nodes[agent.unique_id]["follower_count"] = agent.follower_count
        self.g.nodes[agent.unique_id]["following_count"] = agent.following_count
        self.g.nodes[agent.unique_id]["followers"] = agent.followers
        self.g.nodes[agent.unique_id]["following"] = agent.following


    def step(self):
        self.current_step += 1
        self.agents.shuffle_do("step")